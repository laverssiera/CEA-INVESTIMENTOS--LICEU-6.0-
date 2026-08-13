import numpy as np
from typing import List, Dict, Any

class ProjectFinancingRuntime:
    def __init__(self):
        pass

    def calculate_npv(self, rate, cash_flows):
        return sum(cf / (1 + rate)**i for i, cf in enumerate(cash_flows))

    def calculate_irr(self, cash_flows, iterations=1000):
        rate = 0.1
        for _ in range(iterations):
            npv = self.calculate_npv(rate, cash_flows)
            if abs(npv) < 0.01:
                return rate
            # Simple Newton-Raphson-like adjustment
            derivative = sum(-i * cf / (1 + rate)**(i + 1) for i, cf in enumerate(cash_flows))
            if derivative == 0:
                break
            rate = rate - npv / derivative
        return rate

    async def simulate_financing(self, cash_flows: List[float], discount_rate: float) -> Dict[str, Any]:
        """
        Simula o financiamento do projeto calculando NPV, IRR e Payback.
        """
        if not cash_flows:
            return {"error": "Fluxo de caixa vazio"}

        # NPV (VPL)
        npv = self.calculate_npv(discount_rate, cash_flows)
        
        # IRR (TIR)
        irr = self.calculate_irr(cash_flows)
            
        # Payback
        cumulative_cash_flow = np.cumsum(cash_flows)
        payback_period = None
        for i, val in enumerate(cumulative_cash_flow):
            if val >= 0:
                payback_period = i
                break
        
        return {
            "npv": round(float(npv), 2),
            "irr": round(float(irr), 4),
            "payback_period": payback_period if payback_period is not None else "Never",
            "total_return": round(float(sum(cash_flows)), 2),
            "roi": round(float(sum(cash_flows) / abs(cash_flows[0])), 4) if cash_flows[0] != 0 else 0
        }
