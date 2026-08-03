class ComplianceRuntime:

    def aml_check(self, amount):

        if amount > 1000000:
            return {
                "flagged": True,
                "reason": "AML_THRESHOLD"
            }

        return {
            "flagged": False
        }

runtime = ComplianceRuntime()
