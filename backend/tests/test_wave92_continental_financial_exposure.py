import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models.immutable_runtime import ImmutableEvent
from app.runtime.investments.continental_financial_exposure_runtime import (
    ContinentalFinancialExposureRuntime,
)
from app.services.immutable_runtime_service import ImmutableFinancialRuntime


IDS = {
    "source_event_id": "evt-archimedes-001",
    "trace_id": "trace-archimedes-001",
    "decision_id": "decision-archimedes-001",
    "governance_decision_id": "governance-archimedes-001",
    "execution_id": "execution-archimedes-001",
    "infrastructure_change_id": "infra-change::f86f3b7cddab9312ac202294",
    "supplier_analysis_id": "supplier-analysis::archimedes-001",
    "procurement_plan_id": "procurement-plan-e331ed7665157d2fe625c39b",
    "economic_impact_id": "economic-impact-8823098e873caa50e378325c9",
}


@pytest.fixture
def runtime():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine, tables=[ImmutableEvent.__table__])
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    db = factory()
    history = ImmutableFinancialRuntime(db)
    history.record_event("w89.source", {"event_id": IDS["source_event_id"], **IDS})
    history.record_event(
        "w89.infrastructure",
        {"infrastructure_change_id": IDS["infrastructure_change_id"], "parent_event_id": IDS["source_event_id"]},
    )
    history.record_event(
        "w90.supplier",
        {"supplier_analysis_id": IDS["supplier_analysis_id"], "parent_event_id": IDS["infrastructure_change_id"]},
    )
    history.record_event(
        "w90.procurement",
        {"procurement_plan_id": IDS["procurement_plan_id"], "parent_event_id": IDS["supplier_analysis_id"]},
    )
    history.record_event(
        "w91.economic_impact",
        {
            "economic_impact_id": IDS["economic_impact_id"],
            "parent_event_id": IDS["procurement_plan_id"],
            "project": {
                "project_name": "Corredor Continental",
                "project_type": "porto",
                "capex": 100000000,
                "opex_yearly": 5000000,
                "annual_revenue": 18000000,
                "discount_rate": 0.08,
                "horizon_years": 10,
            },
        },
    )
    yield ContinentalFinancialExposureRuntime(db, factory)
    db.close()
    engine.dispose()


def test_wave_92_persists_reads_and_is_idempotent(runtime):
    first = runtime.run_wave(IDS)
    second = runtime.run_wave(IDS)

    assert first["status"] == "PASS", first["error"]
    assert first["financial_exposure_id"] == second["financial_exposure_id"]
    assert first["canonical_write_valid"] is True
    assert first["canonical_read_valid"] is True
    assert first["persistence_verified"] is True
    assert first["consumer_visibility_valid"] is True
    assert first["replay_valid"] is True
    assert first["audit_valid"] is True
    assert first["lineage"]["parent_event_id"]
    assert second["idempotency_valid"] is True


def test_wave_92_blocks_when_canonical_chain_is_missing(runtime):
    result = runtime.run_wave({**IDS, "economic_impact_id": "missing-economic-impact"})

    assert result["status"] == "BLOCKED"
    assert result["persistence_verified"] is False
    assert result["financial_exposure_id"] is None
