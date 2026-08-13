from app.runtime.investments import EarthInvestmentRuntime


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
