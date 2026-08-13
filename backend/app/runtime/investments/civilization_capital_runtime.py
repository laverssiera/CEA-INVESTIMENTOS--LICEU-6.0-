"""Compatibility runtime for the Capital Global allocation flow."""

from .capital_allocation_runtime import CapitalAllocationRuntime


class CivilizationCapitalRuntime(CapitalAllocationRuntime):
    pass


__all__ = ["CivilizationCapitalRuntime"]