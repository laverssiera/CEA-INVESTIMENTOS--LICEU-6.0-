"""finance hub accounting and budget controls

Revision ID: 0003_finance_hub_budget_controls
Revises: 0002_finance_os_foundation
Create Date: 2026-04-28

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0003_finance_hub_budget_controls"
down_revision: Union[str, None] = "0002_finance_os_foundation"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "finance_accounting_entries",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("entity_id", sa.String(length=36), nullable=False),
        sa.Column("entry_type", sa.String(length=30), nullable=False),
        sa.Column("amount", sa.Numeric(16, 2), nullable=False),
        sa.Column("tax_amount", sa.Numeric(16, 2), nullable=False, server_default="0"),
        sa.Column("due_date", sa.DateTime(), nullable=True),
        sa.Column("reference", sa.String(length=160), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="pending"),
        sa.Column("metadata_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_finance_accounting_entries_entity_id", "finance_accounting_entries", ["entity_id"])
    op.create_index("ix_finance_accounting_entries_entry_type", "finance_accounting_entries", ["entry_type"])

    op.create_table(
        "finance_budget_controls",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("entity_id", sa.String(length=36), nullable=False),
        sa.Column("period", sa.String(length=20), nullable=False),
        sa.Column("planned_amount", sa.Numeric(16, 2), nullable=False, server_default="0"),
        sa.Column("realized_amount", sa.Numeric(16, 2), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="on_track"),
        sa.Column("metadata_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_finance_budget_controls_entity_id", "finance_budget_controls", ["entity_id"])
    op.create_index("ix_finance_budget_controls_period", "finance_budget_controls", ["period"])


def downgrade() -> None:
    op.drop_index("ix_finance_budget_controls_period", table_name="finance_budget_controls")
    op.drop_index("ix_finance_budget_controls_entity_id", table_name="finance_budget_controls")
    op.drop_table("finance_budget_controls")

    op.drop_index("ix_finance_accounting_entries_entry_type", table_name="finance_accounting_entries")
    op.drop_index("ix_finance_accounting_entries_entity_id", table_name="finance_accounting_entries")
    op.drop_table("finance_accounting_entries")
