"""add civilizational and interplanetary tables

Revision ID: 0005_civilizational_infra
Revises: 0004_finance_sla_kanban
Create Date: 2026-05-10 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0005_civilizational_infra'
down_revision = '0004_finance_sla_kanban'
branch_labels = None
depends_on = None

def upgrade():
    # Scientific Funding Table
    op.create_table(
        'scientific_funding',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('project_id', sa.String(), nullable=False),
        sa.Column('funding_type', sa.String(), nullable=False),
        sa.Column('approved_amount', sa.Numeric(precision=20, scale=4), nullable=False),
        sa.Column('compliance_status', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )

    # Planetary Risk Table
    op.create_table(
        'planetary_risk',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scenario_type', sa.String(), nullable=False),
        sa.Column('risk_score', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('mitigation_plan', sa.Text()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )

    # Civilizational ESG Table
    op.create_table(
        'civilizational_esg',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('project_id', sa.String(), nullable=False),
        sa.Column('housing_score', sa.Numeric(precision=5, scale=2)),
        sa.Column('infrastructure_score', sa.Numeric(precision=5, scale=2)),
        sa.Column('environmental_score', sa.Numeric(precision=5, scale=2)),
        sa.Column('ethics_score', sa.Numeric(precision=5, scale=2)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )

    # Interplanetary Assets Table
    op.create_table(
        'interplanetary_assets',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('asset_type', sa.String(), nullable=False),
        sa.Column('valuation', sa.Numeric(precision=20, scale=4)),
        sa.Column('rwa_token', sa.String()),
        sa.Column('compliance_status', sa.String()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('interplanetary_assets')
    op.drop_table('civilizational_esg')
    op.drop_table('planetary_risk')
    op.drop_table('scientific_funding')
