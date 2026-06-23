"""Add tipo_veiculo_nome field to veiculos table

Revision ID: 002
Revises: 001
Create Date: 2026-06-22

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Adiciona coluna tipo_veiculo_nome na tabela veiculos com valor padrão 'AUTOMOVEL'
    op.add_column(
        'veiculos',
        sa.Column('tipo_veiculo_nome', sa.String(50), nullable=False, server_default='AUTOMOVEL')
    )


def downgrade() -> None:
    # Remove a coluna tipo_veiculo_nome da tabela veiculos
    op.drop_column('veiculos', 'tipo_veiculo_nome')
