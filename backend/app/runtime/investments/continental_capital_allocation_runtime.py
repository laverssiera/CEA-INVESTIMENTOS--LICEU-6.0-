from __future__ import annotations

from typing import Any

from .capital_allocation_runtime import CapitalAllocationRuntime


class ContinentalCapitalAllocationRuntime(CapitalAllocationRuntime):
    """A alocação financeira continental é decidida pela CEA e validada pela LICEU."""

    async def allocate_for_continent(
        self,
        total_capital: float,
        risk_profile: str = "Moderate",
        *,
        region: str = "Continental",
    ) -> dict[str, Any]:
        normalized_profile = risk_profile.strip().title() if risk_profile else "Moderate"
        allocation = await self.suggest_allocation(total_capital, normalized_profile)

        allocation["decision_owner"] = "CEA"
        allocation["governance"] = "LICEU"
        allocation["region"] = region
        allocation["allocation_policy"] = "continental"
        allocation["summary"] = "CEA decide a alocação financeira e LICEU governa o processo."
        return allocation
