from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime, timezone


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)

class FederationNode(BaseModel):
    node_id: str
    monolith: str
    domain: str
    sovereign: bool = True
    cognition_enabled: bool = True
    agi_enabled: bool = True
    digital_twin_enabled: bool = True
    created_at: datetime = Field(default_factory=_utc_now)

CEA_NODE = FederationNode(
    node_id=str(uuid4()),
    monolith="CEA_INVESTIMENTOS",
    domain="financial_runtime"
)
