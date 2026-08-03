from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
from uuid import UUID, uuid4
from .isolde_mars import IsoldeMarsFinance

router = APIRouter(prefix="/science/funding", tags=["Scientific Capital"])

class FundingRequest(BaseModel):
    project_name: str
    research_area: str
    requested_amount: float
    impact_description: str

class FundingResponse(BaseModel):
    funding_id: UUID
    status: str
    release_schedule: List[dict]

@router.post("/create", response_model=FundingResponse)
async def create_scientific_funding(request: FundingRequest):
    """
    Inicia processo de funding para capital científico.
    """
    return FundingResponse(
        funding_id=uuid4(),
        status="AWAITING_COMPLIANCE",
        release_schedule=[{"milestone": "Initiation", "amount": request.requested_amount * 0.2}]
    )

@router.get("/report/{funding_id}")
async def get_funding_report(funding_id: UUID):
    """
    Retorna status e impacto do financiamento.
    """
    return {"funding_id": funding_id, "status": "active", "scientific_impact_score": 0.95}

@router.get("/isolde-mars/simulate")
async def simulate_isolde_mars(years: int = 15, discount_rate: float = 0.12):
    """
    Calcula CAPEX, OPEX, Payback, NPV e IRR para o Case Maximum: ISOLDE-MARS.
    Focado em Pesquisa de núcleos exóticos, descoberta de materiais e blindagem radiológica.
    """
    finance = IsoldeMarsFinance()
    results = finance.calculate_metrics(years=years, discount_rate=discount_rate)
    return results
