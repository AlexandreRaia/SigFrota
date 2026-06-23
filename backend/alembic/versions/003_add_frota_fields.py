"""Add frota fields to veiculos table

Revision ID: 003
Revises: 002
Create Date: 2026-06-22

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Adicionar colunas de frota
    op.add_column('veiculos', sa.Column('numero_patrimonio', sa.String(50), nullable=True))
    op.add_column('veiculos', sa.Column('valor_aquisicao', sa.Float(), nullable=True))
    op.add_column('veiculos', sa.Column('tipo_aquisicao', sa.String(20), nullable=True))
    op.add_column('veiculos', sa.Column('nome_locador', sa.String(120), nullable=True))
    op.add_column('veiculos', sa.Column('valor_locacao', sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column('veiculos', 'valor_locacao')
    op.drop_column('veiculos', 'nome_locador')
    op.drop_column('veiculos', 'tipo_aquisicao')
    op.drop_column('veiculos', 'valor_aquisicao')
    op.drop_column('veiculos', 'numero_patrimonio')
