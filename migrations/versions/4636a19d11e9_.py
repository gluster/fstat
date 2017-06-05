"""Add a unique constraint for url and failure_id

Revision ID: 4636a19d11e9
Revises: 52c8de6a0875
Create Date: 2016-11-21 13:33:40.846598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4636a19d11e9'
down_revision = '52c8de6a0875'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(None, 'failure_instance', ['url', 'failure_id'])


def downgrade():
    op.drop_constraint(None, 'failure_instance', type_='unique')
