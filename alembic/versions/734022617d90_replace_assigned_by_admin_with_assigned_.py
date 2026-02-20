"""replace assigned_by_admin with assigned_by

Revision ID: 734022617d90
Revises: 6adcdb50194d
Create Date: 2026-02-20 04:59:09.993684

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '734022617d90'
down_revision: Union[str, None] = '6adcdb50194d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add completed_at column
    op.add_column('tasks', sa.Column('completed_at', sa.DateTime(), nullable=True))

    # Add assigned_by column
    op.add_column('tasks', sa.Column('assigned_by', sa.Integer(), nullable=True))

    # Create foreign key with proper name
    op.create_foreign_key(
        'fk_tasks_assigned_by_users',
        'tasks',
        'users',
        ['assigned_by'],
        ['id']
    )

    # Remove old boolean column
    op.drop_column('tasks', 'assigned_by_admin')


def downgrade() -> None:
    # Add back old column
    op.add_column(
        'tasks',
        sa.Column('assigned_by_admin', sa.Boolean(), nullable=True)
    )

    # Drop foreign key properly
    op.drop_constraint(
        'fk_tasks_assigned_by_users',
        'tasks',
        type_='foreignkey'
    )

    # Drop new columns
    op.drop_column('tasks', 'assigned_by')
    op.drop_column('tasks', 'completed_at')