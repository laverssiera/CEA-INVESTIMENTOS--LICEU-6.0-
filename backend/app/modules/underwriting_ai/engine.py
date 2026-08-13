from typing import Dict, Any, List
from pydantic import BaseModel

class UnderwritingSignal(BaseModel):
    source: str  # BIM, OPERA, HUB, JURIDICOTECH, etc.
    score: float # 0.0 a 1.0
    details: Dict[str, Any]

class UnderwritingDecision(BaseModel):
    spe_id: str
    status: str # APPROVED, PARTIAL, REJECTED
    limit: float
    retention_rate: float
    risk_factors: List[str]
    confidence_level: float

class UnderwritingEngine:
    """
    Novo Motor Cognitivo de Crédito (Evoluído).
    Analisa sinais de múltiplos monólitos para aprovação de funding institucional.
    Análises: BIM, OPERA, HUB, JURIDICOTECH, ANCHOR, PROCUREMENT, RH, ESG, ARCHIMEDES.
    """
    
    async def evaluate_spe(self, spe_id: str, signals: List[UnderwritingSignal]) -> UnderwritingDecision:
        weights = {
            "HUB": 0.20,             # Saúde Financeira
            "BIM": 0.20,             # Execução de Obra
            "ARCHIMEDES": 0.15,      # Histórico/Performance Operacional
            "COMPLIANCE": 0.10,      # Compliance
            "JURIDICOTECH": 0.10,    # Risco Jurídico
            "PROCUREMENT": 0.10,     # Risco Fornecedor
            "ESG": 0.05,             # Impacto Ambiental
            "OPERA": 0.10            # Produtividade/Performance
        }
        
        final_score = 0.0
        risk_factors = []
        
        for signal in signals:
            weight = weights.get(signal.source, 0.05)
            final_score += (signal.score * weight)
            if signal.score < 0.6:
                risk_factors.append(f"Alerta: Baixa performance/risco em {signal.source}")

        status = "APPROVED"
        retention = 0.05 # 5% padrão
        
        # Exemplo baseado no requisito "SPE Alpha"
        if final_score < 0.8:
            status = "PARTIAL"
            retention = 0.12 # Retenção automática de 12% em caso de risco moderado
        
        if final_score < 0.4:
            status = "REJECTED"

        return UnderwritingDecision(
            spe_id=spe_id,
            status=status,
            limit=5000000.0 * final_score, # Capital disponível proporcional ao score
            retention_rate=retention,
            risk_factors=risk_factors,
            confidence_level=0.95
        )
