from __future__ import annotations

from typing import Any

from .project_financing_runtime import ProjectFinancingRuntime


class ContinentalProjectFinanceRuntime(ProjectFinancingRuntime):
    """Calcula impacto financeiro do projeto com responsabilidade da ECONOTECH."""

    async def simulate_project_finance(
        self,
        cash_flows: list[float],
        discount_rate: float,
    ) -> dict[str, Any]:
        result = await super().simulate_financing(cash_flows, discount_rate)

        if "error" in result:
            return {
                **result,
                "owner": "ECONOTECH",
                "governance": "LICEU",
                "decision_owner": "John",
            }

        result["owner"] = "ECONOTECH"
        result["governance"] = "LICEU"
        result["decision_owner"] = "John"
        result["summary"] = "ECONOTECH calcula o impacto financeiro do projeto, enquanto LICEU governa a decisão."
        return result
