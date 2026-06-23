"""Recreate veiculos table with full schema

Revision ID: 004
Revises: 003
Create Date: 2026-06-22

"""
from alembic import op
import sqlalchemy as sa


revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table('veiculos')

    op.create_table(
        'veiculos',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),

        # DADOS GERAIS
        sa.Column('placa', sa.String(10), nullable=False, unique=True),
        sa.Column('chassi', sa.String(17), nullable=False, unique=True),
        sa.Column('renavam', sa.String(11), nullable=False, unique=True),
        sa.Column('marca_id', sa.Integer(), sa.ForeignKey('marcas.id'), nullable=False),
        sa.Column('modelo_id', sa.Integer(), sa.ForeignKey('modelos.id'), nullable=False),
        sa.Column('ano_fabricacao', sa.SmallInteger(), nullable=False),
        sa.Column('ano_modelo', sa.SmallInteger(), nullable=True),
        sa.Column('cor', sa.String(30), nullable=False, server_default=''),
        sa.Column('combustivel', sa.String(12), nullable=False, server_default='FLEX'),
        sa.Column('motorizacao', sa.String(80), nullable=False, server_default=''),
        sa.Column('observacoes', sa.String(500), nullable=False, server_default=''),
        sa.Column('situacao', sa.String(10), nullable=False, server_default='ATIVO'),

        # CLASSIFICAÇÃO DA FROTA
        sa.Column('prefixo', sa.String(20), nullable=True, unique=True),
        sa.Column('tipo_frota_id', sa.Integer(), sa.ForeignKey('tipos_frota.id'), nullable=False),
        sa.Column('categoria_id', sa.Integer(), sa.ForeignKey('categorias.id'), nullable=False),
        sa.Column('numero_patrimonio', sa.String(50), nullable=True),
        sa.Column('valor_aquisicao', sa.Float(), nullable=True),
        sa.Column('tipo_aquisicao', sa.String(20), nullable=True),
        sa.Column('tipo_convenio', sa.String(20), nullable=True),
        sa.Column('nome_locador', sa.String(120), nullable=True),
        sa.Column('valor_locacao', sa.Float(), nullable=True),

        # VINCULAÇÃO ADMINISTRATIVA
        sa.Column('secretaria_id', sa.Integer(), sa.ForeignKey('secretarias.id'), nullable=True),
        sa.Column('unidade_id', sa.Integer(), sa.ForeignKey('unidades.id'), nullable=True),
        sa.Column('subunidade_id', sa.Integer(), sa.ForeignKey('subunidades.id'), nullable=True),
        sa.Column('centro_custo_id', sa.Integer(), sa.ForeignKey('centros_custo.id'), nullable=True),

        # DADOS OPERACIONAIS
        sa.Column('tipo_registro_id', sa.Integer(), sa.ForeignKey('tipos_veiculo.id'), nullable=True),
        sa.Column('tipo_controle', sa.String(20), nullable=False, server_default='QUILOMETRAGEM'),
        sa.Column('hodometro_horimetro_inicial', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('capacidade_tanque', sa.Integer(), nullable=True),
        sa.Column('capacidade_passageiros', sa.Integer(), nullable=True),
        sa.Column('capacidade_carga', sa.Integer(), nullable=True),

        # DOCUMENTAÇÃO
        sa.Column('vencimento_licenciamento', sa.Date(), nullable=True),
        sa.Column('vencimento_seguro', sa.Date(), nullable=True),
        sa.Column('vencimento_ipva', sa.Date(), nullable=True),

        # DADOS TÉCNICOS
        sa.Column('cilindrada', sa.Integer(), nullable=True),
        sa.Column('potencia', sa.Integer(), nullable=True),
        sa.Column('transmissao', sa.String(20), nullable=True),
        sa.Column('tracao', sa.String(10), nullable=True),
        sa.Column('vidros_eletricos', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('direcao', sa.String(20), nullable=True),
        sa.Column('ar_condicionado', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('pneu_dimensao', sa.String(20), nullable=True),
        sa.Column('pneu_velocidade', sa.String(5), nullable=True),
        sa.Column('pneu_carga', sa.String(5), nullable=True),

        # LOCALIZAÇÃO
        sa.Column('uf', sa.String(2), nullable=False, server_default='SP'),
        sa.Column('municipio', sa.String(120), nullable=False, server_default=''),

        # TIMESTAMPS
        sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('atualizado_em', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_index('ix_veiculos_placa', 'veiculos', ['placa'], unique=True)
    op.create_index('ix_veiculos_prefixo', 'veiculos', ['prefixo'], unique=True)


def downgrade() -> None:
    op.drop_table('veiculos')
