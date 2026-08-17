from fastapi.testclient import TestClient

from app.main import app
from app.runtime.investments.planetary_financial_exposure_runtime import PlanetaryFinancialExposureRuntime

client = TestClient(app)

PROJECT = {
    "project_name": "Porto Planetario Norte",
    "project_type": "porto",
    "location": "Costa Atlantica",
    "capex": 100_000_000,
    "opex_yearly": 5_000_000,
    "annual_revenue": 18_000_000,
    "discount_rate": 0.08,
    "horizon_years": 10,
}


def test_wave_83_runtime_preserves_full_causal_chain_and_passes() -> None:
    runtime = PlanetaryFinancialExposureRuntime()

    result = runtime.run_wave(dict(PROJECT))

    assert result["wave"] == 83
    assert result["scope"] == "planetary"
    assert result["origin"] == "CEA"

    for field in (
        "source_event_id",
        "trace_id",
        "decision_id",
        "governance_decision_id",
        "execution_id",
        "infrastructure_change_id",
        "supplier_analysis_id",
        "procurement_plan_id",
        "economic_impact_id",
        "financial_exposure_id",
    ):
        assert result[field] is not None

    assert result["lineage"]["economic_impact_id"] == result["economic_impact_id"]
    assert result["lineage"]["financial_exposure_id"] == result["financial_exposure_id"]
    assert result["status"] == "PASS"


def test_wave_83_is_idempotent_across_two_executions() -> None:
    runtime = PlanetaryFinancialExposureRuntime()

    first = runtime.run_wave(dict(PROJECT))
    second = runtime.run_wave(dict(PROJECT))

    assert first["financial_exposure_id"] == second["financial_exposure_id"]
    assert first["economic_impact_id"] == second["economic_impact_id"]
    assert first["financial_summary"]["npv"] == second["financial_summary"]["npv"]
    assert second["idempotency_valid"] is True


def test_wave_83_consumes_real_w82_result_chain() -> None:
    runtime = PlanetaryFinancialExposureRuntime()
    w82_result = {
        "source_event_id": "EVT-W82-001",
        "trace_id": "TRACE-W82-001",
        "economic_impact_id": "ECO-IMPACT-W82-001",
    }

    result = runtime.run_wave(dict(PROJECT), w82_result)

    assert result["source_event_id"] == "EVT-W82-001"
    assert result["trace_id"] == "TRACE-W82-001"
    assert result["economic_impact_id"] == "ECO-IMPACT-W82-001"
    assert result["lineage"]["economic_impact_id"] == "ECO-IMPACT-W82-001"
    assert result["status"] == "PASS"


def test_wave_83_rejects_null_financial_exposure_id_never_happens_by_design() -> None:
    runtime = PlanetaryFinancialExposureRuntime()
    result = runtime.evaluate(dict(PROJECT))
    assert result["financial_exposure_id"] is not None
    assert result["lineage"]["economic_impact_id"] == result["economic_impact_id"]


def test_planetary_financial_exposure_endpoint() -> None:
    response = client.post(
        "/investments/planetary/financial-exposure",
        json={"project": PROJECT},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["wave"] == 83
    assert body["status"] == "PASS"
    assert body["financial_exposure_id"] is not None
