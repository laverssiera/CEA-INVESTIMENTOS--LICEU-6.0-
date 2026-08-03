"""Finance OS — Fase 5: SLA Financeiro e Kanban Global

Revision ID: 0004_finance_sla_kanban
Revises: 0003_finance_hub_budget_controls
Create Date: 2026-04-28
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0004_finance_sla_kanban"
down_revision = "0003_finance_hub_budget_controls"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "finance_sla_tasks",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("entity_id", sa.String(100), nullable=False),
        sa.Column("task_type", sa.String(60), nullable=False),
        sa.Column("priority", sa.String(20), nullable=False, server_default="normal"),
        sa.Column("sla_deadline", sa.DateTime, nullable=False),
        sa.Column("started_at", sa.DateTime, nullable=True),
        sa.Column("completed_at", sa.DateTime, nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="pending"),
        sa.Column("breach_reason", sa.Text, nullable=True),
        sa.Column("metadata_json", sa.JSON, nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_finance_sla_tasks_entity_id", "finance_sla_tasks", ["entity_id"])
    op.create_index("ix_finance_sla_tasks_task_type", "finance_sla_tasks", ["task_type"])
    op.create_index("ix_finance_sla_tasks_status", "finance_sla_tasks", ["status"])

    op.create_table(
        "finance_kanban_cards",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("entity_id", sa.String(100), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("board", sa.String(60), nullable=False, server_default="finance"),
        sa.Column("column", sa.String(60), nullable=False, server_default="backlog"),
        sa.Column("priority", sa.String(20), nullable=False, server_default="normal"),
        sa.Column("owner_user", sa.String(100), nullable=True),
        sa.Column("linked_sla_id", sa.String(36), nullable=True),
        sa.Column("linked_entity_type", sa.String(60), nullable=True),
        sa.Column("due_date", sa.DateTime, nullable=True),
        sa.Column("metadata_json", sa.JSON, nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_finance_kanban_cards_entity_id", "finance_kanban_cards", ["entity_id"])
    op.create_index("ix_finance_kanban_cards_board", "finance_kanban_cards", ["board"])
    op.create_index("ix_finance_kanban_cards_column", "finance_kanban_cards", ["column"])
    op.create_index("ix_finance_kanban_cards_linked_sla_id", "finance_kanban_cards", ["linked_sla_id"])


def downgrade() -> None:
    op.drop_table("finance_kanban_cards")
    op.drop_table("finance_sla_tasks")
