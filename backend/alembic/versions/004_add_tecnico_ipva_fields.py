"""Add technical data and IPVA fields to Veiculo

Revision ID: 004
Revises: 003
Create Date: 2026-06-22 23:35:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add IPVA vencimento field
    op.add_column('veiculos', sa.Column('vencimento_ipva', sa.Date(), nullable=True))
    
    # Add technical data fields
    op.add_column('veiculos', sa.Column('cilindrada', sa.Integer(), nullable=True))
    op.add_column('veiculos', sa.Column('potencia', sa.Integer(), nullable=True))
    op.add_column('veiculos', sa.Column('transmissao', sa.String(20), nullable=True))
    op.add_column('veiculos', sa.Column('tracao', sa.String(10), nullable=True))
    op.add_column('veiculos', sa.Column('vidros_eletricos', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('veiculos', sa.Column('direcao', sa.String(20), nullable=True))
    op.add_column('veiculos', sa.Column('ar_condicionado', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('veiculos', sa.Column('pneu_dimensao', sa.String(20), nullable=True))
    op.add_column('veiculos', sa.Column('pneu_velocidade', sa.String(5), nullable=True))
    op.add_column('veiculos', sa.Column('pneu_carga', sa.String(5), nullable=True))


def downgrade() -> None:
    # Remove technical data fields
    op.drop_column('veiculos', 'pneu_carga')
    op.drop_column('veiculos', 'pneu_velocidade')
    op.drop_column('veiculos', 'pneu_dimensao')
    op.drop_column('veiculos', 'ar_condicionado')
    op.drop_column('veiculos', 'direcao')
    op.drop_column('veiculos', 'vidros_eletricos')
    op.drop_column('veiculos', 'tracao')
    op.drop_column('veiculos', 'transmissao')
    op.drop_column('veiculos', 'potencia')
    op.drop_column('veiculos', 'cilindrada')
    
    # Remove IPVA field
    op.drop_column('veiculos', 'vencimento_ipva')
