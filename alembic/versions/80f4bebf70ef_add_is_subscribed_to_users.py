"""add is_subscribed to users

Revision ID: 80f4bebf70ef
Revises: bc44d8010200
Create Date: 2026-02-19 03:10:03.807109

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80f4bebf70ef'
down_revision: Union[str, None] = 'bc44d8010200'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('is_subscribed', sa.Boolean(), nullable=False, server_default=sa.text('true'))
    )

def downgrade() -> None:
    op.drop_column('users', 'is_subscribed')
