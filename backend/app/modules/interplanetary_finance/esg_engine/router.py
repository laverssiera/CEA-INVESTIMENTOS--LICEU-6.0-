from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter(prefix="/esg/civilizational", tags=["Interplanetary ESG"])

class ImpactAnalysisRequest(BaseModel):
    project_id: str
    energy_consumption_kwh: float
    habitat_type: str # 'OCEANIC', 'ORBITAL', 'TERRESTRIAL_EXTREME'
    human_capacity: int
    infrastructure_utility_index: float # 0.0 to 1.0

class CivilizationalScore(BaseModel):
    project_id: str
    co2_impact_tons: float
    sustainability_rating: str
    civilizational_contribution: float
    ethical_clearance: bool

@router.post("/analyze", response_model=CivilizationalScore)
async def analyze_civilizational_impact(request: ImpactAnalysisRequest):
    """
    Calcula o impacto civilizacional e ambiental de projetos extremos.
    """
    # Lógica de cálculo de CO2 baseada no habitat
    multipliers = {
        "ORBITAL": 0.05, # Energia solar espacial é limpa
        "OCEANIC": 0.8,
        "TERRESTRIAL_EXTREME": 1.2
    }
    
    co2_impact = request.energy_consumption_kwh * multipliers.get(request.habitat_type, 1.0) * 0.0001
    
    # Cálculo de contribuição civilizacional (exemplo simplificado)
    contribution = (request.human_capacity * 0.1) + (request.infrastructure_utility_index * 10)
    
    return CivilizationalScore(
        project_id=request.project_id,
        co2_impact_tons=round(co2_impact, 4),
        sustainability_rating="A+" if co2_impact < 10 else "B",
        civilizational_contribution=round(contribution, 2),
        ethical_clearance=True if contribution > 5 else False
    )
