from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import uuid


class ContinentalPortfolioRuntime:
    """Portfólio continental com governança LICEU e decisão financeira da CEA."""

    def __init__(self) -> None:
        self.portfolios: dict[str, dict[str, Any]] = {}

    async def create_continental_portfolio(
        self,
        assets: list[dict[str, Any]],
        owner_id: str,
        *,
        region: str = "Continental",
    ) -> dict[str, Any]:
        portfolio_id = str(uuid.uuid4())
        total_value = float(sum(float(asset.get("value", 0.0)) for asset in assets))

        portfolio = {
            "portfolio_id": portfolio_id,
            "owner_id": owner_id,
            "region": region,
            "assets": assets,
            "total_initial_value": total_value,
            "decision_owner": "CEA",
            "governance": "LICEU",
            "status": "active",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self.portfolios[portfolio_id] = portfolio
        return portfolio

    async def get_portfolio_state(self, portfolio_id: str) -> dict[str, Any]:
        return self.portfolios.get(portfolio_id, {"error": "Portfolio not found"})

    async def get_state(self) -> dict[str, Any]:
        total_value = float(
            sum(portfolio.get("total_initial_value", 0.0) for portfolio in self.portfolios.values())
        )
        return {
            "status": "operational",
            "governance": "LICEU",
            "total_portfolios": len(self.portfolios),
            "total_initial_value": total_value,
            "decision_owner": "CEA",
            "captured_at": datetime.now(timezone.utc).isoformat(),
        }
