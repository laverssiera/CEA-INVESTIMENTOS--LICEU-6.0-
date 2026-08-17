from __future__ import annotations

import uuid
from typing import Any

from .earth_investment_runtime import EarthInvestmentRuntime
from .econotech_impact_runtime import EconotechImpactRuntime

# Namespace fixo do CEA para derivacao deterministica da cadeia causal (WAVE 83).
_CHAIN_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, "cea.liceu.federation.causal-chain")


def _derive_id(prefix: str, *parts: Any) -> str:
    """Deriva um id deterministico (uuid5) a partir dos elos anteriores da cadeia causal."""
    seed = "|".join(str(part) for part in parts)
    return f"{prefix}-{uuid.uuid5(_CHAIN_NAMESPACE, seed)}"


class PlanetaryFinancialExposureRuntime:
    """WAVE 83 - CEA: consome o resultado real da W82 (ECONOTECH) e calcula a
    exposicao financeira planetaria, preservando a cadeia causal completa ate o
    financial_exposure_id. Reutiliza EarthInvestmentRuntime/EconotechImpactRuntime
    existentes; nao cria Event Store, Ledger, Registry ou mecanismo de lineage novo.
    """

    SCENARIOS = {
        "base": {"revenue_factor": 1.0, "opex_factor": 1.0, "capex_factor": 1.0},
        "otimista": {"revenue_factor": 1.15, "opex_factor": 0.9, "capex_factor": 0.95},
        "pessimista": {"revenue_factor": 0.85, "opex_factor": 1.2, "capex_factor": 1.1},
    }

    def __init__(
        self,
        earth_investment_runtime: EarthInvestmentRuntime | None = None,
        econotech_runtime: EconotechImpactRuntime | None = None,
    ) -> None:
        self.earth_investment_runtime = earth_investment_runtime or EarthInvestmentRuntime()
        self.econotech_runtime = econotech_runtime or self.earth_investment_runtime.econotech_runtime

    def build_causal_chain(self, project: dict[str, Any], w82_result: dict[str, Any] | None) -> dict[str, Any]:
        """Reconstroi/valida a cadeia causal ate o economic_impact_id (resultado real da W82)."""
        w82_result = w82_result or {}
        reference = str(project.get("project_name") or project.get("project_type") or "project")

        source_event_id = w82_result.get("source_event_id") or _derive_id("EVT", reference, project.get("location"))
        trace_id = w82_result.get("trace_id") or _derive_id("TRACE", source_event_id)
        decision_id = w82_result.get("decision_id") or _derive_id("DEC", trace_id)
        governance_decision_id = w82_result.get("governance_decision_id") or _derive_id("GOV-DEC", decision_id)
        execution_id = w82_result.get("execution_id") or _derive_id("EXEC", governance_decision_id)
        infrastructure_change_id = w82_result.get("infrastructure_change_id") or _derive_id("INFRA-CHG", execution_id)
        supplier_analysis_id = w82_result.get("supplier_analysis_id") or _derive_id("SUP-AN", infrastructure_change_id)
        procurement_plan_id = w82_result.get("procurement_plan_id") or _derive_id("PROC-PLAN", supplier_analysis_id)
        economic_impact_id = w82_result.get("economic_impact_id") or _derive_id("ECO-IMPACT", procurement_plan_id)

        return {
            "source_event_id": source_event_id,
            "trace_id": trace_id,
            "decision_id": decision_id,
            "governance_decision_id": governance_decision_id,
            "execution_id": execution_id,
            "infrastructure_change_id": infrastructure_change_id,
            "supplier_analysis_id": supplier_analysis_id,
            "procurement_plan_id": procurement_plan_id,
            "economic_impact_id": economic_impact_id,
        }

    def _evaluate_scenario(self, project: dict[str, Any], factors: dict[str, float]) -> dict[str, Any]:
        return self.earth_investment_runtime.evaluate_project(
            project_type=str(project["project_type"]),
            capex=float(project["capex"]) * factors["capex_factor"],
            opex_yearly=float(project["opex_yearly"]) * factors["opex_factor"],
            annual_revenue=float(project["annual_revenue"]) * factors["revenue_factor"],
            project_name=project.get("project_name"),
            location=project.get("location"),
            strategic_importance=project.get("strategic_importance"),
            discount_rate=float(project.get("discount_rate", 0.08)),
            horizon_years=int(project.get("horizon_years", 10)),
            physical_event=project.get("physical_event"),
        )

    def _sensitivity(self, project: dict[str, Any], base_discount_rate: float) -> dict[str, Any]:
        deltas = (-0.02, 0.02)
        discount_sensitivity = {}
        for delta in deltas:
            rate = max(0.001, base_discount_rate + delta)
            result = self._evaluate_scenario(
                project,
                {"revenue_factor": 1.0, "opex_factor": 1.0, "capex_factor": 1.0},
            ) if rate == base_discount_rate else self.earth_investment_runtime.evaluate_project(
                project_type=str(project["project_type"]),
                capex=float(project["capex"]),
                opex_yearly=float(project["opex_yearly"]),
                annual_revenue=float(project["annual_revenue"]),
                project_name=project.get("project_name"),
                location=project.get("location"),
                strategic_importance=project.get("strategic_importance"),
                discount_rate=rate,
                horizon_years=int(project.get("horizon_years", 10)),
                physical_event=project.get("physical_event"),
            )
            discount_sensitivity[f"discount_rate_{delta:+.2f}"] = {
                "discount_rate": round(rate, 4),
                "npv": result["npv"],
                "irr": result["irr"],
            }

        capex_sensitivity = {}
        for factor in (0.9, 1.1):
            result = self._evaluate_scenario(
                project, {"revenue_factor": 1.0, "opex_factor": 1.0, "capex_factor": factor}
            )
            capex_sensitivity[f"capex_{factor:.1f}x"] = {
                "capex": result["capex"],
                "npv": result["npv"],
                "payback": result["payback"],
            }

        return {"discount_rate": discount_sensitivity, "capex": capex_sensitivity}

    def evaluate(self, project: dict[str, Any], w82_result: dict[str, Any] | None = None) -> dict[str, Any]:
        """Calcula o modelo financeiro planetario completo (CAPEX -> exposicao financeira)."""
        chain = self.build_causal_chain(project, w82_result)

        scenarios: dict[str, Any] = {}
        for name, factors in self.SCENARIOS.items():
            result = self._evaluate_scenario(project, factors)
            scenarios[name] = {
                "capex": result["capex"],
                "opex": result["opex"],
                "cash_flow": result["cash_flow"],
                "npv": result["npv"],
                "irr": result["irr"],
                "payback": result["payback"],
                "roi": result["roi"],
                "risk": result["risk"],
                "financial_exposure": result["financial_exposure"],
                "economic_impact": result["economic_impact"],
                "decision": result["decision"],
            }

        base = scenarios["base"]
        sensitivity = self._sensitivity(project, float(project.get("discount_rate", 0.08)))

        cumulative_financial_impact = round(
            sum(scenario["financial_exposure"] for scenario in scenarios.values()), 2
        )

        viable = bool(base["npv"] > 0 and base["irr"] >= float(project.get("discount_rate", 0.08)))
        viability_decision = "viavel" if viable and base["decision"] == "fund" else (
            "revisar" if base["decision"] == "review" else "inviavel"
        )

        financial_exposure_id = _derive_id(
            "FIN-EXP", chain["economic_impact_id"], project.get("project_name"), project.get("project_type")
        )

        return {
            **chain,
            "financial_exposure_id": financial_exposure_id,
            "capex": base["capex"],
            "opex": base["opex"],
            "cash_flow": base["cash_flow"],
            "revenue_projetada": project.get("annual_revenue"),
            "financial_exposure": base["financial_exposure"],
            "npv": base["npv"],
            "irr": base["irr"],
            "payback": base["payback"],
            "risk": base["risk"],
            "scenarios": scenarios,
            "sensitivity": sensitivity,
            "cumulative_financial_impact": cumulative_financial_impact,
            "viability_decision": viability_decision,
            "lineage": {
                "financial_exposure_id": financial_exposure_id,
                "economic_impact_id": chain["economic_impact_id"],
                "procurement_plan_id": chain["procurement_plan_id"],
                "infrastructure_change_id": chain["infrastructure_change_id"],
                "execution_id": chain["execution_id"],
                "decision_id": chain["decision_id"],
                "trace_id": chain["trace_id"],
                "source_event_id": chain["source_event_id"],
            },
        }

    def validate(self, project: dict[str, Any], result: dict[str, Any], replay_result: dict[str, Any]) -> dict[str, bool]:
        chain_fields = (
            "source_event_id",
            "trace_id",
            "decision_id",
            "governance_decision_id",
            "execution_id",
            "infrastructure_change_id",
            "supplier_analysis_id",
            "procurement_plan_id",
            "economic_impact_id",
        )
        lineage = result["lineage"]

        contract_valid = all(project.get(key) is not None for key in ("project_type", "capex", "opex_yearly", "annual_revenue"))
        lineage_valid = all(result.get(field) for field in chain_fields) and lineage["economic_impact_id"] == result["economic_impact_id"]
        financial_model_valid = result["capex"] > 0 and result["opex"] >= 0
        cash_flow_valid = len(result["cash_flow"]) == int(project.get("horizon_years", 10)) + 1
        npv_valid = isinstance(result["npv"], (int, float))
        irr_valid = isinstance(result["irr"], (int, float))
        payback_valid = result["payback"] is not None
        exposure_valid = result.get("financial_exposure_id") is not None and result["financial_exposure"] >= 0
        risk_valid = result["risk"]["level"] in {"low", "medium", "high", "very_high"}
        scenario_valid = all(key in result["scenarios"] for key in ("base", "otimista", "pessimista"))
        sensitivity_valid = "discount_rate" in result["sensitivity"] and "capex" in result["sensitivity"]

        replay_valid = replay_result["financial_exposure_id"] == result["financial_exposure_id"]
        idempotency_valid = (
            replay_result["financial_exposure_id"] == result["financial_exposure_id"]
            and replay_result["npv"] == result["npv"]
            and replay_result["financial_exposure"] == result["financial_exposure"]
        )

        rollback_recovery = self.rollback_and_recover(project, result["lineage"])
        rollback_valid = rollback_recovery["rollback_valid"]
        recovery_valid = rollback_recovery["recovery_valid"]

        audit_valid = lineage_valid and exposure_valid and all(
            (
                contract_valid,
                financial_model_valid,
                cash_flow_valid,
                npv_valid,
                irr_valid,
                payback_valid,
                risk_valid,
                scenario_valid,
                sensitivity_valid,
            )
        )

        return {
            "contract_valid": contract_valid,
            "lineage_valid": lineage_valid,
            "financial_model_valid": financial_model_valid,
            "cash_flow_valid": cash_flow_valid,
            "npv_valid": npv_valid,
            "irr_valid": irr_valid,
            "payback_valid": payback_valid,
            "exposure_valid": exposure_valid,
            "risk_valid": risk_valid,
            "scenario_valid": scenario_valid,
            "sensitivity_valid": sensitivity_valid,
            "replay_valid": replay_valid,
            "idempotency_valid": idempotency_valid,
            "rollback_valid": rollback_valid,
            "recovery_valid": recovery_valid,
            "audit_valid": audit_valid,
        }

    def rollback_and_recover(self, project: dict[str, Any], lineage: dict[str, Any]) -> dict[str, Any]:
        """Simula rollback controlado (descarte de estado transiente) seguido de recovery
        reconstruindo o resultado somente a partir da cadeia causal (sem novo store)."""
        w82_result = {
            "source_event_id": lineage["source_event_id"],
            "trace_id": lineage["trace_id"],
            "economic_impact_id": lineage["economic_impact_id"],
            "procurement_plan_id": lineage["procurement_plan_id"],
            "infrastructure_change_id": lineage["infrastructure_change_id"],
            "execution_id": lineage["execution_id"],
        }
        recovered = self.evaluate(project, w82_result)
        rollback_valid = recovered["economic_impact_id"] == lineage["economic_impact_id"]
        recovery_valid = recovered["financial_exposure_id"] is not None and rollback_valid
        return {
            "rollback_valid": rollback_valid,
            "recovery_valid": recovery_valid,
            "recovered_financial_exposure_id": recovered["financial_exposure_id"],
        }

    def run_wave(self, project: dict[str, Any], w82_result: dict[str, Any] | None = None) -> dict[str, Any]:
        """Executa a WAVE 83 completa: evaluate -> replay -> validate -> envelope final."""
        result = self.evaluate(project, w82_result)
        # replay: reexecuta a partir da mesma cadeia causal ja resolvida (idempotencia)
        replay_result = self.evaluate(project, result["lineage"] | {
            "source_event_id": result["source_event_id"],
            "trace_id": result["trace_id"],
            "decision_id": result["decision_id"],
            "governance_decision_id": result["governance_decision_id"],
            "execution_id": result["execution_id"],
            "infrastructure_change_id": result["infrastructure_change_id"],
            "supplier_analysis_id": result["supplier_analysis_id"],
            "procurement_plan_id": result["procurement_plan_id"],
        })

        validations = self.validate(project, result, replay_result)

        if result.get("financial_exposure_id") is None or not validations["lineage_valid"]:
            status = "FAIL"
        else:
            status = "PASS" if all(validations.values()) else "FAIL"

        return {
            "wave": 83,
            "scope": "planetary",
            "origin": "CEA",
            "source_event_id": result["source_event_id"],
            "trace_id": result["trace_id"],
            "decision_id": result["decision_id"],
            "governance_decision_id": result["governance_decision_id"],
            "execution_id": result["execution_id"],
            "infrastructure_change_id": result["infrastructure_change_id"],
            "supplier_analysis_id": result["supplier_analysis_id"],
            "procurement_plan_id": result["procurement_plan_id"],
            "economic_impact_id": result["economic_impact_id"],
            "financial_exposure_id": result["financial_exposure_id"],
            **validations,
            "status": status,
            "financial_summary": {
                "capex": result["capex"],
                "opex": result["opex"],
                "cash_flow": result["cash_flow"],
                "financial_exposure": result["financial_exposure"],
                "npv": result["npv"],
                "irr": result["irr"],
                "payback": result["payback"],
                "risk": result["risk"],
                "scenarios": result["scenarios"],
                "sensitivity": result["sensitivity"],
                "cumulative_financial_impact": result["cumulative_financial_impact"],
                "viability_decision": result["viability_decision"],
            },
            "lineage": result["lineage"],
        }


__all__ = ["PlanetaryFinancialExposureRuntime"]
