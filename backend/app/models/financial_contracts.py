from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, Numeric, String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
import enum


def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class ContractStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PENDING_SETTLEMENT = "pending_settlement"
    SETTLED = "settled"
    CANCELLED = "cancelled"

class FinancialContract(Base):
    """
    Base model for Financial Contracts (ISSUE-CEA-001)
    Supports Ledger, Treasury, and Settlement tracking.
    """
    __tablename__ = "financial_contracts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    contract_type: Mapped[str] = mapped_column(String(50), nullable=False) # 'ledger', 'treasury', 'settlement'
    status: Mapped[str] = mapped_column(String(30), default=ContractStatus.DRAFT, nullable=False)
    
    # Financial details
    amount: Mapped[float] = mapped_column(Numeric(16, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="BRL", nullable=False)
    
    # Parties / Wallets
    source_wallet_id: Mapped[str] = mapped_column(ForeignKey("finance_wallets.id"), nullable=True)
    destination_wallet_id: Mapped[str] = mapped_column(ForeignKey("finance_wallets.id"), nullable=True)
    
    # Settlement Info
    scheduled_settlement_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    actual_settlement_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Immutable & Audit
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

class LedgerContract(FinancialContract):
    """Specific logic for Ledger-based contracts"""
    __tablename__ = "ledger_contracts"
    id: Mapped[str] = mapped_column(ForeignKey("financial_contracts.id"), primary_key=True)
    ledger_account_code: Mapped[str] = mapped_column(String(100), nullable=True)

class TreasuryContract(FinancialContract):
    """Specific logic for Treasury/Funding contracts"""
    __tablename__ = "treasury_contracts"
    id: Mapped[str] = mapped_column(ForeignKey("financial_contracts.id"), primary_key=True)
    funding_source: Mapped[str] = mapped_column(String(100), nullable=True)

class SettlementContract(FinancialContract):
    """Specific logic for Settlement/Liquidation contracts"""
    __tablename__ = "settlement_contracts"
    id: Mapped[str] = mapped_column(ForeignKey("financial_contracts.id"), primary_key=True)
    settlement_method: Mapped[str] = mapped_column(String(50), default="PIX")
