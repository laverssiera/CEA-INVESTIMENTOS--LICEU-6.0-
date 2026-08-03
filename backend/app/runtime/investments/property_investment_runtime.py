from __future__ import annotations

from datetime import datetime
from typing import Any


class PropertyInvestmentRuntime:
    def __init__(self) -> None:
        pass

    async def analyze_property_opportunity(
        self,
        *,
        property_name: str,
        purchase_price: float,
        monthly_rent: float,
        occupancy_rate: float,
        annual_expenses: float,
        appreciation_rate: float = 0.04,
    ) -> dict[str, Any]:
        """
        Analisa um ativo imobiliario com base em renda e valorizacao esperada.
        """
        if purchase_price <= 0:
            return {"error": "purchase_price must be greater than 0"}

        occupancy = min(max(occupancy_rate, 0.0), 1.0)
        annual_gross_rent = monthly_rent * 12 * occupancy
        annual_net_income = annual_gross_rent - annual_expenses

        cap_rate = annual_net_income / purchase_price
        one_year_value = purchase_price * (1 + appreciation_rate)
        one_year_total_return = ((one_year_value - purchase_price) + annual_net_income) / purchase_price

        classification = "high"
        if cap_rate < 0.05:
            classification = "low"
        elif cap_rate < 0.08:
            classification = "medium"

        return {
            "property_name": property_name,
            "purchase_price": purchase_price,
            "monthly_rent": monthly_rent,
            "occupancy_rate": round(occupancy, 4),
            "annual_expenses": annual_expenses,
            "appreciation_rate": round(appreciation_rate, 4),
            "annual_gross_rent": round(annual_gross_rent, 2),
            "annual_net_income": round(annual_net_income, 2),
            "cap_rate": round(cap_rate, 4),
            "one_year_total_return": round(one_year_total_return, 4),
            "return_classification": classification,
            "recommended": one_year_total_return >= 0.08,
            "analysis_date": datetime.now().isoformat(),
        }

    async def simulate_rental_cashflow(
        self,
        *,
        months: int,
        initial_cash: float,
        monthly_rent: float,
        occupancy_rate: float,
        monthly_expenses: float,
    ) -> dict[str, Any]:
        """
        Simula fluxo de caixa mensal para operacao de aluguel.
        """
        if months <= 0:
            return {"error": "months must be greater than 0"}

        occupancy = min(max(occupancy_rate, 0.0), 1.0)
        balance = initial_cash
        history: list[dict[str, Any]] = []

        for month in range(1, months + 1):
            effective_rent = monthly_rent * occupancy
            net = effective_rent - monthly_expenses
            balance += net
            history.append(
                {
                    "month": month,
                    "effective_rent": round(effective_rent, 2),
                    "monthly_expenses": round(monthly_expenses, 2),
                    "net_cash_flow": round(net, 2),
                    "balance": round(balance, 2),
                }
            )

        return {
            "months": months,
            "initial_cash": initial_cash,
            "final_balance": round(balance, 2),
            "total_net_cash_flow": round(balance - initial_cash, 2),
            "occupancy_rate": round(occupancy, 4),
            "history": history,
            "generated_at": datetime.now().isoformat(),
        }
