"""Add a user table

Revision ID: 576e73f71990
Revises: e9b5f1e6ad2b
Create Date: 2017-05-26 13:38:02.381969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '576e73f71990'
down_revision = 'e9b5f1e6ad2b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('profile_picture', sa.String(length=1000), nullable=True),
    sa.Column('token', sa.String(length=1000), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )


def downgrade():
    op.drop_table('user')
