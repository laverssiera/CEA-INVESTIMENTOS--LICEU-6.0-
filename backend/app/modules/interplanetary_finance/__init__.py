from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class InterplanetaryFundingRequest(BaseModel):
    project_id: str
    amount: float
    category: str # scientific, orbital, oceanic, extreme_infra
    impact_civilizational_score: float

class FundingStatus(BaseModel):
    request_id: UUID
    status: str
    compliance_audit_link: str

# Módulos internos representados por estrutura de diretórios em backend/app/modules/interplanetary_finance/
# - scientific_capital/
# - orbital_finance/
# - oceanic_finance/
# - planetary_risk/
# - civilizational_compliance/
# - ethical_treasury/
