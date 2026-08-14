"""Compatibility runtime for the Capital Global investment flow."""

from .earth_investment_runtime import EarthInvestmentRuntime
from .sovereign_investment_runtime import SovereignInvestmentRuntime


class CivilizationInvestmentRuntime(EarthInvestmentRuntime, SovereignInvestmentRuntime):
    """Combines sovereign opportunity analysis with full project finance scoring."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


__all__ = ["CivilizationInvestmentRuntime"]