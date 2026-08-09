"""add_user_active_superuser_columns

Revision ID: add_user_cols
Revises: 0001_initial
Create Date: 2026-08-09 15:52:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_user_cols'
down_revision = '0001_initial'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'))
    op.add_column('users', sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default='false'))

def downgrade() -> None:
    op.drop_column('users', 'is_superuser')
    op.drop_column('users', 'is_active')
