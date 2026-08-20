from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict
from uuid import uuid4

from app.events import event_bus
from app.db.session import get_db
from app.db.session import SessionLocal
from app.runtime.investments.risk_scoring_runtime import RiskScoringRuntime
from app.runtime.investments.portfolio_runtime import PortfolioRuntime
from app.runtime.investments.infrastructure_fund_runtime import InfrastructureFundRuntime
from app.runtime.investments.project_financing_runtime import ProjectFinancingRuntime
from app.runtime.investments.capital_allocation_runtime import CapitalAllocationRuntime
from app.runtime.investments.earth_investment_runtime import EarthInvestmentRuntime
from app.runtime.investments.earth_portfolio_runtime import EarthPortfolioRuntime
from app.runtime.investments.earth_project_score_runtime import EarthProjectScoreRuntime
from app.runtime.investments.sovereign_investment_runtime import SovereignInvestmentRuntime
from app.runtime.investments.global_portfolio_runtime import GlobalPortfolioRuntime
from app.runtime.investments.civilization_investment_runtime import CivilizationInvestmentRuntime
from app.runtime.investments.civilization_project_finance_runtime import CivilizationProjectFinanceRuntime
from app.runtime.investments.continental_investment_runtime import ContinentalInvestmentRuntime
from app.runtime.investments.continental_capital_allocation_runtime import ContinentalCapitalAllocationRuntime
from app.runtime.investments.continental_portfolio_runtime import ContinentalPortfolioRuntime
from app.runtime.investments.continental_project_finance_runtime import ContinentalProjectFinanceRuntime
from app.runtime.investments.continental_risk_runtime import ContinentalRiskRuntime
from app.runtime.investments.planetary_financial_exposure_runtime import PlanetaryFinancialExposureRuntime
from app.runtime.investments.continental_financial_exposure_runtime import ContinentalFinancialExposureRuntime

router = APIRouter(prefix="/investments", tags=["Investments - CEA Layer"])

# --- Schemas ---

class ProjectScoreRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: Optional[str] = None
    location: Optional[str] = None
    complexity: Optional[int] = 3
    budget: Optional[float] = None
    project_type: Optional[str] = None
    capex: Optional[float] = None
    opex_yearly: Optional[float] = None
    annual_revenue: Optional[float] = None
    strategic_importance: Optional[float] = None
    cash_flows: Optional[List[float]] = None
    discount_rate: Optional[float] = 0.1
    horizon_years: Optional[int] = 10
    physical_event: Optional[Dict[str, Any]] = None
    trace_id: Optional[str] = None

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


class EarthPortfolioRequest(BaseModel):
    projects: List[ProjectScoreRequest]
    available_capital: Optional[float] = None

# --- Runtimes (Singleton components could be used here) ---
risk_runtime = RiskScoringRuntime()
portfolio_runtime = PortfolioRuntime()
fund_runtime = InfrastructureFundRuntime()
financing_runtime = ProjectFinancingRuntime()
civilization_investment_runtime = CivilizationInvestmentRuntime()
civilization_project_finance_runtime = CivilizationProjectFinanceRuntime()
allocation_runtime = CapitalAllocationRuntime()
sovereign_runtime = SovereignInvestmentRuntime()
global_portfolio_runtime = GlobalPortfolioRuntime()
continental_investment_runtime = ContinentalInvestmentRuntime()
continental_capital_allocation_runtime = ContinentalCapitalAllocationRuntime()
continental_portfolio_runtime = ContinentalPortfolioRuntime()
continental_project_finance_runtime = ContinentalProjectFinanceRuntime()
continental_risk_runtime = ContinentalRiskRuntime()
earth_investment_runtime = EarthInvestmentRuntime()
earth_project_score_runtime = EarthProjectScoreRuntime(earth_investment_runtime)
earth_portfolio_runtime = EarthPortfolioRuntime(earth_project_score_runtime)
planetary_financial_exposure_runtime = PlanetaryFinancialExposureRuntime(earth_investment_runtime)

# --- Endpoints ---

@router.post("/project/score")
async def project_score(request: ProjectScoreRequest):
    """
    Calcula a leitura economica completa de um projeto seguindo a trilha:
    risco -> CAPEX -> OPEX -> cash flow -> NPV -> IRR -> payback -> ROI -> impacto estrategico
    """
    analysis = earth_project_score_runtime.score_project(request.model_dump())
    trace_id = request.trace_id or str(uuid4())
    analysis["trace_id"] = trace_id

    return {
        "trace_id": trace_id,
        "project": {
            "name": request.name,
            "location": request.location,
            "project_type": request.project_type or request.name,
            "budget": request.budget,
        },
        "decision": analysis["decision"],
        "flow": {
            "trace_id": trace_id,
            "base": {
                "name": request.name,
                "location": request.location,
                "budget": request.budget,
            },
            "risk": analysis["risk"],
            "cash_flow": analysis["cash_flow"],
            "investment": analysis["capex"],
            "metrics": {
                "npv": analysis["npv"],
                "irr": analysis["irr"],
                "payback": analysis["payback"],
                "roi": analysis["roi"],
                "decision_score": analysis["decision_score"],
            },
            "financial_exposure": analysis["financial_exposure"],
            "economic_impact": analysis["economic_impact"],
            "impacto_estrategico": analysis["impacto_estrategico"],
        },
        "analysis": analysis,
        "status": "calculated",
        "timestamp": "2026-06-06T12:00:00Z"
    }


@router.post("/earth/project/score")
async def earth_project_score(request: ProjectScoreRequest):
    """
    Score completo para decisao de capital em um projeto terrestre.
    """
    analysis = earth_project_score_runtime.score_project(request.model_dump())
    analysis["trace_id"] = request.trace_id or str(uuid4())
    return analysis


@router.post("/civilization/project/score")
async def civilization_project_score(request: Dict[str, Any] = Body(...)):
    """
    Score completo para decisao de capital em um projeto de infraestrutura soberana/ondas.
    """
    payload = dict(request or {})
    trace_id = str(payload.get("trace_id") or uuid4())
    normalized_name = payload.get("name") or payload.get("project_name") or "project"
    budget_value = (
        payload.get("budget")
        or payload.get("capital_expenditure")
        or payload.get("capex")
        or 0.0
    )
    capex_value = payload.get("capex") or payload.get("capital_expenditure") or budget_value or 0.0
    opex_value = payload.get("opex_yearly") or payload.get("annual_opex") or 0.0
    revenue_value = payload.get("annual_revenue") or payload.get("revenue") or 0.0
    discount_value = payload.get("discount_rate")
    if discount_value is None:
        discount_value = payload.get("discount") or 0.1
    horizon_value = payload.get("horizon_years")
    if horizon_value is None:
        horizon_value = payload.get("years") or 10

    analysis = civilization_investment_runtime.evaluate_project(
        project_type=payload.get("project_type") or normalized_name,
        capex=float(capex_value),
        opex_yearly=float(opex_value),
        annual_revenue=float(revenue_value),
        project_name=normalized_name,
        location=payload.get("location"),
        cash_flows=payload.get("cash_flows"),
        strategic_importance=payload.get("strategic_importance"),
        discount_rate=float(discount_value),
        horizon_years=int(horizon_value),
        physical_event=payload.get("physical_event"),
    )
    analysis["trace_id"] = trace_id

    return {
        "trace_id": trace_id,
        "project": {
            "name": normalized_name,
            "location": payload.get("location"),
            "project_type": payload.get("project_type") or normalized_name,
            "budget": float(budget_value),
        },
        "decision": analysis["decision"],
        "flow": {
            "trace_id": trace_id,
            "base": {
                "name": normalized_name,
                "location": payload.get("location"),
                "budget": float(budget_value),
            },
            "risk": analysis["risk"],
            "cash_flow": analysis["cash_flow"],
            "investment": analysis["capex"],
            "metrics": {
                "npv": analysis["npv"],
                "irr": analysis["irr"],
                "payback": analysis["payback"],
                "roi": analysis["roi"],
                "decision_score": analysis["decision_score"],
            },
            "financial_exposure": analysis["financial_exposure"],
            "economic_impact": analysis["economic_impact"],
            "impacto_estrategico": analysis["impacto_estrategico"],
        },
        "analysis": analysis,
        "status": "calculated",
        "timestamp": "2026-06-06T12:00:00Z",
    }


@router.post("/earth/projects/rank")
async def earth_projects_rank(request: EarthPortfolioRequest):
    """
    Ranqueia varios projetos por prioridade de capital.
    """
    return earth_project_score_runtime.score_projects([project.model_dump() for project in request.projects])


@router.get("/earth/projects/examples")
async def earth_projects_examples():
    """
    Retorna o conjunto padrão de projetos exemplo com métricas completas.
    """
    return earth_project_score_runtime.example_projects()


@router.post("/earth/portfolio/build")
async def earth_portfolio_build(request: EarthPortfolioRequest):
    """
    Consolida projetos em um portifolio com decisao de capital.
    """
    return earth_portfolio_runtime.build_portfolio(
        [project.model_dump() for project in request.projects],
        request.available_capital,
    )

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


@router.post("/civilization/portfolio/create")
async def civilization_portfolio_create(request: GlobalPortfolioCreateRequest):
    """
    Alias compatível para criação de portfólio global da Onda 10.
    """
    return await global_portfolio_create(request)


@router.get("/portfolio/global/state")
async def get_global_portfolio_state():
    """
    Retorna a visão agregada dos portfólios globais.
    """
    return await global_portfolio_runtime.get_global_state()


@router.get("/portfolio/global/monitor")
async def get_global_portfolio_monitoring_state(
    region: str | None = None,
    country: str | None = None,
    owner_id: str | None = None,
    segment: str | None = None,
    min_value: float | None = None,
    max_value: float | None = None,
):
    """
    Retorna acompanhamento consolidado de mercados, governos, infraestrutura e fundos.
    """
    return await global_portfolio_runtime.get_global_monitoring_state(
        region=region,
        country=country,
        owner_id=owner_id,
        segment=segment,
        min_value=min_value,
        max_value=max_value,
    )


@router.get("/civilization/portfolio/state")
async def get_civilization_portfolio_state():
    """
    Alias compatível para visão agregada do portfólio global da Onda 10.
    """
    return await get_global_portfolio_state()


@router.get("/civilization/portfolio/monitor")
async def get_civilization_portfolio_monitoring_state(
    region: str | None = None,
    country: str | None = None,
    owner_id: str | None = None,
    segment: str | None = None,
    min_value: float | None = None,
    max_value: float | None = None,
):
    """
    Alias compatível para acompanhamento consolidado do portfólio global da Onda 10.
    """
    return await get_global_portfolio_monitoring_state(
        region=region,
        country=country,
        owner_id=owner_id,
        segment=segment,
        min_value=min_value,
        max_value=max_value,
    )


@router.get("/portfolio/global/{portfolio_id}")
async def global_portfolio_state(portfolio_id: str):
    """
    Retorna o estado de um portfólio global por ID.
    """
    result = await global_portfolio_runtime.get_portfolio_state(portfolio_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/civilization/portfolio/{portfolio_id}")
async def civilization_portfolio_state(portfolio_id: str):
    """
    Alias compatível para consulta de portfólio global da Onda 10.
    """
    return await global_portfolio_state(portfolio_id)

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


@router.post("/civilization/risk/score")
async def civilization_risk_score(request: ProjectScoreRequest):
    """
    Alias compatível para cálculo de risco da Onda 10.
    """
    return await risk_runtime.calculate_score(
        {
            "location": request.location,
            "complexity": request.complexity,
            "budget": request.budget,
        }
    )


@router.post("/civilization/capital/suggest")
async def civilization_capital_suggest(total_capital: float, risk_profile: str):
    """
    Alias compatível para sugestão de alocação da Onda 10.
    """
    return await suggest_allocation(total_capital, risk_profile)


@router.post("/civilization/project/finance")
async def civilization_project_finance(cash_flows: List[float], discount_rate: float):
    """Alias compatível para simulação de financiamento de projeto da Onda 42."""
    return await civilization_project_finance_runtime.simulate_financing(cash_flows, discount_rate)

@router.post("/sovereign/analyze")
async def analyze_sovereign(region: str, investment_type: str, amount: float):
    return await sovereign_runtime.analyze_sovereign_opportunity(region, investment_type, amount)


@router.post("/civilization/investment/analyze")
async def civilization_investment_analyze(region: str, investment_type: str, amount: float):
    """
    Alias compatível para análise soberana de investimento da Onda 10.
    """
    return await analyze_sovereign(region, investment_type, amount)


@router.post("/continental/john/decide")
async def continental_john_decide(project: Dict[str, Any], market_signal: Dict[str, Any]):
    """JOHN decide a direção estratégica de um plano continental."""
    return await continental_investment_runtime.john_decide(project, market_signal)


@router.post("/continental/capital/allocation")
async def continental_capital_allocation(total_capital: float, risk_profile: str = "Moderate", region: str = "Continental"):
    """CEA decide a alocação financeira no escopo continental."""
    return await continental_capital_allocation_runtime.allocate_for_continent(
        total_capital,
        risk_profile,
        region=region,
    )


@router.post("/continental/portfolio/create")
async def continental_portfolio_create(request: GlobalPortfolioCreateRequest):
    """Cria um portfólio continental com governança LICEU."""
    return await continental_portfolio_runtime.create_continental_portfolio(
        assets=request.assets,
        owner_id=request.owner_id,
        region=request.region or "Continental",
    )


@router.get("/continental/portfolio/state")
async def continental_portfolio_state_summary():
    """Retorna o estado agregado do portfólio continental."""
    return await continental_portfolio_runtime.get_state()


@router.post("/continental/project/finance")
async def continental_project_finance(cash_flows: List[float], discount_rate: float):
    """ECONOTECH calcula o impacto financeiro do projeto continental."""
    return await continental_project_finance_runtime.simulate_project_finance(cash_flows, discount_rate)


@router.post("/continental/risk/score")
async def continental_risk_score(request: ProjectScoreRequest):
    """JOHN avalia o score de risco do projeto continental."""
    return await continental_risk_runtime.score_continental_project(
        {
            "location": request.location,
            "complexity": request.complexity,
            "budget": request.budget,
        }
    )


@router.post("/planetary/financial-exposure")
async def planetary_financial_exposure(
    request: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
):
    """WAVE 83 - CEA: exposicao financeira planetaria consumindo o resultado real da W82 (ECONOTECH),
    preservando a cadeia causal ate o financial_exposure_id."""
    payload = dict(request or {})
    project = payload.get("project") or payload
    w82_result = payload.get("w82_result")
    from app.services.immutable_runtime_service import ImmutableFinancialRuntime

    return planetary_financial_exposure_runtime.run_wave(
        project,
        w82_result,
        immutable_runtime=ImmutableFinancialRuntime(db),
    )


@router.post("/continental/financial-exposure")
async def continental_financial_exposure(
    request: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
):
    """WAVE 92: lê W89-W91 do Event Store canônico e grava exposição continental."""
    return ContinentalFinancialExposureRuntime(db, SessionLocal).run_wave(
        dict(request or {})
    )
