from sqlalchemy import Column, Integer, String, Numeric, DateTime, JSON, ForeignKey
from datetime import datetime, timezone
from backend.app.db.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class RWAAsset(Base):
    __tablename__ = "rwa_assets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    asset_type = Column(String) # 'real_estate', 'receivable', 'energy', 'industrial'
    valuation = Column(Numeric(precision=20, scale=2))
    token_total_supply = Column(Numeric(precision=20, scale=8))
    token_price = Column(Numeric(precision=10, scale=2))
    status = Column(String, default="active") # 'pending', 'active', 'liquidated'
    origin_project_id = Column(String, nullable=True) # ID do projeto no ARCHIMEDES
    yield_config = Column(JSON) # Regras de distribuição de rendimento
    created_at = Column(DateTime, default=utc_now)

class RWAToken(Base):
    __tablename__ = "rwa_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("rwa_assets.id"))
    wallet_id = Column(Integer, ForeignKey("wallets.id"))
    balance = Column(Numeric(precision=20, scale=8))
    locked_balance = Column(Numeric(precision=20, scale=8), default=0)
    updated_at = Column(DateTime, default=utc_now)

class RWAYieldDistribution(Base):
    __tablename__ = "rwa_yields"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("rwa_assets.id"))
    amount_total = Column(Numeric(precision=20, scale=2))
    distributed_at = Column(DateTime, default=utc_now)
    period_reference = Column(String) # '2026-05'
