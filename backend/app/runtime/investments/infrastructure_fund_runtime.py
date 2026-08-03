from typing import Dict, Any, List
import random

class InfrastructureFundRuntime:
    def __init__(self):
        pass

    async def simulate_fund_performance(self, fund_name: str, period_months: int, initial_capital: float) -> Dict[str, Any]:
        """
        Simula a performance de um fundo de infraestrutura.
        """
        performance_history = []
        current_capital = initial_capital
        
        for month in range(1, period_months + 1):
            # Simulação de rendimento infra: estável mas sujeito a riscos regulatórios/clima
            monthly_yield = random.uniform(0.005, 0.015) # 0.5% a 1.5% ao mês
            current_capital *= (1 + monthly_yield)
            performance_history.append({
                "month": month,
                "capital": round(current_capital, 2),
                "yield": round(monthly_yield, 4)
            })
            
        total_profit = current_capital - initial_capital
        
        return {
            "fund_name": fund_name,
            "period": f"{period_months} months",
            "initial_capital": initial_capital,
            "final_capital": round(current_capital, 2),
            "total_profit": round(total_profit, 2),
            "total_roi": round(total_profit / initial_capital, 4),
            "history": performance_history
        }
