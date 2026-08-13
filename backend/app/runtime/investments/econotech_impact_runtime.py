from __future__ import annotations

from typing import Any


class EconotechImpactRuntime:
    """Converte um evento físico em impacto econômico esperado."""

    def assess_event(self, event: dict[str, Any] | None) -> dict[str, Any]:
        if not event:
            return {
                "status": "not_provided",
                "event": None,
                "economic_impact": {
                    "expected_loss": 0.0,
                    "repair_cost": 0.0,
                    "revenue_at_risk": 0.0,
                    "financial_exposure": 0.0,
                    "risk_uplift": 0.0,
                },
            }

        severity = min(max(float(event.get("severity", 0.0)), 0.0), 1.0)
        probability = min(max(float(event.get("probability", 0.0)), 0.0), 1.0)
        duration_years = max(int(event.get("duration_years", 1)), 1)
        affected_asset_value = max(float(event.get("affected_asset_value", 0.0)), 0.0)
        repair_cost = max(float(event.get("repair_cost", 0.0)), 0.0)
        annual_revenue_at_risk = max(float(event.get("annual_revenue_at_risk", 0.0)), 0.0)

        asset_loss = affected_asset_value * severity
        revenue_loss = annual_revenue_at_risk * duration_years * severity
        gross_loss = asset_loss + repair_cost + revenue_loss
        expected_loss = gross_loss * probability
        expected_repair_cost = repair_cost * probability
        expected_revenue_at_risk = annual_revenue_at_risk * severity * probability

        return {
            "status": "assessed",
            "event": {
                "event_type": event.get("event_type", "unspecified"),
                "severity": round(severity, 4),
                "probability": round(probability, 4),
                "duration_years": duration_years,
            },
            "economic_impact": {
                "asset_loss": round(asset_loss, 2),
                "repair_cost": round(expected_repair_cost, 2),
                "revenue_at_risk": round(expected_revenue_at_risk, 2),
                "expected_loss": round(expected_loss, 2),
                "financial_exposure": round(expected_loss, 2),
                "risk_uplift": round(severity * probability * 0.25, 4),
            },
        }


__all__ = ["EconotechImpactRuntime"]