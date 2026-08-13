"""initial persistence layer

Revision ID: 0001_initial_persistence
Revises: 
Create Date: 2026-04-13

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001_initial_persistence"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(length=80), nullable=False, unique=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_users_username", "users", ["username"])
    op.create_index("ix_users_role", "users", ["role"])

    op.create_table(
        "investors",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("profile_type", sa.String(length=30), nullable=False),
        sa.Column("risk_profile", sa.String(length=30), nullable=False),
        sa.Column("kyc_status", sa.String(length=30), nullable=False),
        sa.Column("suitability_status", sa.String(length=30), nullable=False),
        sa.Column("cpf_cnpj", sa.String(length=20), nullable=True),
        sa.Column("address", sa.String(length=180), nullable=True),
        sa.Column("income_brl", sa.Numeric(14, 2), nullable=False),
        sa.Column("patrimony_brl", sa.Numeric(14, 2), nullable=False),
        sa.Column("source_of_funds", sa.String(length=180), nullable=True),
    )

    op.create_table(
        "investment_assets",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("symbol", sa.String(length=32), nullable=False, unique=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("price", sa.Numeric(14, 2), nullable=False),
        sa.Column("yield", sa.Numeric(8, 4), nullable=False),
        sa.Column("risk", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
    )

    op.create_table(
        "investment_orders",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("asset_id", sa.Integer(), sa.ForeignKey("investment_assets.id"), nullable=False),
        sa.Column("order_type", sa.String(length=10), nullable=False),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "investment_positions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("asset_id", sa.Integer(), sa.ForeignKey("investment_assets.id"), nullable=False),
        sa.Column("invested_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("expected_yield", sa.Numeric(8, 4), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "credit_requests",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("client_name", sa.String(length=120), nullable=False),
        sa.Column("cpf_cnpj", sa.String(length=20), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("project_type", sa.String(length=80), nullable=False),
        sa.Column("location", sa.String(length=120), nullable=False),
        sa.Column("requested_value", sa.Numeric(14, 2), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "treasury_transactions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("type", sa.String(length=30), nullable=False),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("source", sa.String(length=120), nullable=False),
        sa.Column("destination", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("action", sa.String(length=120), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("payload", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("location", sa.String(length=120), nullable=False),
        sa.Column("project_type", sa.String(length=80), nullable=False),
        sa.Column("total_value", sa.Numeric(14, 2), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("liceu_project_id", sa.String(length=60), nullable=True),
    )

    op.create_table(
        "ledger_entries",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("asset_id", sa.Integer(), sa.ForeignKey("investment_assets.id"), nullable=False),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("entry_type", sa.String(length=30), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "treasury_accounts",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("account_name", sa.String(length=80), nullable=False, unique=True),
        sa.Column("balance", sa.Numeric(14, 2), nullable=False),
    )

    op.create_table(
        "treasury_movements",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("from_account_id", sa.Integer(), sa.ForeignKey("treasury_accounts.id"), nullable=False),
        sa.Column("to_account_id", sa.Integer(), sa.ForeignKey("treasury_accounts.id"), nullable=False),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("treasury_movements")
    op.drop_table("treasury_accounts")
    op.drop_table("ledger_entries")
    op.drop_table("projects")
    op.drop_table("audit_logs")
    op.drop_table("treasury_transactions")
    op.drop_table("credit_requests")
    op.drop_table("investment_positions")
    op.drop_table("investment_orders")
    op.drop_table("investment_assets")
    op.drop_table("investors")
    op.drop_index("ix_users_role", table_name="users")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_table("users")
