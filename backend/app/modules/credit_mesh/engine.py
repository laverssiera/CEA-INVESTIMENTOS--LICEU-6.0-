from typing import Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)

class OperationalCreditScore(BaseModel):
    spe_id: str
    financial_health: float = 0.0      # 20%
    construction_execution: float = 0.0 # 20%
    technical_history: float = 0.0     # 15%
    compliance: float = 0.0            # 10%
    legal_risk: float = 0.0            # 10%
    supplier_risk: float = 0.0         # 10%
    esg_impact: float = 0.0            # 5%
    operational_performance: float = 0.0 # 10%
    updated_at: datetime = Field(default_factory=_utc_now)

    @property
    def global_score(self) -> float:
        return (
            self.financial_health * 0.20 +
            self.construction_execution * 0.20 +
            self.technical_history * 0.15 +
            self.compliance * 0.10 +
            self.legal_risk * 0.10 +
            self.supplier_risk * 0.10 +
            self.esg_impact * 0.05 +
            self.operational_performance * 0.10
        )

class CreditMeshEngine:
    """
    Credit Mesh Ecossistêmico.
    Gerencia o Operational Credit Score (OCS) dinâmico baseado em eventos NATS.
    """
    
    async def process_event(self, subject: str, data: Dict):
        """
        Gatilhos de atualização: cea.credit.score.updated, etc.
        """
        # Exemplo: Se vier do BIM (execução de obra), atualiza construction_execution
        pass

    def get_dynamic_limit(self, ocs: OperationalCreditScore, total_liquidity: float) -> float:
        """
        Cálculo dinâmico de limites baseado em score e liquidez sistêmica.
        """
        base_multiplier = ocs.global_score
        return total_liquidity * 0.05 * base_multiplier  # Ex: Libera até 5% da liquidez total proporcional ao score
