from __future__ import annotations

import asyncio

from app.runtime.investments.property_investment_runtime import PropertyInvestmentRuntime


def test_analyze_property_opportunity_happy_path() -> None:
    runtime = PropertyInvestmentRuntime()

    result = asyncio.run(
        runtime.analyze_property_opportunity(
            property_name="Edificio Solaris",
            purchase_price=1_000_000,
            monthly_rent=12_000,
            occupancy_rate=0.9,
            annual_expenses=20_000,
            appreciation_rate=0.05,
        )
    )

    assert result["property_name"] == "Edificio Solaris"
    assert result["annual_gross_rent"] == 129600.0
    assert result["annual_net_income"] == 109600.0
    assert result["cap_rate"] == 0.1096
    assert result["one_year_total_return"] == 0.1596
    assert result["return_classification"] == "high"
    assert result["recommended"] is True
    assert "analysis_date" in result


def test_property_runtime_input_validation_and_cashflow() -> None:
    runtime = PropertyInvestmentRuntime()

    invalid = asyncio.run(
        runtime.analyze_property_opportunity(
            property_name="Invalid",
            purchase_price=0,
            monthly_rent=5_000,
            occupancy_rate=1.2,
            annual_expenses=8_000,
        )
    )
    assert invalid == {"error": "purchase_price must be greater than 0"}

    cashflow = asyncio.run(
        runtime.simulate_rental_cashflow(
            months=3,
            initial_cash=10_000,
            monthly_rent=2_000,
            occupancy_rate=1.2,
            monthly_expenses=700,
        )
    )

    assert cashflow["months"] == 3
    assert cashflow["occupancy_rate"] == 1.0
    assert cashflow["final_balance"] == 13_900.0
    assert cashflow["total_net_cash_flow"] == 3_900.0
    assert len(cashflow["history"]) == 3
    assert cashflow["history"][0]["net_cash_flow"] == 1_300.0
    assert "generated_at" in cashflow
