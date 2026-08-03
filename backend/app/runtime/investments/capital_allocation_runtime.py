from typing import List, Dict, Any

class CapitalAllocationRuntime:
    def __init__(self):
        pass

    async def suggest_allocation(self, total_capital: float, risk_profile: str) -> Dict[str, Any]:
        """
        Sugere alocação de capital baseada no perfil de risco.
        """
        allocations = []
        
        if risk_profile == "Conservative":
            allocations = [
                {"category": "Fixed Income", "percentage": 0.8, "amount": total_capital * 0.8},
                {"category": "Infrastructure", "percentage": 0.15, "amount": total_capital * 0.15},
                {"category": "Alternative", "percentage": 0.05, "amount": total_capital * 0.05}
            ]
        elif risk_profile == "Moderate":
            allocations = [
                {"category": "Fixed Income", "percentage": 0.5, "amount": total_capital * 0.5},
                {"category": "Infrastructure", "percentage": 0.3, "amount": total_capital * 0.3},
                {"category": "Alternative", "percentage": 0.2, "amount": total_capital * 0.2}
            ]
        else: # Aggressive
            allocations = [
                {"category": "Fixed Income", "percentage": 0.2, "amount": total_capital * 0.2},
                {"category": "Infrastructure", "percentage": 0.4, "amount": total_capital * 0.4},
                {"category": "Alternative", "percentage": 0.4, "amount": total_capital * 0.4}
            ]
            
        return {
            "total_capital": total_capital,
            "risk_profile": risk_profile,
            "allocations": allocations
        }
    
    async def optimize_allocation(self, available_projects: List[Dict[str, Any]], budget: float) -> Dict[str, Any]:
        """
        Otimiza a alocação de capital entre vários projetos baseado em ROI/Risco.
        """
        # Ordenação simples por ROI descendente
        sorted_projects = sorted(available_projects, key=lambda x: x.get("expected_roi", 0), reverse=True)
        
        selected_projects = []
        remaining_budget = budget
        
        for p in sorted_projects:
            cost = p.get("cost", 0)
            if cost <= remaining_budget:
                selected_projects.append(p)
                remaining_budget -= cost
                
        return {
            "budget": budget,
            "total_allocated": budget - remaining_budget,
            "remaining_budget": remaining_budget,
            "selected_projects": selected_projects
        }
