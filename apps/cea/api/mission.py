from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from apps.cea.modules.mission.service import calculate_satellite_mission_metrics

router = APIRouter(prefix="/mission", tags=["Mission Analysis"])

class SatelliteAnalysisInput(BaseModel):
    satellite_type: str = Field(description="Ex: Satélite GEO")
    issue_status: str = Field(description="Ex: Combustível baixo, Desvio orbital")
    investment_cost: float = Field(gt=0)
    annual_revenue: float = Field(gt=0)
    extension_years: int = Field(gt=0)

@router.post("/satellite-recovery")
def satellite_recovery_analysis(payload: SatelliteAnalysisInput) -> dict:
    """
    Realiza a análise financeira para uma missão de recuperação orbital.
    """
    metrics = calculate_satellite_mission_metrics(
        investment_cost=payload.investment_cost,
        annual_revenue=payload.annual_revenue,
        extension_years=payload.extension_years
    )
    
    status_message = "Missão aprovada" if metrics["approved"] else "Missão rejeitada (ROI insuficiente)"
    
    return {
        "scenario": {
            "satellite": payload.satellite_type,
            "issues": payload.issue_status
        },
        "financial_analysis": {
            "npv": metrics["npv"],
            "irr": metrics["irr"],
            "payback_years": metrics["payback"]
        },
        "expected_outcome": {
            "life_extension": f"+{metrics['extension_years']} anos de vida útil",
            "roi": f"ROI {'positivo' if metrics['roi'] > 0 else 'negativo'} ({metrics['roi']:.2%})",
            "status": status_message
        }
    }
