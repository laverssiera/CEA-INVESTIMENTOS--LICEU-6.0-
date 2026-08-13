from __future__ import annotations

from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import (
    FinanceAccountingEntry,
    FinanceAudit,
    FinanceBudgetControl,
    FinanceCashflowSnapshot,
    FinanceDealAnalysis,
    FinanceKanbanCard,
    FinanceLedgerEntry,
    FinanceSLATask,
    FinanceWallet,
)


class FinanceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_wallet_by_code(self, code: str) -> FinanceWallet | None:
        return self.db.scalar(select(FinanceWallet).where(FinanceWallet.code == code))

    def list_wallets(self) -> list[FinanceWallet]:
        return list(self.db.scalars(select(FinanceWallet).order_by(FinanceWallet.code)).all())

    def create_wallet(self, **kwargs) -> FinanceWallet:
        wallet = FinanceWallet(**kwargs)
        self.db.add(wallet)
        self.db.flush()
        return wallet

    def create_ledger_entry(self, **kwargs) -> FinanceLedgerEntry:
        entry = FinanceLedgerEntry(**kwargs)
        self.db.add(entry)
        self.db.flush()
        return entry

    def create_cashflow_snapshot(self, **kwargs) -> FinanceCashflowSnapshot:
        snapshot = FinanceCashflowSnapshot(**kwargs)
        self.db.add(snapshot)
        self.db.flush()
        return snapshot

    def latest_cashflow_snapshot(self, period: str) -> FinanceCashflowSnapshot | None:
        return self.db.scalar(
            select(FinanceCashflowSnapshot)
            .where(FinanceCashflowSnapshot.period == period)
            .order_by(FinanceCashflowSnapshot.reference_date.desc())
        )

    def add_audit(self, **kwargs) -> FinanceAudit:
        item = FinanceAudit(**kwargs)
        self.db.add(item)
        self.db.flush()
        return item

    def list_audit_entries(
        self,
        action: str | None = None,
        user_id: str | None = None,
        limit: int = 100,
    ) -> list[FinanceAudit]:
        stmt = select(FinanceAudit).order_by(FinanceAudit.created_at.desc())
        if action:
            stmt = stmt.where(FinanceAudit.action == action)
        if user_id:
            stmt = stmt.where(FinanceAudit.user_id == user_id)
        stmt = stmt.limit(limit)
        return list(self.db.scalars(stmt).all())

    def upsert_deal_analysis(self, entity_id: str, entity_type: str, values: dict) -> FinanceDealAnalysis:
        existing = self.db.scalar(
            select(FinanceDealAnalysis)
            .where(FinanceDealAnalysis.entity_id == entity_id, FinanceDealAnalysis.entity_type == entity_type)
            .order_by(FinanceDealAnalysis.created_at.desc())
        )
        if existing is None:
            existing = FinanceDealAnalysis(entity_id=entity_id, entity_type=entity_type)
            self.db.add(existing)

        for key, value in values.items():
            setattr(existing, key, value)

        self.db.flush()
        return existing

    def ledger_sum_by_period(self, period: str) -> list[tuple[datetime, float, float]]:
        date_bucket = func.date(FinanceLedgerEntry.created_at)
        if period == "monthly":
            date_bucket = func.date(FinanceLedgerEntry.created_at, "start of month")

        rows = self.db.execute(
            select(
                date_bucket.label("bucket"),
                func.sum(FinanceLedgerEntry.amount).label("gross_amount"),
            )
            .group_by(date_bucket)
            .order_by(date_bucket)
        ).all()

        output: list[tuple[datetime, float, float]] = []
        for bucket, gross_amount in rows:
            gross = float(gross_amount or 0)
            outflow = gross / 2
            inflow = gross / 2
            output.append((bucket, inflow, outflow))

        return output

    def create_accounting_entry(self, **kwargs) -> FinanceAccountingEntry:
        entry = FinanceAccountingEntry(**kwargs)
        self.db.add(entry)
        self.db.flush()
        return entry

    def list_accounting_entries(self, entity_id: str | None = None) -> list[FinanceAccountingEntry]:
        stmt = select(FinanceAccountingEntry).order_by(FinanceAccountingEntry.created_at.desc())
        if entity_id:
            stmt = stmt.where(FinanceAccountingEntry.entity_id == entity_id)
        return list(self.db.scalars(stmt).all())

    def get_budget_control(self, entity_id: str, period: str) -> FinanceBudgetControl | None:
        return self.db.scalar(
            select(FinanceBudgetControl).where(
                FinanceBudgetControl.entity_id == entity_id,
                FinanceBudgetControl.period == period,
            )
        )

    def upsert_budget_control(
        self,
        entity_id: str,
        period: str,
        planned_amount: float | None = None,
        realized_delta: float | None = None,
        metadata_json: dict | None = None,
    ) -> FinanceBudgetControl:
        item = self.get_budget_control(entity_id=entity_id, period=period)
        if item is None:
            item = FinanceBudgetControl(entity_id=entity_id, period=period)
            self.db.add(item)

        current_planned = float(item.planned_amount or 0)
        current_realized = float(item.realized_amount or 0)

        if planned_amount is not None:
            item.planned_amount = planned_amount
            current_planned = planned_amount
        if realized_delta is not None:
            current_realized = current_realized + realized_delta
            item.realized_amount = current_realized

        planned = current_planned
        realized = current_realized
        if planned <= 0:
            item.status = "unplanned"
        elif realized <= planned:
            item.status = "on_track"
        elif realized <= planned * 1.1:
            item.status = "warning"
        else:
            item.status = "over_budget"

        if metadata_json:
            merged = dict(item.metadata_json or {})
            merged.update(metadata_json)
            item.metadata_json = merged

        self.db.flush()
        return item

    def list_all_budget_controls(
        self, period: str | None = None, status: list[str] | None = None
    ) -> list[FinanceBudgetControl]:
        stmt = select(FinanceBudgetControl).order_by(
            FinanceBudgetControl.entity_id, FinanceBudgetControl.period
        )
        if period:
            stmt = stmt.where(FinanceBudgetControl.period == period)
        if status:
            stmt = stmt.where(FinanceBudgetControl.status.in_(status))
        return list(self.db.scalars(stmt).all())

    # ------------------------------------------------------------------
    # SLA Tasks
    # ------------------------------------------------------------------
    def create_sla_task(self, **kwargs) -> FinanceSLATask:
        task = FinanceSLATask(**kwargs)
        self.db.add(task)
        self.db.flush()
        return task

    def get_sla_task(self, task_id: str) -> FinanceSLATask | None:
        return self.db.scalar(select(FinanceSLATask).where(FinanceSLATask.id == task_id))

    def list_sla_tasks(
        self, entity_id: str | None = None, status: list[str] | None = None
    ) -> list[FinanceSLATask]:
        stmt = select(FinanceSLATask).order_by(FinanceSLATask.sla_deadline)
        if entity_id:
            stmt = stmt.where(FinanceSLATask.entity_id == entity_id)
        if status:
            stmt = stmt.where(FinanceSLATask.status.in_(status))
        return list(self.db.scalars(stmt).all())

    def update_sla_task(self, task_id: str, **kwargs) -> FinanceSLATask | None:
        task = self.get_sla_task(task_id)
        if task is None:
            return None
        for key, value in kwargs.items():
            setattr(task, key, value)
        self.db.flush()
        return task

    # ------------------------------------------------------------------
    # Kanban Cards
    # ------------------------------------------------------------------
    def create_kanban_card(self, **kwargs) -> FinanceKanbanCard:
        card = FinanceKanbanCard(**kwargs)
        self.db.add(card)
        self.db.flush()
        return card

    def get_kanban_card(self, card_id: str) -> FinanceKanbanCard | None:
        return self.db.scalar(select(FinanceKanbanCard).where(FinanceKanbanCard.id == card_id))

    def list_kanban_cards(
        self,
        board: str | None = None,
        column: str | None = None,
        entity_id: str | None = None,
    ) -> list[FinanceKanbanCard]:
        stmt = select(FinanceKanbanCard).order_by(
            FinanceKanbanCard.board, FinanceKanbanCard.column, FinanceKanbanCard.created_at
        )
        if board:
            stmt = stmt.where(FinanceKanbanCard.board == board)
        if column:
            stmt = stmt.where(FinanceKanbanCard.column == column)
        if entity_id:
            stmt = stmt.where(FinanceKanbanCard.entity_id == entity_id)
        return list(self.db.scalars(stmt).all())

    def move_kanban_card(self, card_id: str, new_column: str) -> FinanceKanbanCard | None:
        card = self.get_kanban_card(card_id)
        if card is None:
            return None
        card.column = new_column
        self.db.flush()
        return card
