"""Compatibility runtime for the Capital Global portfolio flow."""

from .global_portfolio_runtime import GlobalPortfolioRuntime


class CivilizationPortfolioRuntime(GlobalPortfolioRuntime):
    pass


__all__ = ["CivilizationPortfolioRuntime"]