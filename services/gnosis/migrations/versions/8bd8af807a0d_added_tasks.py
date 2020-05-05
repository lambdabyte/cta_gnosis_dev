"""added Tasks

Revision ID: 8bd8af807a0d
Revises: b2d22d1a1c39
Create Date: 2020-05-04 17:08:33.638235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bd8af807a0d'
down_revision = 'b2d22d1a1c39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_name', sa.String(length=120), nullable=True),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.Column('task_description', sa.String(length=256), nullable=True),
    sa.Column('task_type', sa.String(length=120), nullable=True),
    sa.Column('subject_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_due_date'), 'task', ['due_date'], unique=False)
    op.create_index(op.f('ix_task_task_name'), 'task', ['task_name'], unique=False)
    op.create_index(op.f('ix_task_task_type'), 'task', ['task_type'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_task_type'), table_name='task')
    op.drop_index(op.f('ix_task_task_name'), table_name='task')
    op.drop_index(op.f('ix_task_due_date'), table_name='task')
    op.drop_table('task')
    # ### end Alembic commands ###
