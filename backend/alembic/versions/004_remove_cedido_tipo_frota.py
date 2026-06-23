"""Remove CEDIDO from tipos_frota table.

Revision ID: 004
Revises: 003
Create Date: 2026-06-22 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Remove CEDIDO from tipos_frota."""
    # Delete CEDIDO from tipos_frota
    op.execute("DELETE FROM tipos_frota WHERE nome = 'Cedido'")


def downgrade() -> None:
    """Restore CEDIDO to tipos_frota."""
    # This is not reversible in a safe way, so we leave it empty
    pass
