"""Initial conversion to alembic

Revision ID: 52c8de6a0875
Revises:
Create Date: 2016-11-21 12:46:43.870241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52c8de6a0875'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('failure',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('signature', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_failure_signature'), 'failure', ['signature'], unique=False)
    op.create_table('failure_instance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=100), nullable=True),
    sa.Column('state', sa.Integer(), nullable=True),
    sa.Column('job_name', sa.String(length=100), nullable=True),
    sa.Column('node', sa.String(length=100), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('failure_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['failure_id'], ['failure.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_failure_instance_job_name'), 'failure_instance', ['job_name'], unique=False)
    op.create_index(op.f('ix_failure_instance_node'), 'failure_instance', ['node'], unique=False)
    op.create_index(op.f('ix_failure_instance_timestamp'), 'failure_instance', ['timestamp'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_failure_instance_timestamp'), table_name='failure_instance')
    op.drop_index(op.f('ix_failure_instance_node'), table_name='failure_instance')
    op.drop_index(op.f('ix_failure_instance_job_name'), table_name='failure_instance')
    op.drop_table('failure_instance')
    op.drop_index(op.f('ix_failure_signature'), table_name='failure')
    op.drop_table('failure')
