"""Update condutor lotacao: secretaria_id/unidade(str) -> unidade_id/subunidade_id(FK)

Revision ID: 007
Revises: 006
Create Date: 2026-07-09

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # SQLite requer batch_alter_table para DROP COLUMN com FK
    with op.batch_alter_table('condutores') as batch_op:
        batch_op.drop_column('secretaria_id')
        batch_op.drop_column('unidade')
        batch_op.add_column(sa.Column('unidade_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('subunidade_id', sa.Integer(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('condutores') as batch_op:
        batch_op.drop_column('subunidade_id')
        batch_op.drop_column('unidade_id')
        batch_op.add_column(sa.Column('unidade', sa.String(100), nullable=True, server_default=''))
        batch_op.add_column(sa.Column('secretaria_id', sa.Integer(), nullable=True))
