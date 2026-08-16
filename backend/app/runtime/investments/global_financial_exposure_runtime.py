from __future__ import annotations

import json
from collections import defaultdict
from typing import Any

from .earth_investment_runtime import EarthInvestmentRuntime


class GlobalFinancialExposureRuntime:
    """Agrega métricas financeiras da cidade ao mundo."""

    LEVELS = ("city", "region", "continent", "world")

    def __init__(self, investment_runtime: EarthInvestmentRuntime | None = None) -> None:
        self.investment_runtime = investment_runtime or EarthInvestmentRuntime()

    def _scope_keys(self, project: dict[str, Any]) -> dict[str, str]:
        city = str(project.get("city") or project.get("location") or "unknown")
        region = str(project.get("region") or "unknown")
        continent = str(project.get("continent") or "unknown")
        return {
            "city": city,
            "region": region,
            "continent": continent,
            "world": "world",
        }

    def calculate(self, projects: list[dict[str, Any]]) -> dict[str, Any]:
        grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)

        for project in projects:
            result = self.investment_runtime.evaluate_project(
                project_type=str(project["project_type"]),
                capex=float(project["capex"]),
                opex_yearly=float(project["opex_yearly"]),
                annual_revenue=float(project["annual_revenue"]),
                project_name=project.get("project_name"),
                location=project.get("city") or project.get("location"),
                cash_flows=project.get("cash_flows"),
                strategic_importance=project.get("strategic_importance"),
                discount_rate=float(project.get("discount_rate", 0.08)),
                horizon_years=int(project.get("horizon_years", 10)),
                physical_event=project.get("physical_event"),
            )
            for level, key in self._scope_keys(project).items():
                grouped[(level, key)].append(result)

        scopes: dict[str, dict[str, Any]] = {}
        for (level, key), results in grouped.items():
            cash_flow_length = max(len(result["cash_flow"]) for result in results)
            cash_flow = [
                round(sum(result["cash_flow"][index] for result in results if index < len(result["cash_flow"])), 2)
                for index in range(cash_flow_length)
            ]
            npv = self.investment_runtime._calculate_npv(
                float(results[0]["discount_rate"]), cash_flow
            )
            irr = self.investment_runtime._calculate_irr(cash_flow)
            cumulative = 0.0
            payback = None
            for index, value in enumerate(cash_flow):
                cumulative += value
                if cumulative >= 0:
                    payback = index
                    break

            capex = sum(float(result["capex"]) for result in results)
            scopes[f"{level}:{key}"] = {
                "level": level,
                "name": key,
                "projects": len(results),
                "capex": round(capex, 2),
                "cash_flow": cash_flow,
                "npv": round(float(npv), 2),
                "irr": round(float(irr), 4),
                "payback": payback if payback is not None else max(len(cash_flow), 1),
                "financial_exposure": round(
                    sum(float(result["financial_exposure"]) for result in results), 2
                ),
            }

        return {"scopes": scopes}


def demo_projects() -> list[dict[str, Any]]:
    return [
        {
            "project_name": "Ferrovia Norte",
            "project_type": "ferrovia",
            "city": "São Paulo",
            "region": "Sudeste",
            "continent": "América do Sul",
            "capex": 100_000_000,
            "opex_yearly": 5_000_000,
            "annual_revenue": 18_000_000,
        },
        {
            "project_name": "Porto Norte",
            "project_type": "porto",
            "city": "Santos",
            "region": "Sudeste",
            "continent": "América do Sul",
            "capex": 80_000_000,
            "opex_yearly": 4_000_000,
            "annual_revenue": 16_000_000,
        },
        {
            "project_name": "Usina Solar Nordeste",
            "project_type": "usina solar",
            "city": "Petrolina",
            "region": "Nordeste",
            "continent": "América do Sul",
            "capex": 60_000_000,
            "opex_yearly": 1_800_000,
            "annual_revenue": 10_000_000,
        },
    ]


if __name__ == "__main__":
    print(json.dumps(GlobalFinancialExposureRuntime().calculate(demo_projects()), ensure_ascii=False, indent=2))


__all__ = ["GlobalFinancialExposureRuntime", "demo_projects"]