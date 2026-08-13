from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from apps.cea.core.database import get_db
from apps.cea.modules.cashflow.service import get_cashflow
from apps.cea.modules.investment.service import create_manual_investment
from apps.cea.modules.roi.service import calculate_payback, calculate_roi

router = APIRouter(prefix="/finance", tags=["Finance"])


class RoiInput(BaseModel):
    investment: float = Field(gt=0)
    return_value: float


class PaybackInput(BaseModel):
    investment: float = Field(gt=0)
    monthly_return: float = Field(gt=0)


class InvestInput(BaseModel):
    entity_id: str
    amount: float = Field(gt=0)
    expected_roi: float = Field(ge=-1, le=10)


@router.post("/roi")
def roi(payload: RoiInput) -> dict:
    try:
        return {"roi": calculate_roi(payload.investment, payload.return_value)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/payback")
def payback(payload: PaybackInput) -> dict:
    try:
        return {"payback_months": calculate_payback(payload.investment, payload.monthly_return)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/cashflow")
def cashflow(db: Session = Depends(get_db)) -> dict:
    return get_cashflow(db)


@router.post("/invest")
def invest(payload: InvestInput, db: Session = Depends(get_db)) -> dict:
    item = create_manual_investment(
        db,
        entity_id=payload.entity_id,
        amount=payload.amount,
        expected_roi=payload.expected_roi,
    )
    return {
        "id": item.id,
        "entity_id": item.entity_id,
        "amount": float(item.amount),
        "expected_roi": item.expected_roi,
        "status": item.status,
    }
