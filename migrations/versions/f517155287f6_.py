"""

Revision ID: f517155287f6
Revises: 7514a613b106
Create Date: 2018-08-16 16:25:32.980947

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f517155287f6'
down_revision = '7514a613b106'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('bug_failure', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.add_column('failure', sa.Column('type', sa.Integer(), nullable=True, default=0))
    op.drop_column('failure', 'state')


def downgrade():
    op.add_column('failure', sa.Column('state', sa.INTEGER(),
        autoincrement=False, nullable=True))
    op.drop_column('failure', 'type')
    op.alter_column('bug_failure', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
