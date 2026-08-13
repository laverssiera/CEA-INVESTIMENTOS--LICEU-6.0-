from __future__ import annotations

from typing import Any

from .risk_scoring_runtime import RiskScoringRuntime


class ContinentalRiskRuntime(RiskScoringRuntime):
    """Avalia riscos regionais e de projeto com decisão do John e governança da LICEU."""

    async def score_continental_project(self, project_data: dict[str, Any]) -> dict[str, Any]:
        result = await self.calculate_score(project_data)
        return {
            **result,
            "decision_owner": "John",
            "governance": "LICEU",
            "summary": "JOHN decide o nível de risco e a governança permanece sob LICEU.",
        }
