from typing import List, Dict, Any
import uuid
from datetime import datetime

class PortfolioRuntime:
    def __init__(self):
        self.portfolios = {}

    async def create_portfolio(self, assets: List[Dict[str, Any]], owner_id: str) -> Dict[str, Any]:
        """
        Cria um novo portfólio de investimentos.
        """
        portfolio_id = str(uuid.uuid4())
        total_value = sum(asset.get("value", 0) for asset in assets)
        
        portfolio = {
            "portfolio_id": portfolio_id,
            "owner_id": owner_id,
            "assets": assets,
            "total_initial_value": total_value,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        self.portfolios[portfolio_id] = portfolio
        return portfolio

    async def get_portfolio_state(self, portfolio_id: str) -> Dict[str, Any]:
        return self.portfolios.get(portfolio_id, {"error": "Portfolio not found"})
