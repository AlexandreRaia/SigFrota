"""Adiciona tabela condutor_documentos

Revision ID: 006
Revises: 005
Create Date: 2026-07-09

"""
from alembic import op
import sqlalchemy as sa


revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'condutor_documentos',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('condutor_id', sa.Integer(), sa.ForeignKey('condutores.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('tipo', sa.String(30), nullable=False),
        sa.Column('arquivo', sa.String(255), nullable=False),
        sa.Column('descricao', sa.String(200), nullable=False, server_default=''),
        sa.Column('criado_em', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column('atualizado_em', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp()),
    )


def downgrade() -> None:
    op.drop_table('condutor_documentos')
