from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.orm import Session

from app.events import event_bus
from app.repositories.finance_repository import FinanceRepository
from app.services.automation_storage import fetch_event_by_id, fetch_event_dispatch_status, fetch_event_dispatches


@dataclass
class RbacActor:
    user_id: str
    role: str


class FinanceService:
    LEARNING_STATE: dict[str, float] = {"allocation_bias": 0.0}
    LAST_CEFEIDA_SIGNAL: dict[str, Any] = {
        "market_trend": "neutral",
        "demand_index": 0.5,
        "risk_outlook": 0.5,
        "forecast_confidence": 0.5,
    }

    DEFAULT_WALLETS = [
        {
            "code": "CEA_MASTER",
            "name": "CEA Master Capital",
            "owner_entity": "CEA",
            "wallet_type": "master",
            "balance": 5_000_000.0,
            "monthly_budget": 3_000_000.0,
        },
        {
            "code": "ARCHIMEDES_OPER",
            "name": "Archimedes Treasury",
            "owner_entity": "Archimedes",
            "wallet_type": "project",
            "balance": 950_000.0,
            "monthly_budget": 1_800_000.0,
        },
        {
            "code": "GAMEMKT_BUDGET",
            "name": "GameMKT Budget",
            "owner_entity": "GameMKT",
            "wallet_type": "budget",
            "balance": 420_000.0,
            "monthly_budget": 600_000.0,
        },
        {
            "code": "HUBBACKOFFICE_COST",
            "name": "HubBackoffice Custos",
            "owner_entity": "HubBackoffice",
            "wallet_type": "cost",
            "balance": 280_000.0,
            "monthly_budget": 450_000.0,
        },
    ]

    def __init__(self, db: Session):
        self.db = db
        self.repo = FinanceRepository(db)

    def ensure_default_wallets(self) -> list[dict[str, Any]]:
        for wallet in self.DEFAULT_WALLETS:
            if self.repo.get_wallet_by_code(wallet["code"]) is None:
                self.repo.create_wallet(**wallet)

        self.db.commit()
        return self.list_wallets()

    def list_wallets(self) -> list[dict[str, Any]]:
        rows = self.repo.list_wallets()
        return [
            {
                "id": w.id,
                "code": w.code,
                "name": w.name,
                "owner_entity": w.owner_entity,
                "wallet_type": w.wallet_type,
                "balance": float(w.balance),
                "monthly_budget": float(w.monthly_budget),
                "active": w.active,
            }
            for w in rows
        ]

    def transfer(
        self,
        actor: RbacActor,
        from_wallet_code: str,
        to_wallet_code: str,
        amount: float,
        entity_id: str,
        entity_type: str,
        reference: str,
    ) -> dict[str, Any]:
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        source = self.repo.get_wallet_by_code(from_wallet_code)
        target = self.repo.get_wallet_by_code(to_wallet_code)

        if source is None or target is None:
            raise ValueError("Wallet not found")

        source_balance = float(source.balance)
        if source_balance < amount:
            raise ValueError("Insufficient funds")

        source.balance = source_balance - amount
        target.balance = float(target.balance) + amount

        entry = self.repo.create_ledger_entry(
            entity_id=entity_id,
            entity_type=entity_type,
            debit_wallet_id=target.id,
            credit_wallet_id=source.id,
            debit_account=f"wallet:{target.code}",
            credit_account=f"wallet:{source.code}",
            amount=amount,
            reference=reference,
            metadata_json={"actor_role": actor.role, "actor_id": actor.user_id},
        )

        self.repo.add_audit(
            action="wallet.transfer",
            user_id=actor.user_id,
            actor_role=actor.role,
            metadata_json={
                "ledger_entry_id": entry.id,
                "from_wallet": from_wallet_code,
                "to_wallet": to_wallet_code,
                "amount": amount,
                "reference": reference,
            },
        )

        self.db.commit()

        return {
            "ledger_entry_id": entry.id,
            "from_wallet": from_wallet_code,
            "to_wallet": to_wallet_code,
            "amount": amount,
            "reference": reference,
            "balance_after": {
                "from_wallet": float(source.balance),
                "to_wallet": float(target.balance),
            },
        }

    def cashflow(self, period: str = "daily", liquidity_threshold: float = 200_000.0) -> dict[str, Any]:
        rows = self.repo.ledger_sum_by_period(period)
        if not rows:
            now = datetime.now(UTC)
            self.repo.create_cashflow_snapshot(
                period=period,
                reference_date=now,
                inflow=0,
                outflow=0,
                net=0,
                liquidity_alert=True,
            )
            self.db.commit()
            event_bus.publish("finance.cashflow_alert", {"period": period, "net": 0})
            return {
                "period": period,
                "points": [],
                "forecast": {"next_period_net": 0, "signal": "alert"},
                "liquidity_alert": True,
            }

        points = []
        last_net = 0.0
        for bucket, inflow, outflow in rows:
            net = inflow - outflow
            last_net = net
            points.append(
                {
                    "bucket": bucket.isoformat() if hasattr(bucket, "isoformat") else str(bucket),
                    "inflow": round(inflow, 2),
                    "outflow": round(outflow, 2),
                    "net": round(net, 2),
                }
            )

        liquidity_alert = last_net < liquidity_threshold
        self.repo.create_cashflow_snapshot(
            period=period,
            reference_date=datetime.now(UTC),
            inflow=points[-1]["inflow"],
            outflow=points[-1]["outflow"],
            net=points[-1]["net"],
            liquidity_alert=liquidity_alert,
        )
        if liquidity_alert:
            event_bus.publish("finance.cashflow_alert", {"period": period, "net": points[-1]["net"]})

        self.db.commit()

        avg_net = sum(item["net"] for item in points) / len(points)
        return {
            "period": period,
            "points": points,
            "forecast": {
                "next_period_net": round(avg_net, 2),
                "signal": "attention" if liquidity_alert else "healthy",
            },
            "liquidity_alert": liquidity_alert,
        }

    @staticmethod
    def _irr(cashflows: list[float]) -> float:
        low = -0.99
        high = 5.0
        for _ in range(100):
            mid = (low + high) / 2
            npv = 0.0
            for i, value in enumerate(cashflows):
                npv += value / ((1 + mid) ** i)
            if npv > 0:
                low = mid
            else:
                high = mid
        return round((low + high) / 2, 6)

    def roi_metrics(
        self,
        entity_id: str,
        investment_amount: float,
        current_value: float,
        monthly_cashflows: list[float],
        discount_rate: float,
    ) -> dict[str, Any]:
        if investment_amount <= 0:
            raise ValueError("investment_amount must be greater than zero")

        roi = (current_value - investment_amount) / investment_amount

        cumulative = 0.0
        payback_months = None
        for index, cash in enumerate(monthly_cashflows, start=1):
            cumulative += cash
            if cumulative >= investment_amount and payback_months is None:
                payback_months = index

        npv = -investment_amount
        for i, value in enumerate(monthly_cashflows, start=1):
            npv += value / ((1 + discount_rate) ** i)
        npv += current_value / ((1 + discount_rate) ** max(len(monthly_cashflows), 1))

        irr = self._irr([-investment_amount, *monthly_cashflows, current_value])

        self.repo.upsert_deal_analysis(
            entity_id=entity_id,
            entity_type="project",
            values={
                "expected_return": roi,
                "risk_score": 0.45,
                "liquidity_score": 0.63,
                "time_horizon_months": max(len(monthly_cashflows), 1),
                "final_score": max(0.0, min(1.0, roi * 0.5 + 0.32)),
                "recommendation": "invest" if roi > 0.1 else "hold",
                "realized_roi": roi,
            },
        )
        event_bus.publish("finance.roi_calculated", {"entity_id": entity_id, "roi": round(roi, 4)})
        if roi < 0:
            event_bus.publish("finance.loss_detected", {"entity_id": entity_id, "roi": round(roi, 4)})

        self.db.commit()

        return {
            "entity_id": entity_id,
            "roi": round(roi, 4),
            "irr": irr,
            "payback_months": payback_months,
            "npv": round(npv, 2),
        }

    def invest_decision(
        self,
        actor: RbacActor,
        source_wallet_code: str,
        target_wallet_code: str,
        amount: float,
        target: str,
        expected_return: float,
        risk_score: float,
        liquidity_score: float,
        time_horizon_months: int,
    ) -> dict[str, Any]:
        base_score = (expected_return * 0.45) + ((1 - risk_score) * 0.3) + (liquidity_score * 0.15) + (
            max(0.0, 1 - time_horizon_months / 60) * 0.1
        )
        final_score = round(max(0.0, min(1.0, base_score)), 4)
        action = "invest" if final_score >= 0.55 else "hold"

        transfer_receipt = None
        if action == "invest":
            transfer_receipt = self.transfer(
                actor=actor,
                from_wallet_code=source_wallet_code,
                to_wallet_code=target_wallet_code,
                amount=amount,
                entity_id=target,
                entity_type="investment_deal",
                reference="auto-allocation",
            )
            event_bus.publish(
                "finance.investment_created",
                {"target": target, "amount": amount, "source_wallet": source_wallet_code},
            )

        self.repo.upsert_deal_analysis(
            entity_id=target,
            entity_type="investment_deal",
            values={
                "expected_return": expected_return,
                "risk_score": risk_score,
                "liquidity_score": liquidity_score,
                "time_horizon_months": time_horizon_months,
                "final_score": final_score,
                "recommendation": action,
                "realized_roi": 0,
            },
        )

        self.repo.add_audit(
            action="finance.invest_decision",
            user_id=actor.user_id,
            actor_role=actor.role,
            metadata_json={
                "target": target,
                "amount": amount,
                "action": action,
                "score": final_score,
            },
        )

        self.db.commit()

        return {
            "action": action,
            "amount": amount if action == "invest" else 0,
            "target": target,
            "score": final_score,
            "transfer": transfer_receipt,
        }

    def consume_external_event(self, actor: RbacActor, event_name: str, payload: dict[str, Any]) -> dict[str, Any]:
        allowed = {
            "archimedes.deal_created",
            "gamemkt.campaign_started",
            "hub.cost_registered",
        }
        if event_name not in allowed:
            raise ValueError("Unsupported event")

        self.repo.add_audit(
            action="finance.event_consumed",
            user_id=actor.user_id,
            actor_role=actor.role,
            metadata_json={"event_name": event_name, "payload": payload},
        )
        self.db.commit()

        return {"status": "consumed", "event_name": event_name, "received_at": datetime.now(UTC).isoformat()}

    def ingest_cefeida_feed(
        self,
        actor: RbacActor,
        market_trend: str,
        demand_index: float,
        risk_outlook: float,
        forecast_confidence: float,
    ) -> dict[str, Any]:
        normalized = {
            "market_trend": market_trend,
            "demand_index": max(0.0, min(1.0, demand_index)),
            "risk_outlook": max(0.0, min(1.0, risk_outlook)),
            "forecast_confidence": max(0.0, min(1.0, forecast_confidence)),
        }
        self.LAST_CEFEIDA_SIGNAL = normalized

        self.repo.add_audit(
            action="finance.cefeida_feed_ingested",
            user_id=actor.user_id,
            actor_role=actor.role,
            metadata_json=normalized,
        )
        event_bus.publish("finance.cefeida_feed_ingested", normalized)
        self.db.commit()

        return {"status": "ingested", "signal": normalized}

    def john_assisted_decision(
        self,
        actor: RbacActor,
        target: str,
        amount: float,
        expected_return: float,
        risk_score: float,
        liquidity_score: float,
        time_horizon_months: int,
    ) -> dict[str, Any]:
        signal = self.LAST_CEFEIDA_SIGNAL
        trend_bonus = 0.06 if signal["market_trend"] in {"bull", "growth"} else -0.04
        demand_bonus = (signal["demand_index"] - 0.5) * 0.2
        risk_penalty = signal["risk_outlook"] * 0.15
        learning_adjustment = self.LEARNING_STATE["allocation_bias"]

        confidence = max(
            0.0,
            min(
                1.0,
                (expected_return * 0.35)
                + ((1 - risk_score) * 0.25)
                + (liquidity_score * 0.15)
                + (max(0.0, 1 - time_horizon_months / 72) * 0.1)
                + trend_bonus
                + demand_bonus
                - risk_penalty
                + learning_adjustment,
            ),
        )

        action = "invest" if confidence >= 0.55 else "hold"
        recommendation = {
            "action": action,
            "amount": amount if action == "invest" else 0,
            "target": target,
            "confidence": round(confidence, 4),
            "rationale": {
                "market_trend": signal["market_trend"],
                "demand_index": signal["demand_index"],
                "risk_outlook": signal["risk_outlook"],
                "learning_bias": round(learning_adjustment, 4),
            },
        }

        self.repo.add_audit(
            action="finance.john_decision",
            user_id=actor.user_id,
            actor_role=actor.role,
            metadata_json=recommendation,
        )
        event_bus.publish("finance.john_decision_generated", recommendation)
        self.db.commit()
        return recommendation

    def register_learning_feedback(
        self,
        actor: RbacActor,
        target: str,
        invested_amount: float,
        realized_return: float,
    ) -> dict[str, Any]:
        if invested_amount <= 0:
            raise ValueError("invested_amount must be greater than zero")

        realized_roi = realized_return / invested_amount
        current_bias = self.LEARNING_STATE["allocation_bias"]
        adjustment = max(-0.05, min(0.05, realized_roi * 0.1))
        new_bias = max(-0.2, min(0.2, current_bias + adjustment))
        self.LEARNING_STATE["allocation_bias"] = new_bias

        feedback = {
            "target": target,
            "realized_roi": round(realized_roi, 4),
            "previous_bias": round(current_bias, 4),
            "new_bias": round(new_bias, 4),
        }
        self.repo.add_audit(
            action="finance.learning_feedback",
            user_id=actor.user_id,
            actor_role=actor.role,
            metadata_json=feedback,
        )
        event_bus.publish("finance.learning_updated", feedback)
        self.db.commit()

        return {"status": "updated", "learning": feedback}

    def compliance_check(
        self,
        actor: RbacActor,
        contract_valid: bool,
        legal_risk_score: float,
        blocked_by_legal: bool,
    ) -> dict[str, Any]:
        legal_risk_score = max(0.0, min(1.0, legal_risk_score))
        approved = contract_valid and not blocked_by_legal and legal_risk_score <= 0.65
        output = {
            "approved": approved,
            "checks": {
                "contract_valid": contract_valid,
                "blocked_by_legal": blocked_by_legal,
                "legal_risk_score": legal_risk_score,
            },
            "reason": "ok" if approved else "compliance_block",
        }

        self.repo.add_audit(
            action="finance.compliance_check",
            user_id=actor.user_id,
            actor_role=actor.role,
            metadata_json=output,
        )
        event_bus.publish("finance.compliance_checked", output)
        self.db.commit()
        return output

    def antifraud_check(
        self,
        actor: RbacActor,
        transaction_amount: float,
        expected_budget: float,
        velocity_24h: int,
        counterpart_mismatch: bool,
    ) -> dict[str, Any]:
        if expected_budget <= 0:
            expected_budget = 1

        budget_factor = transaction_amount / expected_budget
        velocity_factor = min(1.0, velocity_24h / 20)
        mismatch_factor = 1.0 if counterpart_mismatch else 0.0
        score = max(0.0, min(1.0, (budget_factor * 0.45) + (velocity_factor * 0.3) + (mismatch_factor * 0.25)))
        flagged = score >= 0.6

        output = {
            "flagged": flagged,
            "fraud_score": round(score, 4),
            "signals": {
                "budget_factor": round(budget_factor, 4),
                "velocity_24h": velocity_24h,
                "counterpart_mismatch": counterpart_mismatch,
            },
        }

        self.repo.add_audit(
            action="finance.antifraud_check",
            user_id=actor.user_id,
            actor_role=actor.role,
            metadata_json=output,
        )
        if flagged:
            event_bus.publish("finance.fraud_alert", output)
        self.db.commit()
        return output

    def intelligence_output(
        self,
        entity_id: str,
        roi: float,
        risk_score: float,
        liquidity_alert: bool,
        compliance_blocked: bool,
    ) -> dict[str, Any]:
        viability_score = max(0.0, min(1.0, (roi * 0.5) + ((1 - risk_score) * 0.35) + (0.15 if not liquidity_alert else 0)))
        recommendation = "hold"
        if compliance_blocked:
            recommendation = "blocked"
        elif viability_score >= 0.62:
            recommendation = "invest"

        output = {
            "entity_id": entity_id,
            "viabilidade": round(viability_score, 4),
            "recomendacao_investimento": recommendation,
            "alerta_risco_financeiro": liquidity_alert or risk_score > 0.65,
        }
        event_bus.publish("finance.intelligence_output", output)
        return output

    def accounting_register(
        self,
        actor: RbacActor,
        entity_id: str,
        entry_type: str,
        amount: float,
        tax_amount: float,
        reference: str,
        status: str = "pending",
    ) -> dict[str, Any]:
        allowed_types = {"accounts_payable", "accounts_receivable", "tax"}
        if entry_type not in allowed_types:
            raise ValueError("entry_type must be accounts_payable, accounts_receivable or tax")
        if amount < 0 or tax_amount < 0:
            raise ValueError("amount and tax_amount must be non-negative")

        entry = self.repo.create_accounting_entry(
            entity_id=entity_id,
            entry_type=entry_type,
            amount=amount,
            tax_amount=tax_amount,
            reference=reference,
            status=status,
            metadata_json={"source": "finance_os"},
        )

        payload = {
            "id": entry.id,
            "entity_id": entity_id,
            "entry_type": entry_type,
            "amount": amount,
            "tax_amount": tax_amount,
            "reference": reference,
            "status": status,
        }
        self.repo.add_audit(
            action="finance.accounting_registered",
            user_id=actor.user_id,
            actor_role=actor.role,
            metadata_json=payload,
        )
        self.db.commit()
        return payload

    def accounting_report(self, entity_id: str | None = None) -> dict[str, Any]:
        rows = self.repo.list_accounting_entries(entity_id=entity_id)

        accounts_payable = 0.0
        accounts_receivable = 0.0
        taxes = 0.0
        for row in rows:
            amount = float(row.amount)
            tax = float(row.tax_amount)
            if row.entry_type == "accounts_payable":
                accounts_payable += amount
            elif row.entry_type == "accounts_receivable":
                accounts_receivable += amount
            elif row.entry_type == "tax":
                taxes += amount
            taxes += tax

        net_result = accounts_receivable - accounts_payable - taxes
        report = {
            "entity_id": entity_id or "all",
            "accounts_payable": round(accounts_payable, 2),
            "accounts_receivable": round(accounts_receivable, 2),
            "taxes": round(taxes, 2),
            "net_result": round(net_result, 2),
            "entries": len(rows),
        }
        return report

    def accounting_sync_hub(self, actor: RbacActor, entity_id: str | None = None) -> dict[str, Any]:
        report = self.accounting_report(entity_id=entity_id)
        report["destination"] = "hubbackoffice"
        report["synced_at"] = datetime.now(UTC).isoformat()

        self.repo.add_audit(
            action="finance.accounting_synced_hub",
            user_id=actor.user_id,
            actor_role=actor.role,
            metadata_json=report,
        )
        event_bus.publish("hub.accounting_synced", report)
        self.db.commit()
        return report

    def budget_set(
        self,
        actor: RbacActor,
        entity_id: str,
        period: str,
        planned_amount: float,
        metadata_json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if planned_amount < 0:
            raise ValueError("planned_amount must be non-negative")

        item = self.repo.upsert_budget_control(
            entity_id=entity_id,
            period=period,
            planned_amount=planned_amount,
            metadata_json=metadata_json or {},
        )

        output = {
            "entity_id": entity_id,
            "period": period,
            "planned_amount": float(item.planned_amount),
            "realized_amount": float(item.realized_amount),
            "status": item.status,
        }
        self.repo.add_audit(
            action="finance.budget_set",
            user_id=actor.user_id,
            actor_role=actor.role,
            metadata_json=output,
        )
        self.db.commit()
        return output

    def budget_register_execution(
        self,
        actor: RbacActor,
        entity_id: str,
        period: str,
        realized_delta: float,
        reason: str,
    ) -> dict[str, Any]:
        item = self.repo.upsert_budget_control(
            entity_id=entity_id,
            period=period,
            realized_delta=realized_delta,
            metadata_json={"last_reason": reason},
        )

        planned = float(item.planned_amount)
        realized = float(item.realized_amount)
        variance = planned - realized
        utilization = (realized / planned) if planned > 0 else 0.0

        output = {
            "entity_id": entity_id,
            "period": period,
            "planned_amount": planned,
            "realized_amount": realized,
            "variance": round(variance, 2),
            "utilization": round(utilization, 4),
            "status": item.status,
        }
        self.repo.add_audit(
            action="finance.budget_execution_registered",
            user_id=actor.user_id,
            actor_role=actor.role,
            metadata_json={**output, "reason": reason},
        )
        if item.status in {"warning", "over_budget"}:
            event_bus.publish("finance.budget_alert", output)
        self.db.commit()
        return output

    def budget_status(self, entity_id: str, period: str) -> dict[str, Any]:
        item = self.repo.get_budget_control(entity_id=entity_id, period=period)
        if item is None:
            return {
                "entity_id": entity_id,
                "period": period,
                "planned_amount": 0.0,
                "realized_amount": 0.0,
                "variance": 0.0,
                "utilization": 0.0,
                "status": "unplanned",
            }

        planned = float(item.planned_amount)
        realized = float(item.realized_amount)
        variance = planned - realized
        utilization = (realized / planned) if planned > 0 else 0.0
        return {
            "entity_id": entity_id,
            "period": period,
            "planned_amount": planned,
            "realized_amount": realized,
            "variance": round(variance, 2),
            "utilization": round(utilization, 4),
            "status": item.status,
        }

    # ------------------------------------------------------------------
    # Fase 4 — Issue 15: Financial Command Center
    # ------------------------------------------------------------------
    def command_center_snapshot(self) -> dict[str, Any]:
        self.ensure_default_wallets()
        wallets = self.repo.list_wallets()
        wallets_summary = [
            {
                "code": w.code,
                "name": w.name,
                "owner_entity": w.owner_entity,
                "balance": float(w.balance),
                "monthly_budget": float(w.monthly_budget or 0),
            }
            for w in wallets
        ]
        total_balance = sum(w["balance"] for w in wallets_summary)

        cashflow_snap = self.repo.latest_cashflow_snapshot("daily")
        cashflow_summary: dict[str, Any] = {}
        if cashflow_snap:
            cashflow_summary = {
                "period": cashflow_snap.period,
                "net": float(cashflow_snap.net or 0),
                "inflow": float(cashflow_snap.inflow or 0),
                "outflow": float(cashflow_snap.outflow or 0),
                "liquidity_alert": bool(cashflow_snap.liquidity_alert),
                "reference_date": str(cashflow_snap.reference_date),
            }

        budget_controls = self.repo.list_all_budget_controls()
        budget_summary = [
            {
                "entity_id": b.entity_id,
                "period": b.period,
                "planned": float(b.planned_amount or 0),
                "realized": float(b.realized_amount or 0),
                "status": b.status,
            }
            for b in budget_controls
        ]
        alerts = [b for b in budget_summary if b["status"] in {"warning", "over_budget"}]

        return {
            "snapshot_at": datetime.now(UTC).isoformat(),
            "total_balance": round(total_balance, 2),
            "wallets": wallets_summary,
            "cashflow": cashflow_summary,
            "cefeida_signal": dict(self.LAST_CEFEIDA_SIGNAL),
            "budget_controls": budget_summary,
            "budget_alerts": alerts,
            "learning_state": dict(self.LEARNING_STATE),
        }

    # ------------------------------------------------------------------
    # Fase 4 — Issue 16: Telão LICEU Sync
    # ------------------------------------------------------------------
    def liceu_sync(self, actor: RbacActor) -> dict[str, Any]:
        snapshot = self.command_center_snapshot()
        payload = {
            "event": "liceu.finance_snapshot",
            "triggered_by": actor.user_id,
            "data": snapshot,
        }
        event_bus.publish("liceu.finance_snapshot", payload)
        self.repo.add_audit(
            action="finance.liceu_sync",
            user_id=actor.user_id,
            actor_role=actor.role,
            metadata_json={"total_balance": snapshot["total_balance"]},
        )
        self.db.commit()
        return {"status": "published", "event": "liceu.finance_snapshot", "snapshot_at": snapshot["snapshot_at"]}

    # ------------------------------------------------------------------
    # Fase 4 — Issue 19: Auto Invest Engine
    # ------------------------------------------------------------------
    def auto_invest_trigger(
        self,
        actor: RbacActor,
        source_wallet: str,
        target_wallet: str,
        amount: float,
        target: str,
        expected_return: float,
        risk_score: float,
        liquidity_score: float,
        time_horizon_months: int,
    ) -> dict[str, Any]:
        # 1. Compliance gate
        compliance = self.compliance_check(
            actor=actor,
            contract_valid=True,
            legal_risk_score=risk_score,
            blocked_by_legal=False,
        )
        if not compliance["approved"]:
            return {"action": "blocked", "reason": "compliance_failed", "compliance": compliance}

        # 2. Anti-fraud gate
        source = self.repo.get_wallet_by_code(source_wallet)
        source_balance = float(source.balance) if source else 0.0
        antifraud = self.antifraud_check(
            actor=actor,
            transaction_amount=amount,
            expected_budget=source_balance,
            velocity_24h=1,
            counterpart_mismatch=False,
        )
        if antifraud["fraud_score"] >= 0.8:
            return {"action": "blocked", "reason": "antifraud_failed", "antifraud": antifraud}

        # 3. John-assisted decision
        decision = self.john_assisted_decision(
            actor=actor,
            target=target,
            amount=amount,
            expected_return=expected_return,
            risk_score=risk_score,
            liquidity_score=liquidity_score,
            time_horizon_months=time_horizon_months,
        )

        result: dict[str, Any] = {
            "action": decision["action"],
            "target": target,
            "amount": amount,
            "confidence": decision["confidence"],
            "compliance": compliance,
            "antifraud": antifraud,
            "john_decision": decision,
        }

        # 4. Execute transfer if decision is invest
        if decision["action"] == "invest":
            transfer = self.transfer(
                actor=actor,
                from_wallet_code=source_wallet,
                to_wallet_code=target_wallet,
                amount=amount,
                entity_id=target,
                entity_type="auto_invest",
                reference=f"auto-invest:{target}",
            )
            result["transfer"] = transfer
            result["executed"] = True
            event_bus.publish("finance.auto_invest_executed", result)
        else:
            result["executed"] = False

        self.repo.add_audit(
            action="finance.auto_invest_trigger",
            user_id=actor.user_id,
            actor_role=actor.role,
            metadata_json={"target": target, "amount": amount, "action": result["action"]},
        )
        self.db.commit()
        return result

    def audit_trail(
        self,
        action: str | None = None,
        user_id: str | None = None,
        limit: int = 100,
    ) -> dict[str, Any]:
        limit = max(1, min(limit, 500))
        rows = self.repo.list_audit_entries(action=action, user_id=user_id, limit=limit)
        return {
            "count": len(rows),
            "items": [
                {
                    "id": row.id,
                    "action": row.action,
                    "user_id": row.user_id,
                    "actor_role": row.actor_role,
                    "metadata": row.metadata_json,
                    "created_at": row.created_at.isoformat() if row.created_at else None,
                }
                for row in rows
            ],
        }

    def event_dispatches(
        self,
        transport: str | None = None,
        status: str | None = None,
        limit: int = 100,
    ) -> dict[str, Any]:
        limit = max(1, min(limit, 500))
        rows = fetch_event_dispatches(limit=limit, transport=transport, status=status)
        success = sum(1 for row in rows if row["status"] == "success")
        failed = sum(1 for row in rows if row["status"] == "failed")

        return {
            "count": len(rows),
            "summary": {
                "success": success,
                "failed": failed,
                "failure_rate": round((failed / len(rows)), 4) if rows else 0.0,
            },
            "items": rows,
        }

    def event_dispatch_metrics(
        self,
        window_hours: int = 24,
        transport: str | None = None,
    ) -> dict[str, Any]:
        window_hours = max(1, min(window_hours, 24 * 30))
        rows = fetch_event_dispatches(limit=5000, transport=transport)
        cutoff = datetime.now(UTC).timestamp() - (window_hours * 3600)

        filtered = []
        for row in rows:
            raw = row.get("updated_at")
            if not raw:
                continue
            try:
                dt = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
            except ValueError:
                continue
            if dt.timestamp() >= cutoff:
                filtered.append(row)

        success = sum(1 for row in filtered if row["status"] == "success")
        failed = sum(1 for row in filtered if row["status"] == "failed")
        attempts_total = sum(int(row.get("attempts") or 0) for row in filtered)
        unique_events = len({row["event_id"] for row in filtered})

        return {
            "window_hours": window_hours,
            "transport": transport or "all",
            "total_dispatches": len(filtered),
            "unique_events": unique_events,
            "success": success,
            "failed": failed,
            "failure_rate": round((failed / len(filtered)), 4) if filtered else 0.0,
            "avg_attempts": round((attempts_total / len(filtered)), 4) if filtered else 0.0,
            "generated_at": datetime.now(UTC).isoformat(),
        }

    def event_dispatch_top_failures(
        self,
        window_hours: int = 24,
        transport: str | None = None,
        limit: int = 10,
        group_by: str = "error_type",
    ) -> dict[str, Any]:
        window_hours = max(1, min(window_hours, 24 * 30))
        limit = max(1, min(limit, 100))
        if group_by not in {"error_type", "event_error", "event_name"}:
            group_by = "error_type"

        rows = fetch_event_dispatches(limit=5000, transport=transport, status="failed")
        cutoff = datetime.now(UTC).timestamp() - (window_hours * 3600)

        filtered: list[dict[str, Any]] = []
        for row in rows:
            raw = row.get("updated_at")
            if not raw:
                continue
            try:
                dt = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
            except ValueError:
                continue
            if dt.timestamp() < cutoff:
                continue

            filtered.append(row)

        event_names: dict[str, str] = {}
        if group_by in {"event_error", "event_name"}:
            for event_id in {item["event_id"] for item in filtered}:
                event_row = fetch_event_by_id(event_id=event_id)
                if event_row:
                    event_names[event_id] = event_row.get("event", "unknown_event")

        counts: dict[str, int] = {}
        meta: dict[str, dict[str, str]] = {}
        for row in filtered:
            error_key = (row.get("last_error") or "unknown_error").strip() or "unknown_error"

            if group_by == "event_error":
                event_name = event_names.get(row["event_id"], "unknown_event")
                key = f"{event_name}||{error_key}"
                meta[key] = {"event_name": event_name, "error_type": error_key}
            elif group_by == "event_name":
                event_name = event_names.get(row["event_id"], "unknown_event")
                key = event_name
                meta[key] = {"event_name": event_name}
            else:
                key = error_key
                meta[key] = {"error_type": error_key}

            counts[key] = counts.get(key, 0) + 1

        ranked = sorted(counts.items(), key=lambda item: item[1], reverse=True)[:limit]

        items: list[dict[str, Any]] = []
        total_failed = sum(counts.values())
        for key, count in ranked:
            payload = dict(meta.get(key, {}))
            payload["count"] = count
            payload["participation_pct"] = round((count / total_failed) * 100, 2) if total_failed > 0 else 0.0
            items.append(payload)

        return {
            "window_hours": window_hours,
            "transport": transport or "all",
            "group_by": group_by,
            "total_failed": total_failed,
            "top_failures": items,
            "generated_at": datetime.now(UTC).isoformat(),
        }

    def reprocess_failed_dispatch(
        self,
        actor: RbacActor,
        event_id: str,
        transport: str = "nats",
    ) -> dict[str, Any]:
        if transport != "nats":
            return {
                "event_id": event_id,
                "transport": transport,
                "before": None,
                "result": {"status": "unsupported_transport"},
            }

        dispatch = fetch_event_dispatch_status(event_id=event_id, transport=transport)
        if dispatch is None:
            return {
                "event_id": event_id,
                "transport": transport,
                "before": None,
                "result": {"status": "not_found"},
            }
        if dispatch["status"] != "failed":
            return {
                "event_id": event_id,
                "transport": transport,
                "before": dispatch,
                "result": {"status": "skipped_not_failed"},
            }

        event_row = fetch_event_by_id(event_id=event_id)
        if event_row is None:
            return {
                "event_id": event_id,
                "transport": transport,
                "before": dispatch,
                "result": {"status": "event_payload_not_found"},
            }

        try:
            result = asyncio.run(
                event_bus._nats.reprocess(
                    event_name=event_row["event"],
                    payload=event_row["payload"],
                    event_id=event_id,
                )
            )
        except RuntimeError:
            result = {"status": "failed", "event_id": event_id, "reason": "event_loop_error"}

        self.repo.add_audit(
            action="finance.dispatch_reprocessed",
            user_id=actor.user_id,
            actor_role=actor.role,
            metadata_json={
                "event_id": event_id,
                "transport": transport,
                "result": result,
            },
        )
        self.db.commit()
        return {
            "event_id": event_id,
            "transport": transport,
            "before": dispatch,
            "result": result,
        }

    # ------------------------------------------------------------------
    # Fase 4 — Issue 20: Budget Rebalancer
    # ------------------------------------------------------------------
    def budget_rebalance(self, period: str) -> dict[str, Any]:
        alerts = self.repo.list_all_budget_controls(
            period=period, status=["warning", "over_budget"]
        )
        on_track = self.repo.list_all_budget_controls(period=period, status=["on_track"])

        surplus_pool = sum(
            float(b.planned_amount or 0) - float(b.realized_amount or 0)
            for b in on_track
        )

        proposals = []
        for item in alerts:
            deficit = float(item.realized_amount or 0) - float(item.planned_amount or 0)
            deficit = max(deficit, 0.0)
            proposals.append(
                {
                    "entity_id": item.entity_id,
                    "period": item.period,
                    "status": item.status,
                    "planned": float(item.planned_amount or 0),
                    "realized": float(item.realized_amount or 0),
                    "deficit": round(deficit, 2),
                    "suggested_reallocation": round(min(deficit, surplus_pool * 0.5), 2),
                }
            )

        return {
            "period": period,
            "surplus_pool": round(surplus_pool, 2),
            "alerts_count": len(alerts),
            "proposals": proposals,
            "rebalance_feasible": surplus_pool >= sum(p["deficit"] for p in proposals),
        }

    # ------------------------------------------------------------------
    # Fase 5 — Issue 25: SLA Financeiro
    # ------------------------------------------------------------------

    def sla_create(
        self,
        actor: RbacActor,
        entity_id: str,
        task_type: str,
        priority: str,
        sla_deadline: datetime,
        metadata_json: dict | None = None,
    ) -> dict[str, Any]:
        task = self.repo.create_sla_task(
            entity_id=entity_id,
            task_type=task_type,
            priority=priority,
            sla_deadline=sla_deadline,
            status="pending",
            metadata_json=metadata_json or {},
        )
        self.repo.add_audit(
            action="finance.sla_created",
            user_id=actor.user_id,
            actor_role=actor.role,
            metadata_json={"task_id": task.id, "task_type": task_type, "priority": priority},
        )
        self.db.commit()
        return self._sla_to_dict(task)

    def sla_update_status(
        self,
        actor: RbacActor,
        task_id: str,
        new_status: str,
        breach_reason: str | None = None,
    ) -> dict[str, Any]:
        updates: dict[str, Any] = {"status": new_status}
        if new_status == "in_progress" and not self.repo.get_sla_task(task_id).started_at:
            updates["started_at"] = datetime.now(UTC)
        if new_status in {"completed", "breached", "cancelled"}:
            updates["completed_at"] = datetime.now(UTC)
        if breach_reason:
            updates["breach_reason"] = breach_reason

        task = self.repo.update_sla_task(task_id, **updates)
        if task is None:
            raise ValueError(f"SLA task {task_id} not found")

        if new_status == "breached":
            event_bus.publish("finance.sla_breached", self._sla_to_dict(task))

        self.repo.add_audit(
            action=f"finance.sla_{new_status}",
            user_id=actor.user_id,
            actor_role=actor.role,
            metadata_json={"task_id": task_id, "breach_reason": breach_reason},
        )
        self.db.commit()
        return self._sla_to_dict(task)

    def sla_list(self, entity_id: str | None = None, status: list[str] | None = None) -> dict[str, Any]:
        tasks = self.repo.list_sla_tasks(entity_id=entity_id, status=status)
        now = datetime.now(UTC)
        items = []
        for t in tasks:
            d = self._sla_to_dict(t)
            deadline = t.sla_deadline
            if deadline.tzinfo is None:
                deadline = deadline.replace(tzinfo=UTC)
            d["overdue"] = deadline < now and t.status not in {"completed", "cancelled"}
            items.append(d)
        return {"count": len(items), "items": items}

    @staticmethod
    def _sla_to_dict(task: Any) -> dict[str, Any]:
        return {
            "id": task.id,
            "entity_id": task.entity_id,
            "task_type": task.task_type,
            "priority": task.priority,
            "sla_deadline": task.sla_deadline.isoformat() if task.sla_deadline else None,
            "started_at": task.started_at.isoformat() if task.started_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            "status": task.status,
            "breach_reason": task.breach_reason,
            "metadata_json": task.metadata_json,
        }

    # ------------------------------------------------------------------
    # Fase 5 — Issue 26: Kanban Global
    # ------------------------------------------------------------------

    def kanban_create(
        self,
        actor: RbacActor,
        entity_id: str,
        title: str,
        description: str | None,
        board: str,
        column: str,
        priority: str,
        linked_sla_id: str | None = None,
        linked_entity_type: str | None = None,
        due_date: datetime | None = None,
        metadata_json: dict | None = None,
    ) -> dict[str, Any]:
        card = self.repo.create_kanban_card(
            entity_id=entity_id,
            title=title,
            description=description,
            board=board,
            column=column,
            priority=priority,
            owner_user=actor.user_id,
            linked_sla_id=linked_sla_id,
            linked_entity_type=linked_entity_type,
            due_date=due_date,
            metadata_json=metadata_json or {},
        )
        self.repo.add_audit(
            action="finance.kanban_card_created",
            user_id=actor.user_id,
            actor_role=actor.role,
            metadata_json={"card_id": card.id, "board": board, "column": column},
        )
        self.db.commit()
        return self._card_to_dict(card)

    def kanban_move(self, actor: RbacActor, card_id: str, new_column: str) -> dict[str, Any]:
        card = self.repo.move_kanban_card(card_id, new_column)
        if card is None:
            raise ValueError(f"Kanban card {card_id} not found")
        event_bus.publish("finance.kanban_card_moved", {"card_id": card_id, "column": new_column})
        self.repo.add_audit(
            action="finance.kanban_card_moved",
            user_id=actor.user_id,
            actor_role=actor.role,
            metadata_json={"card_id": card_id, "new_column": new_column},
        )
        self.db.commit()
        return self._card_to_dict(card)

    def kanban_board(self, board: str) -> dict[str, Any]:
        cards = self.repo.list_kanban_cards(board=board)
        grouped: dict[str, list] = {}
        for card in cards:
            grouped.setdefault(card.column, []).append(self._card_to_dict(card))
        return {"board": board, "columns": grouped, "total": len(cards)}

    def kanban_list(
        self, board: str | None = None, column: str | None = None, entity_id: str | None = None
    ) -> dict[str, Any]:
        cards = self.repo.list_kanban_cards(board=board, column=column, entity_id=entity_id)
        return {"count": len(cards), "items": [self._card_to_dict(c) for c in cards]}

    @staticmethod
    def _card_to_dict(card: Any) -> dict[str, Any]:
        return {
            "id": card.id,
            "entity_id": card.entity_id,
            "title": card.title,
            "description": card.description,
            "board": card.board,
            "column": card.column,
            "priority": card.priority,
            "owner_user": card.owner_user,
            "linked_sla_id": card.linked_sla_id,
            "linked_entity_type": card.linked_entity_type,
            "due_date": card.due_date.isoformat() if card.due_date else None,
            "metadata_json": card.metadata_json,
            "created_at": card.created_at.isoformat() if card.created_at else None,
        }
