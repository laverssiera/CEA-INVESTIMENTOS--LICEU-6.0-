"""Compatibility runtime for global investment monitoring flows."""

from .global_portfolio_runtime import GlobalPortfolioRuntime


class GlobalInvestmentRuntime(GlobalPortfolioRuntime):
    pass


__all__ = ["GlobalInvestmentRuntime"]