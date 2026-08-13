from __future__ import annotations

import numpy as np
from typing import Dict, Any

def calculate_irr(cash_flows: list[float], iterations: int = 100) -> float:
    rate = 0.1
    for _ in range(iterations):
        npv = sum(cf / (1 + rate)**i for i, cf in enumerate(cash_flows))
        if abs(npv) < 0.01:
            return rate
        derivative = sum(-i * cf / (1 + rate)**(i + 1) for i, cf in enumerate(cash_flows))
        if derivative == 0:
            break
        rate = rate - npv / derivative
    return rate

def calculate_satellite_mission_metrics(
    investment_cost: float,
    annual_revenue: float,
    extension_years: int,
    discount_rate: float = 0.10
) -> Dict[str, Any]:
    """
    Calcula as métricas financeiras (NPV, IRR, Payback) para uma missão de recuperação de satélite.
    """
    # Fluxo de caixa: investimento inicial negativo seguido de retornos anuais
    cash_flows = [-investment_cost] + [annual_revenue] * extension_years
    
    # NPV (VPL)
    npv = sum(cf / (1 + discount_rate)**i for i, cf in enumerate(cash_flows))
    
    # IRR (TIR)
    irr = calculate_irr(cash_flows)

    # Payback
    payback = investment_cost / annual_revenue if annual_revenue > 0 else float('inf')
    
    # ROI
    total_return = (annual_revenue * extension_years)
    roi = (total_return - investment_cost) / investment_cost if investment_cost > 0 else 0
    
    return {
        "npv": round(float(npv), 2),
        "irr": round(float(irr), 4),
        "payback": round(float(payback), 2),
        "roi": round(float(roi), 4),
        "extension_years": extension_years,
        "approved": npv > 0 and irr > discount_rate
    }
