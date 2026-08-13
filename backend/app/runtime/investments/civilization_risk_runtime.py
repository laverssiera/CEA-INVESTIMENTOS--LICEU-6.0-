"""Compatibility runtime for the Capital Global risk flow."""

from .risk_scoring_runtime import RiskScoringRuntime


class CivilizationRiskRuntime(RiskScoringRuntime):
    pass


__all__ = ["CivilizationRiskRuntime"]