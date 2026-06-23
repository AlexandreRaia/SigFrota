"""Create base veiculos table

Revision ID: 000
Revises: 
Create Date: 2026-06-22

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Criar tabela veiculos com todas as colunas básicas
    op.create_table(
        'veiculos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('placa', sa.String(20), nullable=False),
        sa.Column('prefixo', sa.String(50), nullable=True),
        sa.Column('chassi', sa.String(17), nullable=False),
        sa.Column('renavam', sa.String(11), nullable=False),
        sa.Column('marca_id', sa.Integer(), nullable=False),
        sa.Column('modelo_id', sa.Integer(), nullable=False),
        sa.Column('tipo_veiculo_id', sa.Integer(), nullable=False),
        sa.Column('categoria_id', sa.Integer(), nullable=False),
        sa.Column('tipo_frota_id', sa.Integer(), nullable=False),
        sa.Column('ano_fabricacao', sa.Integer(), nullable=True),
        sa.Column('cor', sa.String(50), nullable=True),
        sa.Column('combustivel', sa.String(50), nullable=True),
        sa.Column('operacional', sa.String(20), nullable=True),
        sa.Column('observacoes', sa.Text(), nullable=True),
        sa.Column('data_criacao', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('data_atualizacao', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_veiculos_placa'), 'veiculos', ['placa'], unique=True)
    op.create_index(op.f('ix_veiculos_marca_id'), 'veiculos', ['marca_id'])
    op.create_index(op.f('ix_veiculos_modelo_id'), 'veiculos', ['modelo_id'])


def downgrade() -> None:
    op.drop_table('veiculos')
