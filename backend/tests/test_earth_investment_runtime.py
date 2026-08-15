from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.runtime.investments import CivilizationInvestmentRuntime, EarthInvestmentRuntime

client = TestClient(app)


def test_civilization_investment_runtime_has_risk_and_financial_metrics() -> None:
    runtime = CivilizationInvestmentRuntime()

    result = runtime.evaluate_project(
        project_type="ferrovia",
        capex=100_000_000,
        opex_yearly=5_000_000,
        annual_revenue=18_000_000,
        discount_rate=0.08,
        horizon_years=10,
    )

    assert result["project_type"] == "ferrovia"
    assert result["risk"]["level"] in {"low", "medium", "high", "very_high"}
    assert "cash_flow" in result
    assert "npv" in result
    assert "irr" in result
    assert "payback" in result
    assert "payback_period" in result


def test_civilization_project_score_api_returns_financial_contract() -> None:
    response = client.post(
        "/investments/civilization/project/score",
        json={
            "name": "Ferrovia Norte",
            "location": "São Paulo",
            "project_type": "ferrovia",
            "budget": 100_000_000,
            "capex": 100_000_000,
            "opex_yearly": 5_000_000,
            "annual_revenue": 18_000_000,
            "strategic_importance": 0.8,
            "discount_rate": 0.08,
            "horizon_years": 10,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["decision"] in {"fund", "review", "defer"}
    assert body["flow"]["risk"]["level"] in {"low", "medium", "high", "very_high"}
    assert "cash_flow" in body["flow"]
    assert body["flow"]["metrics"]["npv"] is not None
    assert body["flow"]["metrics"]["irr"] is not None
    assert body["flow"]["metrics"]["payback"] is not None
    assert body["flow"]["metrics"]["roi"] is not None


def test_project_score_links_financial_exposure_chain_to_trace_id() -> None:
    trace_id = "trace-financial-exposure-001"
    response = client.post(
        "/investments/project/score",
        json={
            "name": "Porto Norte",
            "project_type": "porto",
            "capex": 100_000_000,
            "opex_yearly": 5_000_000,
            "annual_revenue": 18_000_000,
            "trace_id": trace_id,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["trace_id"] == trace_id
    assert body["flow"]["trace_id"] == trace_id
    assert body["analysis"]["trace_id"] == trace_id
    assert body["flow"]["risk"] == body["analysis"]["risk"]
    assert body["flow"]["cash_flow"] == body["analysis"]["cash_flow"]
    assert body["flow"]["metrics"]["npv"] == body["analysis"]["npv"]
    assert body["flow"]["metrics"]["irr"] == body["analysis"]["irr"]
    assert body["flow"]["metrics"]["payback"] == body["analysis"]["payback"]
    assert body["flow"]["financial_exposure"] == body["analysis"]["financial_exposure"]


def test_civilization_project_score_api_accepts_frontend_aliases() -> None:
    response = client.post(
        "/investments/civilization/project/score",
        json={
            "project_name": "Ferrovia Norte",
            "location": "São Paulo",
            "project_type": "ferrovia",
            "capital_expenditure": 100_000_000,
            "annual_opex": 5_000_000,
            "annual_revenue": 18_000_000,
            "strategic_importance": 0.8,
            "discount": 0.08,
            "years": 10,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["project"]["name"] == "Ferrovia Norte"
    assert body["flow"]["metrics"]["npv"] is not None
    assert body["flow"]["metrics"]["irr"] is not None
    assert body["flow"]["metrics"]["payback"] is not None


def test_evaluate_project_generates_financial_metrics() -> None:
    runtime = EarthInvestmentRuntime()

    result = runtime.evaluate_project(
        project_type="ferrovia",
        capex=100_000_000,
        opex_yearly=5_000_000,
        annual_revenue=18_000_000,
        discount_rate=0.08,
        horizon_years=10,
    )

    assert result["project_type"] == "ferrovia"
    assert result["capex"] == 100_000_000
    assert result["opex"] == 5_000_000
    assert "npv" in result
    assert "irr" in result
    assert "payback_period" in result
    assert "roi" in result
    assert result["risk"]["score"] >= 0.0
    assert result["risk"]["level"] in {"low", "medium", "high", "very_high"}


def test_physical_event_becomes_economic_impact_and_financial_exposure() -> None:
    runtime = EarthInvestmentRuntime()

    result = runtime.evaluate_project(
        project_type="porto",
        capex=100_000_000,
        opex_yearly=5_000_000,
        annual_revenue=18_000_000,
        physical_event={
            "event_type": "flood",
            "severity": 0.8,
            "probability": 0.5,
            "duration_years": 2,
            "affected_asset_value": 20_000_000,
            "repair_cost": 4_000_000,
            "annual_revenue_at_risk": 3_000_000,
        },
    )

    impact = result["economic_impact"]
    assert impact["status"] == "assessed"
    assert impact["economic_impact"]["expected_loss"] == 12_400_000.0
    assert result["financial_exposure"] == 112_400_000.0
    assert result["cash_flow"][1] < 13_000_000
