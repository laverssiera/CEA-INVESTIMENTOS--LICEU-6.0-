from sqlalchemy.orm import Session
from app.ai.john_financial import JohnFinancialCopilot
from app.services.ecosystem_score import EcosystemCreditScoreService
from app.services.supplier_liquidity import SupplierLiquidityService
from app.models.financial_contracts import FinancialContract
import logging

class AIUnderwritingRuntime:
    """
    ISSUE-CEA-003: AI Underwriting Runtime
    Responsible for risk orchestration, liquidity balancing, and credit intelligence.
    """
    def __init__(self, db: Session, finance_os):
        self.db = db
        self.john = JohnFinancialCopilot(finance_os)
        self.score_service = EcosystemScoreService(db)
        self.liquidity_service = SupplierLiquidityService(db)

    async def run_underwriting_pipeline(self, entity_id: str, requested_amount: float):
        """
        Orchestrates the AI-driven underwriting process.
        """
        logging.info(f"Starting AI Underwriting for entity {entity_id}")
        
        # 1. Credit Intelligence (Ecosystem Score)
        score_data = self.score_service.calculate_score(entity_id)
        credit_score = score_data.get("score", 0)
        
        # 2. Risk Orchestration (John's Insights)
        treasury_health = await self.john.analyze_treasury_health()
        exposure_index = treasury_health.get("exposure_index", 0)
        
        # Determine approval based on score and exposure
        is_approved = False
        reason = ""
        
        if credit_score > 700 and exposure_index < 0.6:
            is_approved = True
            reason = "High score and healthy treasury exposure."
        elif credit_score > 850:
            is_approved = True
            reason = "Elite performer entity, exception granted."
        else:
            is_approved = False
            reason = f"Underwriting failed: Score {credit_score}, Exposure {exposure_index}"

        # 3. Liquidity Balancing (Dynamic Pricing)
        # Apply yield dynamic based on treasury health
        yield_multiplier = 1.0
        if exposure_index > 0.5:
            yield_multiplier = 1.2 # Increase cost to balance liquidity demand
            
        final_rate = self.liquidity_service.get_dynamic_rate(entity_id) * yield_multiplier

        return {
            "entity_id": entity_id,
            "approved": is_approved,
            "reason": reason,
            "credit_score": credit_score,
            "recommended_rate": final_rate,
            "treasury_status": treasury_health.get("cio_virtual_status")
        }
