"""Make prefixo column nullable in veiculos table.

Revision ID: 005
Revises: 004
Create Date: 2026-06-22 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Make prefixo nullable in veiculos table."""
    with op.batch_alter_table('veiculos', schema=None) as batch_op:
        batch_op.alter_column('prefixo',
                   existing_type=sa.String(20),
                   nullable=True)


def downgrade() -> None:
    """Revert prefixo back to non-nullable."""
    with op.batch_alter_table('veiculos', schema=None) as batch_op:
        batch_op.alter_column('prefixo',
                   existing_type=sa.String(20),
                   nullable=False)
