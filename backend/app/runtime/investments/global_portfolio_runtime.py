from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import uuid


class GlobalPortfolioRuntime:
    def __init__(self) -> None:
        self.portfolios: dict[str, dict[str, Any]] = {}

    async def create_global_portfolio(
        self,
        assets: list[dict[str, Any]],
        owner_id: str,
        region: str = "global",
    ) -> dict[str, Any]:
        """
        Cria um portfólio com contexto global (multi-região).
        """
        portfolio_id = str(uuid.uuid4())
        total_value = float(sum(asset.get("value", 0) for asset in assets))

        portfolio = {
            "portfolio_id": portfolio_id,
            "owner_id": owner_id,
            "region": region,
            "assets": assets,
            "total_initial_value": total_value,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "active",
        }

        self.portfolios[portfolio_id] = portfolio
        return portfolio

    async def get_portfolio_state(self, portfolio_id: str) -> dict[str, Any]:
        return self.portfolios.get(portfolio_id, {"error": "Portfolio not found"})

    async def get_global_state(self) -> dict[str, Any]:
        """
        Retorna visão agregada dos portfólios ativos em escopo global.
        """
        total_value = float(
            sum(p.get("total_initial_value", 0.0) for p in self.portfolios.values())
        )
        owners = {p.get("owner_id") for p in self.portfolios.values() if p.get("owner_id")}
        regions: dict[str, int] = {}
        for portfolio in self.portfolios.values():
            region = str(portfolio.get("region", "global"))
            regions[region] = regions.get(region, 0) + 1

        return {
            "status": "operational",
            "total_portfolios": len(self.portfolios),
            "total_initial_value": total_value,
            "owners": len(owners),
            "regions": regions,
            "captured_at": datetime.now(timezone.utc).isoformat(),
        }