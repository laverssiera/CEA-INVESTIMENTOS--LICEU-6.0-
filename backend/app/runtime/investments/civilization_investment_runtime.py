"""Compatibility runtime for the Capital Global sovereign investment flow."""

from .sovereign_investment_runtime import SovereignInvestmentRuntime


class CivilizationInvestmentRuntime(SovereignInvestmentRuntime):
    pass


__all__ = ["CivilizationInvestmentRuntime"]