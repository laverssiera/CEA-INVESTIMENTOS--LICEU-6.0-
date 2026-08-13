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

    async def get_global_monitoring_state(
        self,
        *,
        region: str | None = None,
        country: str | None = None,
        owner_id: str | None = None,
        segment: str | None = None,
        min_value: float | None = None,
        max_value: float | None = None,
    ) -> dict[str, Any]:
        """
        Retorna um acompanhamento consolidado das exposições globais por segmento.
        """
        segment_labels = {
            "mercados": "markets",
            "governos": "governments",
            "infraestrutura": "infrastructure",
            "fundos": "funds",
        }
        summary = {
            alias: {
                "assets": 0,
                "total_value": 0.0,
            }
            for alias in segment_labels.values()
        }
        countries: dict[str, float] = {}
        contributing_portfolios: set[str] = set()

        for portfolio in self.portfolios.values():
            if region and str(portfolio.get("region", "")).strip().lower() != region.strip().lower():
                continue
            if owner_id and str(portfolio.get("owner_id", "")).strip().lower() != owner_id.strip().lower():
                continue

            for asset in portfolio.get("assets", []):
                asset_country = asset.get("country")
                if country and str(asset_country or "").strip().lower() != country.strip().lower():
                    continue

                raw_segment = str(asset.get("segment", "")).strip().lower()
                if segment and raw_segment != segment.strip().lower():
                    continue

                segment_key = segment_labels.get(raw_segment)
                if not segment_key:
                    continue

                value = float(asset.get("value", 0.0))
                if min_value is not None and value < min_value:
                    continue
                if max_value is not None and value > max_value:
                    continue

                contributing_portfolios.add(str(portfolio.get("portfolio_id")))
                summary[segment_key]["assets"] += 1
                summary[segment_key]["total_value"] = round(
                    summary[segment_key]["total_value"] + value,
                    2,
                )

                if asset_country:
                    country_key = str(asset_country)
                    countries[country_key] = round(countries.get(country_key, 0.0) + value, 2)

        return {
            "status": "operational",
            "global_portfolios": len(contributing_portfolios),
            "filters": {
                "region": region,
                "country": country,
                "owner_id": owner_id,
                "segment": segment,
                "min_value": min_value,
                "max_value": max_value,
            },
            "segments": summary,
            "countries": countries,
            "captured_at": datetime.now(timezone.utc).isoformat(),
        }