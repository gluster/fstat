"""Add an index for failure_instance url

Revision ID: e9b5f1e6ad2b
Revises: 4d7e4aa31f4f
Create Date: 2017-05-26 13:37:05.984056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9b5f1e6ad2b'
down_revision = '4d7e4aa31f4f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(op.f('ix_failure_instance_url'), 'failure_instance', ['url'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_failure_instance_url'), table_name='failure_instance')
