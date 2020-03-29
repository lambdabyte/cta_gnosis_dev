"""moved color column to UserSubjects

Revision ID: a5fb8195fd15
Revises: df9cf377c798
Create Date: 2020-03-28 17:10:33.250436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5fb8195fd15'
down_revision = 'df9cf377c798'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subject', 'color')
    op.add_column('usersubjects', sa.Column('color', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usersubjects', 'color')
    op.add_column('subject', sa.Column('color', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
