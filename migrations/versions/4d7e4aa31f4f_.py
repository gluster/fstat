"""Add a column for branch information and index for review info

Revision ID: 4d7e4aa31f4f
Revises: 00bd302603db
Create Date: 2016-11-29 09:49:54.596197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d7e4aa31f4f'
down_revision = '00bd302603db'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('failure_instance', sa.Column('branch', sa.String(length=100), nullable=True))
    op.create_index(op.f('ix_failure_instance_branch'), 'failure_instance', ['branch'], unique=False)
    op.create_index(op.f('ix_failure_instance_review'), 'failure_instance', ['review'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_failure_instance_review'), table_name='failure_instance')
    op.drop_index(op.f('ix_failure_instance_branch'), table_name='failure_instance')
    op.drop_column('failure_instance', 'bran/h')
