class InterplanetaryLiquidityEngine:
    def __init__(self):
        self.pools = {}


    def create_pool(self, name, reserve):
        self.pools[name] = {
            "reserve": reserve,
            "stability_index": 1.0
        }


    def rebalance(self, pool_name, delta):
        self.pools[pool_name]["reserve"] += delta


        return self.pools[pool_name]
