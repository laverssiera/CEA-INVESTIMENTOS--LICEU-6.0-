from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from uuid import UUID, uuid4
from .models import MissionAsset, MissionPortfolio, MissionPortfolioStatus

router = APIRouter(prefix="/interplanetary/portfolio", tags=["Mission Finance Portfolio"])

# Mock storage for demonstration (should be replaced by DB in production)
MOCK_PORTFOLIOS: Dict[str, MissionPortfolio] = {
    "cea_master": MissionPortfolio(
        owner_id="cea_master",
        assets=[
            MissionAsset(
                name="Deep Sea Laboratory Alpha",
                category="oceanic",
                valuation=120000000.0,
                funding_status="OPERATIONAL",
                impact_civilizational_score=0.92
            ),
            MissionAsset(
                name="Lunar Orbital Hub",
                category="orbital",
                valuation=450000000.0,
                funding_status="PARTIALLY_FUNDED",
                impact_civilizational_score=0.98
            ),
            MissionAsset(
                name="Fusion Energy R&D",
                category="scientific",
                valuation=300000000.0,
                funding_status="AWAITING_FUNDS",
                impact_civilizational_score=0.99
            )
        ]
    )
}

@router.get("/", response_model=MissionPortfolio)
async def get_portfolio(owner_id: str = "cea_master"):
    """
    Retorna o portfólio de missões para um determinado proprietário.
    """
    if owner_id not in MOCK_PORTFOLIOS:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return MOCK_PORTFOLIOS[owner_id]

@router.get("/status", response_model=MissionPortfolioStatus)
async def get_portfolio_status(owner_id: str = "cea_master"):
    """
    Retorna estatísticas consolidadas do portfólio de missões.
    """
    if owner_id not in MOCK_PORTFOLIOS:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    portfolio = MOCK_PORTFOLIOS[owner_id]
    total_val = sum(a.valuation for a in portfolio.assets)
    avg_impact = sum(a.impact_civilizational_score for a in portfolio.assets) / len(portfolio.assets) if portfolio.assets else 0
    
    allocation = {}
    for a in portfolio.assets:
        allocation[a.category] = allocation.get(a.category, 0) + a.valuation
    
    # Normalizar alocação em %
    if total_val > 0:
        for cat in allocation:
            allocation[cat] = round((allocation[cat] / total_val) * 100, 2)

    return MissionPortfolioStatus(
        total_valuation=total_val,
        active_missions_count=len(portfolio.assets),
        average_impact_score=round(avg_impact, 4),
        allocation_by_category=allocation
    )

@router.post("/add-mission", response_model=MissionAsset)
async def add_mission_to_portfolio(mission: MissionAsset, owner_id: str = "cea_master"):
    """
    Adiciona uma nova missão (ativo civilizacional) ao portfólio.
    """
    if owner_id not in MOCK_PORTFOLIOS:
        MOCK_PORTFOLIOS[owner_id] = MissionPortfolio(owner_id=owner_id)
    
    MOCK_PORTFOLIOS[owner_id].assets.append(mission)
    return mission
