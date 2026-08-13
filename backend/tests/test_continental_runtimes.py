import pytest

from app.runtime.investments import (
    ContinentalCapitalAllocationRuntime,
    ContinentalInvestmentRuntime,
    ContinentalPortfolioRuntime,
    ContinentalProjectFinanceRuntime,
    ContinentalRiskRuntime,
)


@pytest.mark.asyncio
async def test_continental_runtime_exports_and_core_flow() -> None:
    investment = ContinentalInvestmentRuntime()
    investment_decision = await investment.john_decide(
        {"name": "Continental Grid", "strategic_importance": 0.8},
        {"risk_score": 0.3, "economic_impact": 0.82},
    )
    assert investment_decision["decision"] in {"approve", "review"}
    assert investment_decision["governance"] == "LICEU"

    allocation = ContinentalCapitalAllocationRuntime()
    suggestion = await allocation.allocate_for_continent(1_000_000.0, "Moderate")
    assert suggestion["decision_owner"] == "CEA"
    assert suggestion["allocations"]

    portfolio = ContinentalPortfolioRuntime()
    created = await portfolio.create_continental_portfolio(
        [{"asset_id": "C-1", "value": 250_000.0, "segment": "infraestrutura"}],
        "owner-continental-1",
        region="Continental",
    )
    assert created["region"] == "Continental"
    assert created["governance"] == "LICEU"

    finance = ContinentalProjectFinanceRuntime()
    financed = await finance.simulate_project_finance([ -500_000.0, 150_000.0, 180_000.0, 200_000.0 ], 0.1)
    assert financed["owner"] == "ECONOTECH"
    assert "npv" in financed

    risk = ContinentalRiskRuntime()
    risk_score = await risk.score_continental_project({"location": "South America", "complexity": 6, "budget": 500000})
    assert risk_score["classification"] in {"Low", "Medium", "High"}
    assert risk_score["decision_owner"] == "John"
