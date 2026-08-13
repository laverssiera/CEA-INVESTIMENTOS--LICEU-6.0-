from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.modules.decision_engine.engine import auto_allocation, ml_alerts, pre_credit_approval, rebalance_portfolio

router = APIRouter(tags=["Decision Engine"])


class AutoAllocationInput(BaseModel):
    amount: float = Field(gt=0)
    profile: str = "moderado"
    risk_level: float = Field(default=55, ge=0, le=100)


class PreCreditInput(BaseModel):
    score: float = Field(default=700, ge=0, le=1000)
    ltv: float = Field(default=0.65, ge=0, le=1)
    risk_flag: bool = False


class RebalanceInput(BaseModel):
    exposure_by_asset: dict[str, float]


@router.post("/ml/allocation/auto")
def allocation_auto(payload: AutoAllocationInput) -> dict[str, Any]:
    return auto_allocation(payload.amount, payload.profile, payload.risk_level)


@router.post("/ml/credit/pre-approval")
def credit_pre_approval(payload: PreCreditInput) -> dict[str, Any]:
    return pre_credit_approval(payload.score, payload.ltv, payload.risk_flag)


@router.post("/ml/rebalance")
def rebalance(payload: RebalanceInput) -> dict[str, Any]:
    return rebalance_portfolio(payload.exposure_by_asset)


@router.get("/ml/alerts")
def alerts() -> dict[str, Any]:
    return {"items": ml_alerts()}
