"""finance os foundation

Revision ID: 0002_finance_os_foundation
Revises: 0001_initial_persistence
Create Date: 2026-04-28

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0002_finance_os_foundation"
down_revision: Union[str, None] = "0001_initial_persistence"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "finance_wallets",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("code", sa.String(length=80), nullable=False, unique=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("owner_entity", sa.String(length=80), nullable=False),
        sa.Column("wallet_type", sa.String(length=30), nullable=False, server_default="operational"),
        sa.Column("balance", sa.Numeric(16, 2), nullable=False, server_default="0"),
        sa.Column("monthly_budget", sa.Numeric(16, 2), nullable=False, server_default="0"),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_finance_wallets_code", "finance_wallets", ["code"])

    op.create_table(
        "finance_ledger_entries",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("entity_id", sa.String(length=36), nullable=False),
        sa.Column("entity_type", sa.String(length=60), nullable=False),
        sa.Column("debit_wallet_id", sa.String(length=36), sa.ForeignKey("finance_wallets.id"), nullable=False),
        sa.Column("credit_wallet_id", sa.String(length=36), sa.ForeignKey("finance_wallets.id"), nullable=False),
        sa.Column("debit_account", sa.String(length=100), nullable=False),
        sa.Column("credit_account", sa.String(length=100), nullable=False),
        sa.Column("amount", sa.Numeric(16, 2), nullable=False),
        sa.Column("reference", sa.String(length=160), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_finance_ledger_entries_entity_id", "finance_ledger_entries", ["entity_id"])
    op.create_index("ix_finance_ledger_entries_entity_type", "finance_ledger_entries", ["entity_type"])
    op.create_index("ix_finance_ledger_entries_debit_wallet_id", "finance_ledger_entries", ["debit_wallet_id"])
    op.create_index("ix_finance_ledger_entries_credit_wallet_id", "finance_ledger_entries", ["credit_wallet_id"])

    op.create_table(
        "finance_cashflow_snapshots",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("period", sa.String(length=20), nullable=False),
        sa.Column("reference_date", sa.DateTime(), nullable=False),
        sa.Column("inflow", sa.Numeric(16, 2), nullable=False, server_default="0"),
        sa.Column("outflow", sa.Numeric(16, 2), nullable=False, server_default="0"),
        sa.Column("net", sa.Numeric(16, 2), nullable=False, server_default="0"),
        sa.Column("liquidity_alert", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_finance_cashflow_snapshots_period", "finance_cashflow_snapshots", ["period"])
    op.create_index("ix_finance_cashflow_snapshots_reference_date", "finance_cashflow_snapshots", ["reference_date"])

    op.create_table(
        "finance_deal_analyses",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("entity_id", sa.String(length=36), nullable=False),
        sa.Column("entity_type", sa.String(length=60), nullable=False),
        sa.Column("expected_return", sa.Numeric(8, 4), nullable=False, server_default="0"),
        sa.Column("risk_score", sa.Numeric(8, 4), nullable=False, server_default="0"),
        sa.Column("time_horizon_months", sa.Integer(), nullable=False, server_default="12"),
        sa.Column("liquidity_score", sa.Numeric(8, 4), nullable=False, server_default="0"),
        sa.Column("final_score", sa.Numeric(8, 4), nullable=False, server_default="0"),
        sa.Column("recommendation", sa.String(length=30), nullable=False, server_default="hold"),
        sa.Column("realized_roi", sa.Numeric(8, 4), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_finance_deal_analyses_entity_id", "finance_deal_analyses", ["entity_id"])
    op.create_index("ix_finance_deal_analyses_entity_type", "finance_deal_analyses", ["entity_type"])

    op.create_table(
        "finance_audit",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("action", sa.Text(), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("actor_role", sa.String(length=40), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_finance_audit_user_id", "finance_audit", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_finance_audit_user_id", table_name="finance_audit")
    op.drop_table("finance_audit")

    op.drop_index("ix_finance_deal_analyses_entity_type", table_name="finance_deal_analyses")
    op.drop_index("ix_finance_deal_analyses_entity_id", table_name="finance_deal_analyses")
    op.drop_table("finance_deal_analyses")

    op.drop_index("ix_finance_cashflow_snapshots_reference_date", table_name="finance_cashflow_snapshots")
    op.drop_index("ix_finance_cashflow_snapshots_period", table_name="finance_cashflow_snapshots")
    op.drop_table("finance_cashflow_snapshots")

    op.drop_index("ix_finance_ledger_entries_credit_wallet_id", table_name="finance_ledger_entries")
    op.drop_index("ix_finance_ledger_entries_debit_wallet_id", table_name="finance_ledger_entries")
    op.drop_index("ix_finance_ledger_entries_entity_type", table_name="finance_ledger_entries")
    op.drop_index("ix_finance_ledger_entries_entity_id", table_name="finance_ledger_entries")
    op.drop_table("finance_ledger_entries")

    op.drop_index("ix_finance_wallets_code", table_name="finance_wallets")
    op.drop_table("finance_wallets")
