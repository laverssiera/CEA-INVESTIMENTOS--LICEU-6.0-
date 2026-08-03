from typing import Optional, List, Any
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID

class FinancialContractBase(BaseModel):
    contract_type: str
    amount: float
    currency: str = "BRL"
    source_wallet_id: Optional[str] = None
    destination_wallet_id: Optional[str] = None
    scheduled_settlement_at: Optional[datetime] = None
    metadata_json: dict = Field(default_factory=dict)

class FinancialContractCreate(FinancialContractBase):
    pass

class FinancialContractUpdate(BaseModel):
    status: Optional[str] = None
    amount: Optional[float] = None
    actual_settlement_at: Optional[datetime] = None
    metadata_json: Optional[dict] = None

class FinancialContractSchema(FinancialContractBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    status: str
    version: int
    created_at: datetime
    updated_at: datetime

class LedgerContractCreate(FinancialContractCreate):
    ledger_account_code: str

class TreasuryContractCreate(FinancialContractCreate):
    funding_source: str

class SettlementContractCreate(FinancialContractCreate):
    settlement_method: str = "PIX"
