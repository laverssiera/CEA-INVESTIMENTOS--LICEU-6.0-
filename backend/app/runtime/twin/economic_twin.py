import random

class EconomicTwin:

    def simulate_crisis(self):

        inflation = random.uniform(4, 22)
        liquidity = random.uniform(0, 100)
        default_rate = random.uniform(0, 40)

        return {
            "inflation": inflation,
            "liquidity": liquidity,
            "default_rate": default_rate,
            "systemic_alert": default_rate > 25
        }

twin = EconomicTwin()
