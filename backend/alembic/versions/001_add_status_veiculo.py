"""Add status field to veiculos table

Revision ID: 001
Revises: 
Create Date: 2026-06-22

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = '000'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Adiciona coluna status na tabela veiculos com valor padrão 'ATIVO'
    op.add_column(
        'veiculos',
        sa.Column('status', sa.String(20), nullable=False, server_default='ATIVO')
    )


def downgrade() -> None:
    # Remove a coluna status da tabela veiculos
    op.drop_column('veiculos', 'status')
