"""Add a column to track patchset and review

Revision ID: 00bd302603db
Revises: 4636a19d11e9
Create Date: 2016-11-21 15:53:16.939032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00bd302603db'
down_revision = '4636a19d11e9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('failure_instance', sa.Column('patchset', sa.Integer(), nullable=True))
    op.add_column('failure_instance', sa.Column('review', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('failure_instance', 'review')
    op.drop_column('failure_instance', 'patchset')
