"""initial

Revision ID: bc44d8010200
Revises: 
Create Date: 2026-02-17 06:44:06.848500

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc44d8010200'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('is_subscribed', sa.Boolean(), nullable=False, server_default=sa.text('true'))
    )


def downgrade() -> None:
    op.drop_column('users', 'is_subscribed')

