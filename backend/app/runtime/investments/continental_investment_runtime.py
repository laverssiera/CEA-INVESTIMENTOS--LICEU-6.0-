from __future__ import annotations

from typing import Any


class ContinentalInvestmentRuntime:
    """Orquestra a decisão estratégica continental do John sobre projetos e portfólios."""

    async def john_decide(
        self,
        project: dict[str, Any],
        market_signal: dict[str, Any],
    ) -> dict[str, Any]:
        strategic_importance = float(project.get("strategic_importance", 0.5))
        risk_score = float(market_signal.get("risk_score", 0.5))
        economic_impact = float(market_signal.get("economic_impact", 0.5))

        decision_score = (
            0.45 * min(max(strategic_importance, 0.0), 1.0)
            + 0.35 * min(max(economic_impact, 0.0), 1.0)
            + 0.20 * (1.0 - min(max(risk_score, 0.0), 1.0))
        )

        if decision_score >= 0.72:
            decision = "approve"
        elif decision_score >= 0.52:
            decision = "review"
        else:
            decision = "defer"

        return {
            "decision": decision,
            "decision_owner": "John",
            "governance": "LICEU",
            "strategic_importance": round(strategic_importance, 4),
            "economic_impact": round(economic_impact, 4),
            "risk_score": round(risk_score, 4),
            "decision_score": round(decision_score, 4),
            "summary": "JOHN decide pela aprovação, revisão ou deferimento com governança LICEU.",
        }

    async def analyze(self, project: dict[str, Any], market_signal: dict[str, Any]) -> dict[str, Any]:
        return await self.john_decide(project, market_signal)
