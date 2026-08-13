from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.modules.documents.service import (
    generate_committee_minutes,
    generate_financing_term,
    generate_investment_contract,
    latest_documents,
)

router = APIRouter(prefix="/api/documents", tags=["Documents"])


class InvestmentContractInput(BaseModel):
    investor: str
    amount: float


class FinancingTermInput(BaseModel):
    client: str
    amount: float


class CommitteeMinutesInput(BaseModel):
    committee: str
    decision: str


@router.post("/investment-contract")
def investment_contract(payload: InvestmentContractInput) -> dict[str, Any]:
    return generate_investment_contract(payload.investor, payload.amount)


@router.post("/financing-term")
def financing_term(payload: FinancingTermInput) -> dict[str, Any]:
    return generate_financing_term(payload.client, payload.amount)


@router.post("/committee-minutes")
def committee_minutes(payload: CommitteeMinutesInput) -> dict[str, Any]:
    return generate_committee_minutes(payload.committee, payload.decision)


@router.get("/logs")
def logs() -> dict[str, Any]:
    return {"items": latest_documents()}
