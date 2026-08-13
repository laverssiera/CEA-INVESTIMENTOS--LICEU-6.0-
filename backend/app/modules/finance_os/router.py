from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.finance_service import FinanceService, RbacActor

router = APIRouter(tags=["Finance OS"])


class WalletTransferInput(BaseModel):
    from_wallet: str
    to_wallet: str
    amount: float = Field(gt=0)
    entity_id: str = "cea-core"
    entity_type: str = "monolith"
    reference: str = "wallet-transfer"


class InvestInput(BaseModel):
    source_wallet: str = "CEA_MASTER"
    target_wallet: str = "ARCHIMEDES_OPER"
    amount: float = Field(gt=0)
    target: str
    expected_return: float = Field(ge=-1, le=5)
    risk_score: float = Field(ge=0, le=1)
    liquidity_score: float = Field(ge=0, le=1)
    time_horizon_months: int = Field(gt=0, le=120)


class ConsumeEventInput(BaseModel):
    event_name: str
    payload: dict[str, Any] = Field(default_factory=dict)


class CefeidaFeedInput(BaseModel):
    market_trend: str = Field(default="neutral")
    demand_index: float = Field(ge=0, le=1)
    risk_outlook: float = Field(ge=0, le=1)
    forecast_confidence: float = Field(ge=0, le=1)


class JohnDecisionInput(BaseModel):
    target: str
    amount: float = Field(gt=0)
    expected_return: float = Field(ge=-1, le=5)
    risk_score: float = Field(ge=0, le=1)
    liquidity_score: float = Field(ge=0, le=1)
    time_horizon_months: int = Field(gt=0, le=120)


class LearningFeedbackInput(BaseModel):
    target: str
    invested_amount: float = Field(gt=0)
    realized_return: float


class ComplianceCheckInput(BaseModel):
    contract_valid: bool
    legal_risk_score: float = Field(ge=0, le=1)
    blocked_by_legal: bool = False


class AntifraudInput(BaseModel):
    transaction_amount: float = Field(gt=0)
    expected_budget: float = Field(gt=0)
    velocity_24h: int = Field(ge=0)
    counterpart_mismatch: bool = False


class IntelligenceOutputInput(BaseModel):
    entity_id: str
    roi: float
    risk_score: float = Field(ge=0, le=1)
    liquidity_alert: bool = False
    compliance_blocked: bool = False


class AccountingEntryInput(BaseModel):
    entity_id: str
    entry_type: str = Field(pattern="^(accounts_payable|accounts_receivable|tax)$")
    amount: float = Field(ge=0)
    tax_amount: float = Field(ge=0, default=0)
    reference: str
    status: str = "pending"


class BudgetSetInput(BaseModel):
    entity_id: str
    period: str = Field(default="monthly")
    planned_amount: float = Field(ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class BudgetExecutionInput(BaseModel):
    entity_id: str
    period: str = Field(default="monthly")
    realized_delta: float
    reason: str = "execution"


class ReprocessDispatchInput(BaseModel):
    event_id: str
    transport: str = "nats"


def _actor(user_id: str | None, role: str | None) -> RbacActor:
    return RbacActor(user_id=user_id or "system", role=(role or "cfo").lower())


def _require_finance_role(actor: RbacActor, allowed: set[str]) -> None:
    if actor.role not in allowed:
        raise HTTPException(status_code=403, detail="Role not allowed")


@router.get("/wallets")
def list_wallets(db: Session = Depends(get_db)) -> dict[str, Any]:
    service = FinanceService(db)
    service.ensure_default_wallets()
    return {"items": service.list_wallets()}


@router.post("/wallet/transfer")
def wallet_transfer(
    payload: WalletTransferInput,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor"})
    service = FinanceService(db)
    service.ensure_default_wallets()
    try:
        result = service.transfer(
            actor=actor,
            from_wallet_code=payload.from_wallet,
            to_wallet_code=payload.to_wallet,
            amount=payload.amount,
            entity_id=payload.entity_id,
            entity_type=payload.entity_type,
            reference=payload.reference,
        )
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/finance/cashflow")
def finance_cashflow(period: str = "daily", db: Session = Depends(get_db)) -> dict[str, Any]:
    service = FinanceService(db)
    if period not in {"daily", "monthly"}:
        raise HTTPException(status_code=400, detail="period must be daily or monthly")
    service.ensure_default_wallets()
    return service.cashflow(period=period)


@router.get("/finance/roi/{entity_id}")
def finance_roi(
    entity_id: str,
    investment_amount: float = 100_000,
    current_value: float = 120_000,
    discount_rate: float = 0.01,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    service = FinanceService(db)
    monthly_cashflows = [investment_amount * 0.03 for _ in range(12)]
    try:
        return service.roi_metrics(
            entity_id=entity_id,
            investment_amount=investment_amount,
            current_value=current_value,
            monthly_cashflows=monthly_cashflows,
            discount_rate=discount_rate,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/finance/invest")
def finance_invest(
    payload: InvestInput,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor", "analista"})
    service = FinanceService(db)
    service.ensure_default_wallets()
    try:
        return service.invest_decision(
            actor=actor,
            source_wallet_code=payload.source_wallet,
            target_wallet_code=payload.target_wallet,
            amount=payload.amount,
            target=payload.target,
            expected_return=payload.expected_return,
            risk_score=payload.risk_score,
            liquidity_score=payload.liquidity_score,
            time_horizon_months=payload.time_horizon_months,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/finance/events/consume")
def consume_finance_event(
    payload: ConsumeEventInput,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor", "analista"})
    service = FinanceService(db)
    try:
        return service.consume_external_event(actor=actor, event_name=payload.event_name, payload=payload.payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/finance/cefeida/feed")
def ingest_cefeida_feed(
    payload: CefeidaFeedInput,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor", "analista"})
    service = FinanceService(db)
    return service.ingest_cefeida_feed(
        actor=actor,
        market_trend=payload.market_trend,
        demand_index=payload.demand_index,
        risk_outlook=payload.risk_outlook,
        forecast_confidence=payload.forecast_confidence,
    )


@router.post("/finance/john/decision")
def finance_john_decision(
    payload: JohnDecisionInput,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor", "analista"})
    service = FinanceService(db)
    return service.john_assisted_decision(
        actor=actor,
        target=payload.target,
        amount=payload.amount,
        expected_return=payload.expected_return,
        risk_score=payload.risk_score,
        liquidity_score=payload.liquidity_score,
        time_horizon_months=payload.time_horizon_months,
    )


@router.post("/finance/learning/feedback")
def finance_learning_feedback(
    payload: LearningFeedbackInput,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor", "analista"})
    service = FinanceService(db)
    try:
        return service.register_learning_feedback(
            actor=actor,
            target=payload.target,
            invested_amount=payload.invested_amount,
            realized_return=payload.realized_return,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/finance/compliance/check")
def finance_compliance_check(
    payload: ComplianceCheckInput,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor", "analista"})
    service = FinanceService(db)
    return service.compliance_check(
        actor=actor,
        contract_valid=payload.contract_valid,
        legal_risk_score=payload.legal_risk_score,
        blocked_by_legal=payload.blocked_by_legal,
    )


@router.post("/finance/antifraud/check")
def finance_antifraud_check(
    payload: AntifraudInput,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor", "analista"})
    service = FinanceService(db)
    return service.antifraud_check(
        actor=actor,
        transaction_amount=payload.transaction_amount,
        expected_budget=payload.expected_budget,
        velocity_24h=payload.velocity_24h,
        counterpart_mismatch=payload.counterpart_mismatch,
    )


@router.post("/finance/intelligence/output")
def finance_intelligence_output(payload: IntelligenceOutputInput, db: Session = Depends(get_db)) -> dict[str, Any]:
    service = FinanceService(db)
    return service.intelligence_output(
        entity_id=payload.entity_id,
        roi=payload.roi,
        risk_score=payload.risk_score,
        liquidity_alert=payload.liquidity_alert,
        compliance_blocked=payload.compliance_blocked,
    )

@router.get("/finance/audit")
def finance_audit_trail(
    action: str | None = None,
    user_id: str | None = None,
    limit: int = 100,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor", "analista"})
    service = FinanceService(db)
    return service.audit_trail(action=action, user_id=user_id, limit=limit)


@router.get("/finance/events/dispatches")
def finance_event_dispatches(
    transport: str | None = None,
    status: str | None = None,
    limit: int = 100,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor", "analista"})
    service = FinanceService(db)
    return service.event_dispatches(transport=transport, status=status, limit=limit)


@router.get("/finance/events/dispatches/metrics")
def finance_event_dispatches_metrics(
    window_hours: int = 24,
    transport: str | None = None,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor", "analista"})
    service = FinanceService(db)
    return service.event_dispatch_metrics(window_hours=window_hours, transport=transport)


@router.get("/finance/events/dispatches/top-failures")
def finance_event_dispatches_top_failures(
    window_hours: int = 24,
    transport: str | None = None,
    limit: int = 10,
    group_by: str = "error_type",
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor", "analista"})
    service = FinanceService(db)
    return service.event_dispatch_top_failures(
        window_hours=window_hours,
        transport=transport,
        limit=limit,
        group_by=group_by,
    )


@router.post("/finance/events/dispatches/reprocess")
def finance_event_dispatches_reprocess(
    payload: ReprocessDispatchInput,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor"})
    service = FinanceService(db)
    return service.reprocess_failed_dispatch(
        actor=actor,
        event_id=payload.event_id,
        transport=payload.transport,
    )


@router.post("/finance/accounting/register")
def finance_accounting_register(
    payload: AccountingEntryInput,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor", "analista"})
    service = FinanceService(db)
    try:
        return service.accounting_register(
            actor=actor,
            entity_id=payload.entity_id,
            entry_type=payload.entry_type,
            amount=payload.amount,
            tax_amount=payload.tax_amount,
            reference=payload.reference,
            status=payload.status,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/finance/accounting/report")
def finance_accounting_report(entity_id: str | None = None, db: Session = Depends(get_db)) -> dict[str, Any]:
    service = FinanceService(db)
    return service.accounting_report(entity_id=entity_id)


@router.post("/finance/accounting/sync-hub")
def finance_accounting_sync_hub(
    entity_id: str | None = None,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor"})
    service = FinanceService(db)
    return service.accounting_sync_hub(actor=actor, entity_id=entity_id)


@router.post("/finance/budget/set")
def finance_budget_set(
    payload: BudgetSetInput,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor"})
    service = FinanceService(db)
    try:
        return service.budget_set(
            actor=actor,
            entity_id=payload.entity_id,
            period=payload.period,
            planned_amount=payload.planned_amount,
            metadata_json=payload.metadata,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/finance/budget/execute")
def finance_budget_execute(
    payload: BudgetExecutionInput,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor", "analista"})
    service = FinanceService(db)
    return service.budget_register_execution(
        actor=actor,
        entity_id=payload.entity_id,
        period=payload.period,
        realized_delta=payload.realized_delta,
        reason=payload.reason,
    )


@router.get("/finance/budget/status")
def finance_budget_status(entity_id: str, period: str = "monthly", db: Session = Depends(get_db)) -> dict[str, Any]:
    service = FinanceService(db)
    return service.budget_status(entity_id=entity_id, period=period)


# ---------------------------------------------------------------------------
# Fase 4 — Issue 15: Financial Command Center
# ---------------------------------------------------------------------------

@router.get("/finance/command-center")
def finance_command_center(db: Session = Depends(get_db)) -> dict[str, Any]:
    service = FinanceService(db)
    return service.command_center_snapshot()


# ---------------------------------------------------------------------------
# Fase 4 — Issue 16: Telão LICEU Sync
# ---------------------------------------------------------------------------

@router.post("/finance/liceu/sync")
def finance_liceu_sync(
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor"})
    service = FinanceService(db)
    return service.liceu_sync(actor=actor)


# ---------------------------------------------------------------------------
# Fase 4 — Issue 19: Auto Invest Engine
# ---------------------------------------------------------------------------

class AutoInvestInput(BaseModel):
    source_wallet: str = "CEA_MASTER"
    target_wallet: str = "ARCHIMEDES_OPER"
    amount: float = Field(gt=0)
    target: str
    expected_return: float = Field(ge=-1, le=5)
    risk_score: float = Field(ge=0, le=1)
    liquidity_score: float = Field(ge=0, le=1)
    time_horizon_months: int = Field(gt=0, le=120)


@router.post("/finance/auto-invest/trigger")
def finance_auto_invest(
    payload: AutoInvestInput,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor"})
    service = FinanceService(db)
    return service.auto_invest_trigger(
        actor=actor,
        source_wallet=payload.source_wallet,
        target_wallet=payload.target_wallet,
        amount=payload.amount,
        target=payload.target,
        expected_return=payload.expected_return,
        risk_score=payload.risk_score,
        liquidity_score=payload.liquidity_score,
        time_horizon_months=payload.time_horizon_months,
    )


# ---------------------------------------------------------------------------
# Fase 4 — Issue 20: Budget Rebalancer
# ---------------------------------------------------------------------------

@router.get("/finance/budget/rebalance")
def finance_budget_rebalance(period: str = "2026-04", db: Session = Depends(get_db)) -> dict[str, Any]:
    service = FinanceService(db)
    return service.budget_rebalance(period=period)


# ---------------------------------------------------------------------------
# Fase 5 — Issue 25: SLA Financeiro
# ---------------------------------------------------------------------------

class SLACreateInput(BaseModel):
    entity_id: str
    task_type: str
    priority: str = "normal"
    sla_deadline: str  # ISO datetime string
    metadata: dict[str, Any] = Field(default_factory=dict)


class SLAUpdateInput(BaseModel):
    task_id: str
    new_status: str
    breach_reason: str | None = None


@router.post("/finance/sla/create")
def finance_sla_create(
    payload: SLACreateInput,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    from datetime import datetime as _dt
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor", "analista"})
    service = FinanceService(db)
    try:
        deadline = _dt.fromisoformat(payload.sla_deadline)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid sla_deadline: {exc}") from exc
    return service.sla_create(
        actor=actor,
        entity_id=payload.entity_id,
        task_type=payload.task_type,
        priority=payload.priority,
        sla_deadline=deadline,
        metadata_json=payload.metadata,
    )


@router.post("/finance/sla/update")
def finance_sla_update(
    payload: SLAUpdateInput,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor", "analista"})
    service = FinanceService(db)
    try:
        return service.sla_update_status(
            actor=actor,
            task_id=payload.task_id,
            new_status=payload.new_status,
            breach_reason=payload.breach_reason,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/finance/sla/list")
def finance_sla_list(
    entity_id: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    service = FinanceService(db)
    status_filter = status.split(",") if status else None
    return service.sla_list(entity_id=entity_id, status=status_filter)


# ---------------------------------------------------------------------------
# Fase 5 — Issue 26: Kanban Global
# ---------------------------------------------------------------------------

class KanbanCreateInput(BaseModel):
    entity_id: str
    title: str
    description: str | None = None
    board: str = "finance"
    column: str = "backlog"
    priority: str = "normal"
    linked_sla_id: str | None = None
    linked_entity_type: str | None = None
    due_date: str | None = None  # ISO datetime
    metadata: dict[str, Any] = Field(default_factory=dict)


class KanbanMoveInput(BaseModel):
    card_id: str
    new_column: str


@router.post("/finance/kanban/create")
def finance_kanban_create(
    payload: KanbanCreateInput,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    from datetime import datetime as _dt
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor", "analista"})
    service = FinanceService(db)
    due = None
    if payload.due_date:
        try:
            due = _dt.fromisoformat(payload.due_date)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=f"Invalid due_date: {exc}") from exc
    return service.kanban_create(
        actor=actor,
        entity_id=payload.entity_id,
        title=payload.title,
        description=payload.description,
        board=payload.board,
        column=payload.column,
        priority=payload.priority,
        linked_sla_id=payload.linked_sla_id,
        linked_entity_type=payload.linked_entity_type,
        due_date=due,
        metadata_json=payload.metadata,
    )


@router.post("/finance/kanban/move")
def finance_kanban_move(
    payload: KanbanMoveInput,
    db: Session = Depends(get_db),
    x_finance_user: str | None = Header(default=None),
    x_finance_role: str | None = Header(default=None),
) -> dict[str, Any]:
    actor = _actor(x_finance_user, x_finance_role)
    _require_finance_role(actor, {"cfo", "gestor", "analista"})
    service = FinanceService(db)
    try:
        return service.kanban_move(actor=actor, card_id=payload.card_id, new_column=payload.new_column)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/finance/kanban/board")
def finance_kanban_board(board: str = "finance", db: Session = Depends(get_db)) -> dict[str, Any]:
    service = FinanceService(db)
    return service.kanban_board(board=board)


@router.get("/finance/kanban/list")
def finance_kanban_list(
    board: str | None = None,
    column: str | None = None,
    entity_id: str | None = None,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    service = FinanceService(db)
    return service.kanban_list(board=board, column=column, entity_id=entity_id)
