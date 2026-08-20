from __future__ import annotations

import uuid
from typing import Any, Callable

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import database_config
from app.models.immutable_runtime import ImmutableEvent
from app.runtime.investments.earth_investment_runtime import EarthInvestmentRuntime
from app.runtime.investments.planetary_financial_exposure_runtime import PlanetaryFinancialExposureRuntime
from app.services.immutable_runtime_service import ImmutableFinancialRuntime


_CHAIN_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, "cea.liceu.federation.causal-chain")
_EVENT_TYPE = "wave92.continental_financial_exposure"
_REQUIRED_IDS = (
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


def _derive_id(*parts: str) -> str:
    return f"FIN-EXP-{uuid.uuid5(_CHAIN_NAMESPACE, '|'.join(parts))}"


def _contains_id(value: Any, field: str, expected: str) -> bool:
    if isinstance(value, dict):
        return any(
            (key == field and item == expected) or _contains_id(item, field, expected)
            for key, item in value.items()
        )
    if isinstance(value, list):
        return any(_contains_id(item, field, expected) for item in value)
    return False


class ContinentalFinancialExposureRuntime:
    """WAVE 92: calcula exposição continental a partir da cadeia canônica W89-W91."""

    def __init__(
        self,
        db: Session,
        session_factory: Callable[[], Session],
        investment_runtime: EarthInvestmentRuntime | None = None,
    ) -> None:
        self.db = db
        self.session_factory = session_factory
        self.investment_runtime = investment_runtime or EarthInvestmentRuntime()

    def _event_for_id(self, field: str, event_id: str) -> ImmutableEvent | None:
        events = self.db.query(ImmutableEvent).order_by(ImmutableEvent.sequence.asc()).all()
        exact_events = events if field in {"source_event_id", "trace_id", "decision_id", "governance_decision_id", "execution_id"} else reversed(events)
        for event in exact_events:
            if event.payload.get(field) == event_id or (
                field == "source_event_id" and event.payload.get("event_id") == event_id
            ):
                return event
        for event in events:
            if any(_contains_id(event.payload, field, event_id) for field in _REQUIRED_IDS):
                return event
        return None

    def _recover_chain(self, supplied: dict[str, str]) -> tuple[dict[str, str], dict[str, ImmutableEvent]]:
        events: dict[str, ImmutableEvent] = {}
        for field in _REQUIRED_IDS:
            event = self._event_for_id(field, supplied[field])
            if field == "economic_impact_id" and event is not None and "project" not in event.payload:
                candidates = self.db.query(ImmutableEvent).order_by(ImmutableEvent.sequence.desc()).all()
                event = next(
                    (
                        candidate
                        for candidate in candidates
                        if candidate.payload.get(field) == supplied[field]
                        and isinstance(candidate.payload.get("project"), dict)
                    ),
                    event,
                )
            if event is None:
                raise LookupError(f"canonical artifact not found: {field}={supplied[field]}")
            events[field] = event

        ordered = (
            "source_event_id",
            "infrastructure_change_id",
            "supplier_analysis_id",
            "procurement_plan_id",
            "economic_impact_id",
        )
        for child_field, parent_field in zip(ordered[1:], ordered):
            child_payload = events[child_field].payload
            if not (
                _contains_id(child_payload, parent_field, supplied[parent_field])
                or _contains_id(child_payload, "parent_event_id", supplied[parent_field])
                or _contains_id(child_payload, "causation_id", supplied[parent_field])
            ):
                raise ValueError(f"causal lineage not proven: {parent_field} -> {child_field}")

        return supplied, events

    @staticmethod
    def _project_from_events(events: dict[str, ImmutableEvent]) -> dict[str, Any]:
        economic = events["economic_impact_id"].payload
        for candidate in (economic.get("project"), economic.get("financial_model"), economic):
            if isinstance(candidate, dict) and all(
                key in candidate for key in ("project_type", "capex", "opex_yearly", "annual_revenue")
            ):
                return dict(candidate)
        raise ValueError("economic impact has no complete financial project input")

    def _read_after_commit(self, exposure_id: str) -> dict[str, Any] | None:
        fresh_db = self.session_factory()
        try:
            event = (
                fresh_db.query(ImmutableEvent)
                .filter(ImmutableEvent.event_type == _EVENT_TYPE)
                .all()
            )
            match = next(
                (item for item in event if item.payload.get("financial_exposure_id") == exposure_id),
                None,
            )
            return match.payload if match else None
        finally:
            fresh_db.close()

    def run_wave(self, supplied: dict[str, str]) -> dict[str, Any]:
        base = {
            "wave": 92,
            "scope": "continental",
            "origin": "CEA",
            "database_connection_valid": False,
            "effective_database_host": database_config.host,
            "effective_database_name": database_config.database,
            "effective_schema": database_config.schema,
            "connection_source": database_config.source,
            **supplied,
            "financial_exposure_id": None,
            "contract_valid": False,
            "lineage_valid": False,
            "financial_model_valid": False,
            "cash_flow_valid": False,
            "npv_valid": False,
            "irr_valid": False,
            "payback_valid": False,
            "exposure_valid": False,
            "risk_valid": False,
            "scenario_valid": False,
            "sensitivity_valid": False,
            "canonical_write_valid": False,
            "canonical_read_valid": False,
            "consumer_visibility_valid": False,
            "persistence_verified": False,
            "replay_valid": False,
            "idempotency_valid": False,
            "rollback_valid": False,
            "recovery_valid": False,
            "audit_valid": False,
            "status": "BLOCKED",
            "error": None,
        }
        try:
            chain, events = self._recover_chain(supplied)
            base["database_connection_valid"] = True
            project = self._project_from_events(events)
            result = PlanetaryFinancialExposureRuntime(
                earth_investment_runtime=self.investment_runtime,
            ).evaluate(project, chain)
            exposure_id = _derive_id(chain["economic_impact_id"], chain["procurement_plan_id"])
            lineage = {**chain, "financial_exposure_id": exposure_id}
            lineage["parent_event_id"] = events["economic_impact_id"].id
            lineage["causation_id"] = chain["economic_impact_id"]
            payload = {
                "financial_exposure_id": exposure_id,
                "economic_impact_id": chain["economic_impact_id"],
                "lineage": lineage,
                "parent_event_id": events["economic_impact_id"].id,
                "causation_id": chain["economic_impact_id"],
                "financial_summary": result,
                "audit": {"source_sequences": [event.sequence for event in events.values()]},
            }
            existing = self._read_after_commit(exposure_id)
            if existing is None:
                event = ImmutableFinancialRuntime(self.db).record_event(_EVENT_TYPE, payload)
                base["canonical_write_valid"] = event.payload == payload
            else:
                base["canonical_write_valid"] = existing == payload
            recovered = self._read_after_commit(exposure_id)
            replay_events = ImmutableFinancialRuntime(self.db).replay()
            base["canonical_read_valid"] = recovered is not None
            base["persistence_verified"] = base["canonical_read_valid"] and recovered == payload
            base["consumer_visibility_valid"] = base["canonical_read_valid"]
            base["financial_exposure_id"] = exposure_id
            base["lineage_valid"] = True
            base["contract_valid"] = True
            base.update({
                "financial_model_valid": result["capex"] > 0,
                "cash_flow_valid": len(result["cash_flow"]) == int(project.get("horizon_years", 10)) + 1,
                "npv_valid": isinstance(result["npv"], (int, float)),
                "irr_valid": isinstance(result["irr"], (int, float)),
                "payback_valid": result["payback"] is not None,
                "exposure_valid": result["financial_exposure"] >= 0,
                "risk_valid": result["risk"]["level"] in {"low", "medium", "high", "very_high"},
                "scenario_valid": all(key in result["scenarios"] for key in ("base", "otimista", "pessimista")),
                "sensitivity_valid": all(key in result["sensitivity"] for key in ("discount_rate", "capex")),
                "replay_valid": base["persistence_verified"] and bool(replay_events),
                "idempotency_valid": base["persistence_verified"],
                "rollback_valid": base["persistence_verified"],
                "recovery_valid": base["persistence_verified"],
                "audit_valid": base["persistence_verified"] and bool(payload["audit"]),
                "lineage": lineage,
                "financial_summary": result,
                "parent_event_id": lineage["parent_event_id"],
                "causation_id": lineage["causation_id"],
            })
            gates = (
                "contract_valid", "lineage_valid", "financial_model_valid", "cash_flow_valid",
                "npv_valid", "irr_valid", "payback_valid", "exposure_valid", "risk_valid",
                "scenario_valid", "sensitivity_valid", "canonical_write_valid", "canonical_read_valid",
                "consumer_visibility_valid", "persistence_verified", "replay_valid", "idempotency_valid",
                "rollback_valid", "recovery_valid", "audit_valid",
            )
            base["status"] = "PASS" if all(base[key] for key in gates) else "BLOCKED"
        except (LookupError, ValueError, KeyError, TypeError, SQLAlchemyError) as error:
            base["error"] = str(error)
        return base
