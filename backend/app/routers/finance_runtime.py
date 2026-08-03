from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.db.session import get_db
from app.services.settlement_service import SettlementService
from app.services.immutable_runtime_service import ImmutableFinancialRuntime
from app.services.ai_underwriting_runtime import AIUnderwritingRuntime
from app.services.treasury_autoscaling import TreasuryAutoscaling
from app.schemas.financial_contracts import (
    LedgerContractCreate, 
    TreasuryContractCreate, 
    SettlementContractCreate,
    FinancialContractSchema
)
from app.services.finance_os_core import FinanceOSService

router = APIRouter(prefix="/api/finance-os", tags=["Finance OS Runtime"])

# --- ISSUE-CEA-001: Financial Contracts ---

@router.post("/contracts/ledger", response_model=FinancialContractSchema)
def create_ledger_contract(data: LedgerContractCreate, db: Session = Depends(get_db)):
    service = SettlementService(db)
    return service.create_ledger_contract(data)

@router.post("/contracts/treasury", response_model=FinancialContractSchema)
def create_treasury_contract(data: TreasuryContractCreate, db: Session = Depends(get_db)):
    service = SettlementService(db)
    return service.create_treasury_contract(data)

@router.post("/contracts/settlement", response_model=FinancialContractSchema)
def create_settlement_contract(data: SettlementContractCreate, db: Session = Depends(get_db)):
    service = SettlementService(db)
    return service.create_settlement_contract(data)

@router.post("/contracts/{contract_id}/settle")
def contract_settle(contract_id: str, db: Session = Depends(get_db)):
    service = SettlementService(db)
    contract = service.settle_contract(contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return {"status": "settled", "contract_id": contract_id}

# --- ISSUE-CEA-002: Immutable Financial Runtime ---

@router.get("/runtime/replay")
def replay_events(start: int = 0, end: int = None, db: Session = Depends(get_db)):
    runtime = ImmutableFinancialRuntime(db)
    try:
        events = runtime.replay(start, end)
        return events
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/runtime/snapshot")
def create_snapshot(db: Session = Depends(get_db)):
    runtime = ImmutableFinancialRuntime(db)
    snapshot = runtime.create_snapshot()
    if not snapshot:
        raise HTTPException(status_code=400, detail="No events to snapshot")
    return {"status": "created", "snapshot_id": snapshot.id}

# --- ISSUE-CEA-003: AI Underwriting Runtime ---

@router.post("/underwriting/analyze")
async def analyze_underwriting(entity_id: str, amount: float, db: Session = Depends(get_db)):
    # FinanceOSService is needed for JohnFinancialCopilot
    finance_os = FinanceOSService(db)
    runtime = AIUnderwritingRuntime(db, finance_os)
    result = await runtime.run_underwriting_pipeline(entity_id, amount)
    return result

# --- ISSUE-CEA-004: Treasury Autoscaling ---

@router.get("/treasury/liquidity-prediction")
async def get_liquidity_prediction(days: int = 30, db: Session = Depends(get_db)):
    finance_os = FinanceOSService(db)
    autoscaling = TreasuryAutoscaling(db, finance_os)
    return await autoscaling.predict_liquidity_gap(days)

@router.post("/treasury/rebalance")
async def rebalance_funding(db: Session = Depends(get_db)):
    finance_os = FinanceOSService(db)
    autoscaling = TreasuryAutoscaling(db, finance_os)
    return await autoscaling.balance_funding()

@router.get("/treasury/ai-scaling-status")
async def get_ai_scaling_status(db: Session = Depends(get_db)):
    finance_os = FinanceOSService(db)
    autoscaling = TreasuryAutoscaling(db, finance_os)
    return await autoscaling.scale_treasury_ai()
