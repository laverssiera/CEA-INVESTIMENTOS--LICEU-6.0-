class TreasuryBrain:

    def rebalance(self, cash, liabilities):

        ratio = cash / liabilities

        if ratio < 1:
            return {
                "action": "raise_liquidity"
            }

        return {
            "action": "stable"
        }

brain = TreasuryBrain()
