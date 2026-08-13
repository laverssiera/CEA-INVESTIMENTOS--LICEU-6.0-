from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone
from uuid import UUID, uuid4


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)

class MissionAsset(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    category: str # 'scientific', 'orbital', 'oceanic', 'deep_tech'
    valuation: float
    funding_status: str # 'AWAITING_FUNDS', 'PARTIALLY_FUNDED', 'FULLY_FUNDED', 'OPERATIONAL'
    impact_civilizational_score: float # 0.0 to 1.0

class MissionPortfolioStatus(BaseModel):
    total_valuation: float
    active_missions_count: int
    average_impact_score: float
    allocation_by_category: dict[str, float]

class MissionPortfolio(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    owner_id: str
    assets: List[MissionAsset] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)
