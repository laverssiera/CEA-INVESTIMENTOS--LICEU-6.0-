from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)


class Investor(Base):
    __tablename__ = "investors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    profile_type: Mapped[str] = mapped_column(String(30), nullable=False)
    risk_profile: Mapped[str] = mapped_column(String(30), nullable=False, default="moderado")
    kyc_status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    suitability_status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    cpf_cnpj: Mapped[str] = mapped_column(String(20), nullable=True)
    address: Mapped[str] = mapped_column(String(180), nullable=True)
    income_brl: Mapped[float] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    patrimony_brl: Mapped[float] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    source_of_funds: Mapped[str] = mapped_column(String(180), nullable=True)


class InvestmentAsset(Base):
    __tablename__ = "investment_assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    yield_value: Mapped[float] = mapped_column("yield", Numeric(8, 4), nullable=False)
    risk: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="open")


class InvestmentOrder(Base):
    __tablename__ = "investment_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("investment_assets.id"), nullable=False, index=True)
    order_type: Mapped[str] = mapped_column(String(10), nullable=False, default="buy")
    amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="open")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)


class InvestmentPosition(Base):
    __tablename__ = "investment_positions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("investment_assets.id"), nullable=False, index=True)
    invested_amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False, default=0)
    expected_yield: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)


class CreditRequest(Base):
    __tablename__ = "credit_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_name: Mapped[str] = mapped_column(String(120), nullable=False)
    cpf_cnpj: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    project_type: Mapped[str] = mapped_column(String(80), nullable=False)
    location: Mapped[str] = mapped_column(String(120), nullable=False)
    requested_value: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="submitted")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)


class TreasuryTransaction(Base):
    __tablename__ = "treasury_transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(30), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    source: Mapped[str] = mapped_column(String(120), nullable=False)
    destination: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    username: Mapped[str] = mapped_column(String(80), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    payload: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    location: Mapped[str] = mapped_column(String(120), nullable=False)
    project_type: Mapped[str] = mapped_column(String(80), nullable=False)
    total_value: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="planning")
    liceu_project_id: Mapped[str] = mapped_column(String(60), nullable=True)


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("investment_assets.id"), nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    entry_type: Mapped[str] = mapped_column(String(30), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)


class TreasuryAccount(Base):
    __tablename__ = "treasury_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_name: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    balance: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False, default=0)


class TreasuryMovement(Base):
    __tablename__ = "treasury_movements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    from_account_id: Mapped[int] = mapped_column(ForeignKey("treasury_accounts.id"), nullable=False)
    to_account_id: Mapped[int] = mapped_column(ForeignKey("treasury_accounts.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)


class FinanceWallet(Base):
    __tablename__ = "finance_wallets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    code: Mapped[str] = mapped_column(String(80), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    owner_entity: Mapped[str] = mapped_column(String(80), nullable=False)
    wallet_type: Mapped[str] = mapped_column(String(30), nullable=False, default="operational")
    balance: Mapped[float] = mapped_column(Numeric(16, 2), nullable=False, default=0)
    monthly_budget: Mapped[float] = mapped_column(Numeric(16, 2), nullable=False, default=0)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)


class FinanceLedgerEntry(Base):
    __tablename__ = "finance_ledger_entries"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    debit_wallet_id: Mapped[str] = mapped_column(ForeignKey("finance_wallets.id"), nullable=False, index=True)
    credit_wallet_id: Mapped[str] = mapped_column(ForeignKey("finance_wallets.id"), nullable=False, index=True)
    debit_account: Mapped[str] = mapped_column(String(100), nullable=False)
    credit_account: Mapped[str] = mapped_column(String(100), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(16, 2), nullable=False)
    reference: Mapped[str] = mapped_column(String(160), nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)


class FinanceCashflowSnapshot(Base):
    __tablename__ = "finance_cashflow_snapshots"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    period: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    reference_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    inflow: Mapped[float] = mapped_column(Numeric(16, 2), nullable=False, default=0)
    outflow: Mapped[float] = mapped_column(Numeric(16, 2), nullable=False, default=0)
    net: Mapped[float] = mapped_column(Numeric(16, 2), nullable=False, default=0)
    liquidity_alert: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)


class FinanceDealAnalysis(Base):
    __tablename__ = "finance_deal_analyses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    expected_return: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False, default=0)
    risk_score: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False, default=0)
    time_horizon_months: Mapped[int] = mapped_column(Integer, nullable=False, default=12)
    liquidity_score: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False, default=0)
    final_score: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False, default=0)
    recommendation: Mapped[str] = mapped_column(String(30), nullable=False, default="hold")
    realized_roi: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)


class FinanceAudit(Base):
    __tablename__ = "finance_audit"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    action: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    actor_role: Mapped[str] = mapped_column(String(40), nullable=False)
    metadata_json: Mapped[dict] = mapped_column("metadata", JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)


class FinanceAccountingEntry(Base):
    __tablename__ = "finance_accounting_entries"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    entry_type: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Numeric(16, 2), nullable=False)
    tax_amount: Mapped[float] = mapped_column(Numeric(16, 2), nullable=False, default=0)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    reference: Mapped[str] = mapped_column(String(160), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)


class FinanceBudgetControl(Base):
    __tablename__ = "finance_budget_controls"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    period: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    planned_amount: Mapped[float] = mapped_column(Numeric(16, 2), nullable=False, default=0)
    realized_amount: Mapped[float] = mapped_column(Numeric(16, 2), nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="on_track")
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)


# ---------------------------------------------------------------------------
# Fase 5 — Issue 25: SLA Financeiro
# ---------------------------------------------------------------------------

class FinanceSLATask(Base):
    __tablename__ = "finance_sla_tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    entity_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    task_type: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    # task_type examples: payment, reconciliation, reporting, compliance_review
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="normal")
    # priority: critical, high, normal, low
    sla_deadline: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    # status: pending, in_progress, completed, breached, cancelled
    breach_reason: Mapped[str] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)


# ---------------------------------------------------------------------------
# Fase 5 — Issue 26: Kanban Global
# ---------------------------------------------------------------------------

class FinanceKanbanCard(Base):
    __tablename__ = "finance_kanban_cards"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    entity_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    board: Mapped[str] = mapped_column(String(60), nullable=False, default="finance", index=True)
    # board: finance, operations, compliance, investments
    column: Mapped[str] = mapped_column(String(60), nullable=False, default="backlog", index=True)
    # column: backlog, in_progress, review, done, blocked
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="normal")
    owner_user: Mapped[str] = mapped_column(String(100), nullable=True)
    linked_sla_id: Mapped[str] = mapped_column(String(36), nullable=True, index=True)
    linked_entity_type: Mapped[str] = mapped_column(String(60), nullable=True)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)


class InterplanetaryDomain(Base):
    __tablename__ = "interplanetary_domains"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    domain_id: Mapped[str] = mapped_column(String(80), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    domain_type: Mapped[str] = mapped_column(String(80), nullable=False)
    subject: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="planned")
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    last_activation_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)
