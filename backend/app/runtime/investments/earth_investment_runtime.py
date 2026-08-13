from __future__ import annotations

from typing import Any

import numpy as np

from .econotech_impact_runtime import EconotechImpactRuntime


class EarthInvestmentRuntime:
    """Avalia projetos com foco em decisao de capital e impacto estrategico."""

    def __init__(self, econotech_runtime: EconotechImpactRuntime | None = None) -> None:
        self.econotech_runtime = econotech_runtime or EconotechImpactRuntime()

    PROJECT_PROFILES = (
        {
            "keywords": ("ferrovia", "rail", "railway"),
            "risk": 0.18,
            "revenue_yield": 0.15,
            "opex_ratio": 0.045,
            "strategic_impact": 0.95,
            "drivers": ("conectividade logistica", "reduz custo sistmico", "escala economica"),
        },
        {
            "keywords": ("porto", "port"),
            "risk": 0.16,
            "revenue_yield": 0.17,
            "opex_ratio": 0.05,
            "strategic_impact": 0.92,
            "drivers": ("fluxo comercial", "acesso a mercados", "trade enablement"),
        },
        {
            "keywords": ("hospital", "saude", "health"),
            "risk": 0.14,
            "revenue_yield": 0.13,
            "opex_ratio": 0.06,
            "strategic_impact": 0.91,
            "drivers": ("resiliencia social", "servico essencial", "capital humano"),
        },
        {
            "keywords": ("data center", "datacenter", "data-centre"),
            "risk": 0.19,
            "revenue_yield": 0.2,
            "opex_ratio": 0.07,
            "strategic_impact": 0.88,
            "drivers": ("infra de dados", "capacidade digital", "alta densidade de receita"),
        },
        {
            "keywords": ("sistema hidrico", "hidrico", "water", "reservatorio", "barragem"),
            "risk": 0.21,
            "revenue_yield": 0.12,
            "opex_ratio": 0.04,
            "strategic_impact": 0.9,
            "drivers": ("seguranca hidrica", "continuidade operacional", "destravamento regional"),
        },
        {
            "keywords": ("usina solar", "solar", "energia solar", "fotovoltaica"),
            "risk": 0.17,
            "revenue_yield": 0.14,
            "opex_ratio": 0.03,
            "strategic_impact": 0.87,
            "drivers": ("transicao energetica", "descarbonizacao", "custo marginal baixo"),
        },
        {
            "keywords": ("planta industrial", "industrial", "factory", "fabbrica"),
            "risk": 0.2,
            "revenue_yield": 0.16,
            "opex_ratio": 0.055,
            "strategic_impact": 0.84,
            "drivers": ("cadeia produtiva", "emprego", "valor agregado"),
        },
    )

    def _calculate_npv(self, rate: float, cash_flows: list[float]) -> float:
        if rate == -1:
            raise ValueError("discount_rate cannot be -1")
        return sum(cf / ((1 + rate) ** i) for i, cf in enumerate(cash_flows))

    def _calculate_irr(self, cash_flows: list[float], iterations: int = 1000) -> float:
        if not cash_flows or cash_flows[0] == 0:
            return 0.0

        rate = 0.1
        for _ in range(iterations):
            npv = self._calculate_npv(rate, cash_flows)
            if abs(npv) < 1e-6:
                return rate

            derivative = sum(-index * value / ((1 + rate) ** (index + 1)) for index, value in enumerate(cash_flows))
            if abs(derivative) < 1e-12:
                break

            rate = rate - npv / derivative

        return rate

    def _risk_level(self, score: float) -> str:
        if score < 0.15:
            return "low"
        if score < 0.25:
            return "medium"
        if score < 0.35:
            return "high"
        return "very_high"

    def _impact_level(self, score: float) -> str:
        if score >= 0.85:
            return "critical"
        if score >= 0.7:
            return "high"
        if score >= 0.5:
            return "medium"
        return "low"

    def _project_profile(self, reference_text: str) -> dict[str, Any]:
        normalized = reference_text.lower().strip()
        for profile in self.PROJECT_PROFILES:
            if any(keyword in normalized for keyword in profile["keywords"]):
                return profile

        return {
            "risk": 0.22,
            "revenue_yield": 0.13,
            "opex_ratio": 0.05,
            "strategic_impact": 0.8,
            "drivers": ("alocacao equilibrada", "base padrao", "diversificacao"),
        }

    def _build_cash_flows(
        self,
        *,
        capex: float,
        opex_yearly: float,
        annual_revenue: float,
        cash_flows: list[float] | None,
        horizon_years: int,
    ) -> list[float]:
        if cash_flows:
            return [float(value) for value in cash_flows]

        net_cash_flow = annual_revenue - opex_yearly
        return [-capex, *([net_cash_flow] * horizon_years)]

    def _calculate_payback(self, cash_flows: list[float]) -> float | None:
        cumulative_cash_flow = np.cumsum(cash_flows)
        for index, value in enumerate(cumulative_cash_flow):
            if value >= 0:
                return float(index)
        return None

    def evaluate_project(
        self,
        *,
        project_type: str,
        capex: float,
        opex_yearly: float,
        annual_revenue: float,
        project_name: str | None = None,
        location: str | None = None,
        cash_flows: list[float] | None = None,
        strategic_importance: float | None = None,
        discount_rate: float = 0.08,
        horizon_years: int = 10,
        physical_event: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Calcula risco, CAPEX, OPEX, cash flow, NPV, IRR, payback e ROI."""
        if horizon_years <= 0:
            return {"error": "horizon_years must be greater than 0"}
        if capex <= 0:
            return {"error": "capex must be greater than 0"}
        if opex_yearly < 0 or annual_revenue < 0:
            return {"error": "opex_yearly and annual_revenue must be non-negative"}

        project_label = project_name or project_type
        reference_text = " ".join(part for part in (project_label, project_type, location or "") if part).lower()
        profile = self._project_profile(reference_text)
        econotech = self.econotech_runtime.assess_event(physical_event)
        economic_impact = econotech["economic_impact"]

        capex_value = float(capex) + economic_impact["repair_cost"]
        opex_value = float(opex_yearly)
        revenue_value = max(0.0, float(annual_revenue) - economic_impact["revenue_at_risk"])
        cash_flow_values = self._build_cash_flows(
            capex=capex_value,
            opex_yearly=opex_value,
            annual_revenue=revenue_value,
            cash_flows=cash_flows,
            horizon_years=horizon_years,
        )

        annual_net_cash_flow = revenue_value - opex_value
        npv = self._calculate_npv(discount_rate, cash_flow_values)
        irr = self._calculate_irr(cash_flow_values)
        payback_period = self._calculate_payback(cash_flow_values)

        total_net_profit = sum(cash_flow_values)
        roi = total_net_profit / capex_value if capex_value else 0.0

        revenue_ratio = revenue_value / max(capex_value, 1.0)
        opex_ratio = opex_value / max(capex_value, 1.0)
        base_risk = float(profile["risk"])
        risk_score = min(
            0.85,
            base_risk
            + (opex_ratio * 0.6)
            + (max(0.0, 0.15 - revenue_ratio) * 0.8)
            + economic_impact["risk_uplift"],
        )

        strategic_score = float(profile["strategic_impact"])
        if strategic_importance is not None:
            strategic_score = (strategic_score * 0.7) + (max(0.0, min(1.0, strategic_importance)) * 0.3)

        strategic_score = min(0.98, max(0.0, strategic_score + min(0.04, revenue_ratio * 0.1)))
        decision_score = min(
            1.0,
            max(
                0.0,
                (strategic_score * 0.4)
                + ((1.0 - risk_score) * 0.25)
                + (max(0.0, roi) / 1.5 * 0.2)
                + (max(0.0, npv) / max(capex_value, 1.0) * 0.15),
            ),
        )

        if decision_score >= 0.75:
            decision = "fund"
        elif decision_score >= 0.55:
            decision = "review"
        else:
            decision = "defer"

        impact_summary = " / ".join(profile["drivers"])

        return {
            "project_name": project_label,
            "project_type": project_type,
            "location": location,
            "capex": round(capex_value, 2),
            "opex": round(opex_value, 2),
            "cash_flow": [round(float(value), 2) for value in cash_flow_values],
            "annual_net_cash_flow": round(float(annual_net_cash_flow), 2),
            "npv": round(float(npv), 2),
            "irr": round(float(irr), 4),
            "payback": payback_period if payback_period is not None else horizon_years + 1,
            "payback_period": payback_period if payback_period is not None else horizon_years + 1,
            "roi": round(float(roi), 4),
            "risk": {
                "score": round(float(risk_score), 4),
                "level": self._risk_level(risk_score),
            },
            "impacto_estrategico": {
                "score": round(float(strategic_score), 4),
                "level": self._impact_level(strategic_score),
                "drivers": list(profile["drivers"]),
                "summary": impact_summary,
            },
            "decision_score": round(float(decision_score), 4),
            "decision": decision,
            "horizon_years": horizon_years,
            "discount_rate": round(float(discount_rate), 4),
            "economic_impact": econotech,
            "financial_exposure": round(float(capex) + economic_impact["expected_loss"], 2),
        }


__all__ = ["EarthInvestmentRuntime"]
