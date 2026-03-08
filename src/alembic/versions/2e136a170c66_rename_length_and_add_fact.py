"""rename_length_and_add_fact

Revision ID: 2e136a170c66
Revises: 51d4b3b68b11
Create Date: 2026-03-08 17:02:46.013476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e136a170c66'
down_revision: Union[str, Sequence[str], None] = '51d4b3b68b11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('cards', 'total_length', new_column_name='total_length_balance')
    op.add_column('cards', sa.Column('total_length_fact', sa.Float(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('cards', 'total_length_fact')
    op.alter_column('cards', 'total_length_balance', new_column_name='total_length')
