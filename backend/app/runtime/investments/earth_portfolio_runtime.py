from __future__ import annotations

from typing import Any

from .earth_project_score_runtime import EarthProjectScoreRuntime


class EarthPortfolioRuntime:
    def __init__(self, scorer: EarthProjectScoreRuntime | None = None) -> None:
        self.scorer = scorer or EarthProjectScoreRuntime()

    def build_portfolio(
        self,
        projects: list[dict[str, Any]],
        available_capital: float | None = None,
    ) -> dict[str, Any]:
        scored = self.scorer.score_projects(projects)
        ranked_projects = scored["projects"]

        selected_projects: list[dict[str, Any]] = []
        rejected_projects: list[dict[str, Any]] = []
        remaining_capital = float(available_capital) if available_capital is not None else None

        for project in ranked_projects:
            capex = float(project["capex"])
            if remaining_capital is None or capex <= remaining_capital:
                selected_projects.append(project)
                if remaining_capital is not None:
                    remaining_capital = round(remaining_capital - capex, 2)
            else:
                rejected_projects.append(project)

        allocated_capital = sum(float(project["capex"]) for project in selected_projects)
        financial_exposure = sum(
            float(project.get("financial_exposure", project["capex"])) for project in selected_projects
        )
        portfolio_npv = sum(float(project["npv"]) for project in selected_projects)
        portfolio_roi = (
            sum(float(project["roi"]) * float(project["capex"]) for project in selected_projects) / allocated_capital
            if allocated_capital
            else 0.0
        )
        portfolio_risk = (
            sum(float(project["risk"]["score"]) * float(project["capex"]) for project in selected_projects) / allocated_capital
            if allocated_capital
            else 0.0
        )
        portfolio_strategic_impact = (
            sum(float(project["impacto_estrategico"]["score"]) * float(project["capex"]) for project in selected_projects) / allocated_capital
            if allocated_capital
            else 0.0
        )

        if portfolio_npv > 0 and portfolio_risk <= 0.25:
            recommendation = "approve"
        elif selected_projects:
            recommendation = "review"
        else:
            recommendation = "defer"

        return {
            "status": "portfolio_built",
            "available_capital": available_capital,
            "allocated_capital": round(float(allocated_capital), 2),
            "financial_exposure": round(float(financial_exposure), 2),
            "remaining_capital": remaining_capital,
            "portfolio_npv": round(float(portfolio_npv), 2),
            "portfolio_roi": round(float(portfolio_roi), 4),
            "portfolio_risk": round(float(portfolio_risk), 4),
            "portfolio_strategic_impact": round(float(portfolio_strategic_impact), 4),
            "recommendation": recommendation,
            "selected_projects": selected_projects,
            "rejected_projects": rejected_projects,
            "ranked_projects": ranked_projects,
            "recommended_project": scored["recommended_project"],
        }


__all__ = ["EarthPortfolioRuntime"]