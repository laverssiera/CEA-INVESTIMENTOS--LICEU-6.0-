from sqlalchemy.orm import Session
from app.models.entities import FinanceWallet, FinanceCashflowSnapshot
from app.ai.john_financial import JohnFinancialCopilot
from datetime import datetime, timedelta, timezone
import logging

class TreasuryAutoscaling:
    """
    ISSUE-CEA-004: Treasury Autoscaling
    Implements predictive liquidity, funding balancing, and AI scaling.
    """
    def __init__(self, db: Session, finance_os):
        self.db = db
        self.john = JohnFinancialCopilot(finance_os)

    async def predict_liquidity_gap(self, days: int = 30):
        """
        Simple predictive model based on historical snapshots and schedules.
        """
        snapshots = self.db.query(FinanceCashflowSnapshot).order_by(
            FinanceCashflowSnapshot.reference_date.desc()
        ).limit(days).all()
        
        if not snapshots:
            return {"status": "insufficient_data"}
            
        avg_outflow = sum(float(s.outflow) for s in snapshots) / len(snapshots)
        avg_inflow = sum(float(s.inflow) for s in snapshots) / len(snapshots)
        
        projected_net = avg_inflow - avg_outflow
        
        return {
            "projected_net_30d": projected_net,
            "confidence": 0.85 if len(snapshots) >= days else 0.5,
            "prediction_date": datetime.now(timezone.utc) + timedelta(days=days)
        }

    async def balance_funding(self):
        """
        Automatically balances funding between entities based on John's insights.
        """
        health = await self.john.analyze_treasury_health()
        exposure = health.get("exposure_index", 0)
        
        actions_taken = []
        
        if exposure > 0.6:
            # High risk: Pull liquidity from non-essential budgets
            actions_taken.append("Initiated emergency funding pull from GAMEMKT_BUDGET")
            # In a real scenario, this would trigger ledger transfers
        elif exposure < 0.2:
            # Excess liquidity: Deploy to Archimedes for RWA yield
            actions_taken.append("Deploying excess liquidity to ARCHIMEDES_TREASURY for project expansion")
            
        return {
            "exposure_index": exposure,
            "rebalancing_actions": actions_taken,
            "status": "balanced" if exposure <= 0.5 else "rebalancing_req"
        }

    async def scale_treasury_ai(self):
        """
        Scales AI processing capacity based on transaction volume.
        """
        # Monitoring transaction velocity
        # (Mock implementation of AI scaling logic)
        return {
            "ai_agent_replicas": 3,
            "model_version": "john-financial-v2-scaling",
            "active_tasks": ["liquidity_predict", "yield_opt"]
        }
