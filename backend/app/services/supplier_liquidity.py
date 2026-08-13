from decimal import Decimal
from typing import Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from backend.app.models.finance_core import Wallet, LiquidityPosition
from backend.app.services.finance_os_core import FinanceOSService
from backend.app.services.ecosystem_score import EcosystemCreditScoreService

class SupplierLiquidityService:
    def __init__(self, db: Session):
        self.db = db
        self.finance_os = FinanceOSService(db)
        self.score_service = EcosystemCreditScoreService()

    async def evaluate_anticipation_limit(self, supplier_id: str, receivables_amount: Decimal, opera_metrics: dict) -> dict:
        """
        Calcula o limite de antecipação e taxa baseada no Ecosystem Score.
        """
        # 1. Obtém o Score Real do Ecossistema
        score_data = await self.score_service.calculate_score(supplier_id, opera_metrics, {"reputation": 9.5})
        score = score_data["ecosystem_score"]
        
        # 2. Define Taxas Dinâmicas (Yield Dinâmico)
        # Score 1000 -> 0.5% a.m | Score 0 -> 5% a.m (exemplo punitivo)
        base_rate = Decimal("0.05") 
        reduction = (Decimal(str(score)) / Decimal("1000")) * Decimal("0.045")
        final_monthly_rate = base_rate - reduction
        
        # 3. Calcula Limite por Tier
        multiplier = Decimal("0.95") if score > 850 else Decimal("0.80") if score > 700 else Decimal("0.50")
        max_anticipation = receivables_amount * multiplier

        return {
            "supplier_id": supplier_id,
            "ecosystem_score": score,
            "max_anticipation_limit": max_anticipation,
            "monthly_rate": round(final_monthly_rate * 100, 2),
            "tier": score_data["tier"],
            "recommendation": "APPROVED" if score > 600 else "REQUIRES_GOVERNANCE"
        }

    def process_anticipation(self, supplier_wallet_id: int, amount: Decimal, total_receivable: Decimal):
        """
        Executa a antecipação de fato no Finance OS.
        """
        # Taxa de conveniência/risco fixa para o exemplo
        fee = amount * Decimal("0.02")
        net_amount = amount - fee
        
        # Transação: Holding -> Fornecedor
        tx_id = self.finance_os.process_transaction(
            from_wallet_id=1, # Central Liquidity Wallet
            to_wallet_id=supplier_wallet_id,
            amount=net_amount,
            description=f"Antecipação de Recebíveis - Liquidez Fornecedor"
        )
        
        return {
            "transaction_id": tx_id,
            "net_amount": net_amount,
            "fee_retained": fee,
            "timestamp": datetime.now(timezone.utc)
        }
