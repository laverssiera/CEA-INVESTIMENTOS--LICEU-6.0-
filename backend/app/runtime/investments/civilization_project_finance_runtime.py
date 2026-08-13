"""Compatibility runtime for the Capital Global project-finance flow."""

from .project_financing_runtime import ProjectFinancingRuntime


class CivilizationProjectFinanceRuntime(ProjectFinancingRuntime):
    pass


__all__ = ["CivilizationProjectFinanceRuntime"]