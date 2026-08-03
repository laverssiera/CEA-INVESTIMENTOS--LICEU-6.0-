from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, JSON, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from backend.app.db.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class Wallet(Base):
    __tablename__ = "wallets"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(String, index=True)  # Pode ser ID de Usuário, Fornecedor ou Empresa
    owner_type = Column(String)  # 'user', 'supplier', 'institutional', 'holding'
    balance = Column(Numeric(precision=20, scale=8), default=0)
    currency = Column(String, default="BRL")
    status = Column(String, default="active")
    extra_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

class LedgerEntry(Base):
    """Realiza o registro de partidas dobradas (Double-Entry Ledger)"""
    __tablename__ = "ledger_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"))
    entry_type = Column(String)  # 'debit', 'credit'
    amount = Column(Numeric(precision=20, scale=8))
    description = Column(String)
    account_code = Column(String) # Plano de contas institucional
    created_at = Column(DateTime, default=utc_now)

class LiquidityPosition(Base):
    __tablename__ = "liquidity_positions"
    
    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(String, index=True)
    total_receivables = Column(Numeric(precision=20, scale=2))
    available_liquidity = Column(Numeric(precision=20, scale=2))
    locked_amount = Column(Numeric(precision=20, scale=2))
    risk_buffer = Column(Numeric(precision=20, scale=2))
    updated_at = Column(DateTime, default=utc_now)
