from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/treasury/ethical", tags=["Ethical Treasury"])

class SystemicRiskStress(BaseModel):
    habitat_exposure: List[str]
    liquidity_buffer_ratio: float
    bubble_detection_index: float

@router.post("/stability-check")
async def treasury_stability_check(request: SystemicRiskStress):
    """
    IA Financeira Ética para detecção de bolhas e proteção de caixa sistêmico.
    """
    is_stable = True
    alert_level = "LOW"
    
    if request.bubble_detection_index > 0.7:
        is_stable = False
        alert_level = "CRITICAL"
    
    return {
        "status": "STABLE" if is_stable else "ACTION_REQUIRED",
        "alert_level": alert_level,
        "recommended_action": "Freeze speculatives, boost scientific liquidity" if not is_stable else "Maintain flow"
    }
