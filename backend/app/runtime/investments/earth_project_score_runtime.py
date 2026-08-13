from __future__ import annotations

from typing import Any

from .earth_investment_runtime import EarthInvestmentRuntime


class EarthProjectScoreRuntime:
    EXAMPLE_PROJECTS: list[dict[str, Any]] = [
        {
            "project_name": "Nova ferrovia",
            "project_type": "ferrovia",
            "location": "Corredor logístico nacional",
            "capex": 240_000_000,
            "opex_yearly": 10_800_000,
            "annual_revenue": 39_000_000,
            "strategic_importance": 0.97,
        },
        {
            "project_name": "Usina solar",
            "project_type": "usina solar",
            "location": "Nordeste",
            "capex": 180_000_000,
            "opex_yearly": 5_400_000,
            "annual_revenue": 31_500_000,
            "strategic_importance": 0.88,
        },
        {
            "project_name": "Porto",
            "project_type": "porto",
            "location": "Litoral exportador",
            "capex": 310_000_000,
            "opex_yearly": 15_500_000,
            "annual_revenue": 55_000_000,
            "strategic_importance": 0.95,
        },
        {
            "project_name": "Hospital",
            "project_type": "hospital",
            "location": "Regiao metropolitana",
            "capex": 130_000_000,
            "opex_yearly": 7_800_000,
            "annual_revenue": 24_500_000,
            "strategic_importance": 0.93,
        },
        {
            "project_name": "Data center",
            "project_type": "data center",
            "location": "Hub digital",
            "capex": 210_000_000,
            "opex_yearly": 14_700_000,
            "annual_revenue": 42_000_000,
            "strategic_importance": 0.91,
        },
        {
            "project_name": "Sistema hídrico",
            "project_type": "sistema hidrico",
            "location": "Bacia regional",
            "capex": 160_000_000,
            "opex_yearly": 6_400_000,
            "annual_revenue": 28_000_000,
            "strategic_importance": 0.92,
        },
    ]

    def __init__(self, investment_runtime: EarthInvestmentRuntime | None = None) -> None:
        self.investment_runtime = investment_runtime or EarthInvestmentRuntime()

    def _resolve_project_inputs(self, project: dict[str, Any]) -> dict[str, Any]:
        project_name = str(project.get("project_name") or project.get("name") or project.get("project_type") or "Project")
        project_type = str(project.get("project_type") or project_name)
        reference_text = f"{project_name} {project_type} {project.get('location', '')}"
        profile = self.investment_runtime._project_profile(reference_text)

        capex = float(project.get("capex") or project.get("budget") or 0.0)
        opex_yearly = project.get("opex_yearly")
        annual_revenue = project.get("annual_revenue")

        if capex <= 0:
            raise ValueError("capex or budget must be greater than 0")

        if opex_yearly is None:
            opex_yearly = capex * float(profile["opex_ratio"])
        if annual_revenue is None:
            annual_revenue = capex * float(profile["revenue_yield"])

        return {
            "project_name": project_name,
            "project_type": project_type,
            "location": project.get("location"),
            "capex": capex,
            "opex_yearly": float(opex_yearly),
            "annual_revenue": float(annual_revenue),
            "cash_flows": project.get("cash_flows"),
            "strategic_importance": project.get("strategic_importance"),
            "discount_rate": float(project.get("discount_rate", 0.08)),
            "horizon_years": int(project.get("horizon_years", 10)),
            "physical_event": project.get("physical_event"),
        }

    def score_project(self, project: dict[str, Any]) -> dict[str, Any]:
        inputs = self._resolve_project_inputs(project)
        analysis = self.investment_runtime.evaluate_project(
            project_name=inputs["project_name"],
            project_type=inputs["project_type"],
            location=inputs["location"],
            capex=inputs["capex"],
            opex_yearly=inputs["opex_yearly"],
            annual_revenue=inputs["annual_revenue"],
            cash_flows=inputs["cash_flows"],
            strategic_importance=inputs["strategic_importance"],
            discount_rate=inputs["discount_rate"],
            horizon_years=inputs["horizon_years"],
            physical_event=inputs["physical_event"],
        )

        decision_score = float(analysis["decision_score"])
        if decision_score >= 0.75:
            capital_priority = "priority_1"
        elif decision_score >= 0.55:
            capital_priority = "priority_2"
        else:
            capital_priority = "priority_3"

        analysis["capital_priority"] = capital_priority
        analysis["score_band"] = capital_priority.replace("priority_", "band_")
        return analysis

    def score_projects(self, projects: list[dict[str, Any]]) -> dict[str, Any]:
        scored_projects = [self.score_project(project) for project in projects]
        ranked_projects = sorted(scored_projects, key=lambda item: item["decision_score"], reverse=True)

        for rank, project in enumerate(ranked_projects, start=1):
            project["rank"] = rank

        return {
            "status": "scored",
            "total_projects": len(ranked_projects),
            "recommended_project": ranked_projects[0] if ranked_projects else None,
            "projects": ranked_projects,
        }

    def example_projects(self) -> dict[str, Any]:
        scored = self.score_projects(self.EXAMPLE_PROJECTS)
        return {
            "status": "examples_ready",
            "count": scored["total_projects"],
            "projects": scored["projects"],
            "recommended_project": scored["recommended_project"],
        }


__all__ = ["EarthProjectScoreRuntime"]