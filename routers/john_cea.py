from fastapi import APIRouter
from typing import Any, Dict
from datetime import datetime, timezone

from backend.app.runtime.investments.continental_capital_allocation_runtime import ContinentalCapitalAllocationRuntime
from backend.app.runtime.investments.continental_investment_runtime import ContinentalInvestmentRuntime
from backend.app.runtime.investments.continental_portfolio_runtime import ContinentalPortfolioRuntime
from backend.app.runtime.investments.continental_project_finance_runtime import ContinentalProjectFinanceRuntime
from backend.app.runtime.investments.continental_risk_runtime import ContinentalRiskRuntime

router = APIRouter(prefix="/api/john/cea", tags=["John CEA"])

continental_investment_runtime = ContinentalInvestmentRuntime()
continental_capital_allocation_runtime = ContinentalCapitalAllocationRuntime()
continental_portfolio_runtime = ContinentalPortfolioRuntime()
continental_project_finance_runtime = ContinentalProjectFinanceRuntime()
continental_risk_runtime = ContinentalRiskRuntime()


@router.get("/health")
async def john_cea_health():
    return {
        "john": "cea",
        "status": "online",
        "module": "finance",
        "timestamp": datetime.now(timezone.utc)
    }


@router.post("/analyze")
async def john_cea_analyze(payload: Dict[str, Any]):
    return {
        "john": "cea",
        "action": "analyze",
        "received": payload,
        "decision": "monitor",
        "confidence": 0.87
    }


@router.post("/allocate")
async def john_cea_allocate(payload: Dict[str, Any]):
    return {
        "john": "cea",
        "action": "allocate",
        "strategy": "balanced",
        "status": "suggested",
        "payload": payload
    }


@router.post("/credit-evaluate")
async def john_cea_credit(payload: Dict[str, Any]):
    return {
        "john": "cea",
        "action": "credit-evaluate",
        "risk": "moderate",
        "approval": True,
        "score": 0.78
    }


@router.post("/fund-project")
async def john_cea_fund(payload: Dict[str, Any]):
    return {
        "john": "cea",
        "action": "fund-project",
        "status": "under-analysis",
        "project": payload.get("project_id")
    }


@router.post("/sync")
async def john_cea_sync(payload: Dict[str, Any]):
    return {
        "john": "cea",
        "sync": True,
        "source": payload.get("source"),
        "timestamp": datetime.now(timezone.utc)
    }


@router.post("/continental/decision")
async def john_cea_continental_decision(payload: Dict[str, Any]):
    project = payload.get("project", {})
    market_signal = payload.get("market_signal", {})
    result = await continental_investment_runtime.john_decide(project, market_signal)
    return {
        "john": "cea",
        "action": "continental-decision",
        "decision_owner": "John",
        "governance": "LICEU",
        "result": result,
        "timestamp": datetime.now(timezone.utc),
    }


@router.post("/continental/allocate")
async def john_cea_continental_allocate(payload: Dict[str, Any]):
    total_capital = float(payload.get("total_capital", 0.0))
    risk_profile = payload.get("risk_profile", "Moderate")
    region = payload.get("region", "Continental")
    result = await continental_capital_allocation_runtime.allocate_for_continent(
        total_capital,
        risk_profile,
        region=region,
    )
    return {
        "john": "cea",
        "action": "continental-allocate",
        "decision_owner": "CEA",
        "governance": "LICEU",
        "result": result,
        "timestamp": datetime.now(timezone.utc),
    }


@router.post("/continental/portfolio")
async def john_cea_continental_portfolio(payload: Dict[str, Any]):
    result = await continental_portfolio_runtime.create_continental_portfolio(
        assets=payload.get("assets", []),
        owner_id=payload.get("owner_id", "john-continental"),
        region=payload.get("region", "Continental"),
    )
    return {
        "john": "cea",
        "action": "continental-portfolio",
        "decision_owner": "CEA",
        "governance": "LICEU",
        "result": result,
        "timestamp": datetime.now(timezone.utc),
    }


@router.post("/continental/finance")
async def john_cea_continental_finance(payload: Dict[str, Any]):
    result = await continental_project_finance_runtime.simulate_project_finance(
        cash_flows=payload.get("cash_flows", []),
        discount_rate=float(payload.get("discount_rate", 0.1)),
    )
    return {
        "john": "cea",
        "action": "continental-finance",
        "owner": "ECONOTECH",
        "governance": "LICEU",
        "result": result,
        "timestamp": datetime.now(timezone.utc),
    }


@router.post("/continental/risk")
async def john_cea_continental_risk(payload: Dict[str, Any]):
    result = await continental_risk_runtime.score_continental_project(
        {
            "location": payload.get("location", "Continental"),
            "complexity": payload.get("complexity", 5),
            "budget": payload.get("budget", 0.0),
        }
    )
    return {
        "john": "cea",
        "action": "continental-risk",
        "decision_owner": "John",
        "governance": "LICEU",
        "result": result,
        "timestamp": datetime.now(timezone.utc),
    }
