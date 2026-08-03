from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from app.events import event_bus
from app.db.session import get_db
from app.runtime.investments.risk_scoring_runtime import RiskScoringRuntime
from app.runtime.investments.portfolio_runtime import PortfolioRuntime
from app.runtime.investments.infrastructure_fund_runtime import InfrastructureFundRuntime
from app.runtime.investments.project_financing_runtime import ProjectFinancingRuntime
from app.runtime.investments.capital_allocation_runtime import CapitalAllocationRuntime
from app.runtime.investments.sovereign_investment_runtime import SovereignInvestmentRuntime
from app.runtime.investments.global_portfolio_runtime import GlobalPortfolioRuntime

router = APIRouter(prefix="/investments", tags=["Investments - CEA Layer"])

# --- Schemas ---

class ProjectScoreRequest(BaseModel):
    name: str
    location: str
    complexity: int
    budget: float
    cash_flows: Optional[List[float]] = None
    discount_rate: Optional[float] = 0.1

class PortfolioCreateRequest(BaseModel):
    owner_id: str
    assets: List[Dict[str, Any]]


class GlobalPortfolioCreateRequest(BaseModel):
    owner_id: str
    assets: List[Dict[str, Any]]
    region: Optional[str] = "global"

class FundSimulateRequest(BaseModel):
    fund_name: str
    period_months: int
    initial_capital: float

# --- Runtimes (Singleton components could be used here) ---
risk_runtime = RiskScoringRuntime()
portfolio_runtime = PortfolioRuntime()
fund_runtime = InfrastructureFundRuntime()
financing_runtime = ProjectFinancingRuntime()
allocation_runtime = CapitalAllocationRuntime()
sovereign_runtime = SovereignInvestmentRuntime()
global_portfolio_runtime = GlobalPortfolioRuntime()

# --- Endpoints ---

@router.post("/project/score")
async def project_score(request: ProjectScoreRequest):
    """
    Calcula o score de risco e viabilidade financeira de um projeto seguindo a trilha:
    Base Marciana -> Risco -> Fluxo de Caixa -> Investimento -> Payback -> IRR -> NPV
    """
    # 1. Base (Project Data)
    base_info = {
        "name": request.name,
        "location": request.location,
        "budget": request.budget
    }

    # 2. Risco
    risk_result = await risk_runtime.calculate_score({
        "location": request.location,
        "complexity": request.complexity,
        "budget": request.budget
    })
    
    # 3/4/5/6/7. Fluxo de Caixa, Investimento, Payback, IRR, NPV
    financing_result = {}
    if request.cash_flows:
        # Assume o investimento inicial é o primeiro item do fluxo de caixa se for negativo, 
        # ou o budget se não houver fluxo inicial.
        financing_result = await financing_runtime.simulate_financing(
            request.cash_flows, 
            request.discount_rate
        )
    
    return {
        "flow": {
            "base": base_info,
            "risk": risk_result,
            "cash_flow": request.cash_flows,
            "investment": request.budget,
            "metrics": financing_result
        },
        "status": "calculated",
        "timestamp": "2026-06-06T12:00:00Z"
    }

@router.post("/portfolio/create")
async def portfolio_create(request: PortfolioCreateRequest):
    """
    Cria um novo portfólio de investimentos.
    """
    result = await portfolio_runtime.create_portfolio(request.assets, request.owner_id)
    return result


@router.post("/portfolio/global/create")
async def global_portfolio_create(request: GlobalPortfolioCreateRequest):
    """
    Cria um novo portfólio global (multi-região).
    """
    result = await global_portfolio_runtime.create_global_portfolio(
        assets=request.assets,
        owner_id=request.owner_id,
        region=request.region or "global",
    )
    return result


@router.get("/portfolio/global/state")
async def get_global_portfolio_state():
    """
    Retorna a visão agregada dos portfólios globais.
    """
    return await global_portfolio_runtime.get_global_state()


@router.get("/portfolio/global/{portfolio_id}")
async def global_portfolio_state(portfolio_id: str):
    """
    Retorna o estado de um portfólio global por ID.
    """
    return await global_portfolio_runtime.get_portfolio_state(portfolio_id)

@router.post("/fund/simulate")
async def fund_simulate(request: FundSimulateRequest):
    """
    Simula o crescimento de um fundo de infraestrutura.
    """
    result = await fund_runtime.simulate_fund_performance(
        request.fund_name, 
        request.period_months, 
        request.initial_capital
    )
    return result

@router.get("/state")
async def get_investments_state():
    """
    Retorna o estado global da camada de investimentos.
    """
    return {
        "status": "operational",
        "active_runtimes": [
            "portfolio_runtime",
            "global_portfolio_runtime",
            "project_financing_runtime",
            "infrastructure_fund_runtime",
            "risk_scoring_runtime",
            "capital_allocation_runtime",
            "sovereign_investment_runtime"
        ],
        "metrics": {
            "total_portfolios_managed": len(portfolio_runtime.portfolios),
            "total_global_portfolios_managed": len(global_portfolio_runtime.portfolios),
            "engine_version": "LICEU-6.0-INVEST"
        }
    }


@router.get("/network/state")
async def get_investment_network_state():
    """
    Retorna o estado atual da rede de investimentos alimentada por eventos.
    """
    network = event_bus.investment_network_summary()
    return {
        "status": "operational",
        "network": network,
        "active_runtimes": [
            "investment_network_runtime",
            "event_bus",
        ],
    }

# Additional helper endpoints for other runtimes

@router.post("/allocation/suggest")
async def suggest_allocation(total_capital: float, risk_profile: str):
    return await allocation_runtime.suggest_allocation(total_capital, risk_profile)

@router.post("/sovereign/analyze")
async def analyze_sovereign(region: str, investment_type: str, amount: float):
    return await sovereign_runtime.analyze_sovereign_opportunity(region, investment_type, amount)
