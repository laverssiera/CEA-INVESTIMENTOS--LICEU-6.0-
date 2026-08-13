class CausalRuntime:

    def evaluate(
        self,
        treasury_stress,
        supplier_default,
        logistics_delay
    ):

        impact = (
            treasury_stress * 0.5 +
            supplier_default * 0.3 +
            logistics_delay * 0.2
        )

        if impact > 70:
            return "SYSTEMIC_COLLAPSE_RISK"

        return "STABLE"

runtime = CausalRuntime()
