class UnderwritingAGI:

    def analyze(
        self,
        liquidity,
        supplier_score,
        legal_risk,
        operational_score
    ):

        risk = (
            liquidity * 0.2 +
            supplier_score * 0.3 +
            legal_risk * 0.3 +
            operational_score * 0.2
        )

        if risk > 80:
            return {
                "status": "rejected",
                "reason": "systemic_risk"
            }

        return {
            "status": "approved",
            "credit_limit": 1000000
        }

agi = UnderwritingAGI()
