"""added sleepiness column

Revision ID: 52f17d88136a
Revises: 013e107d4867
Create Date: 2020-03-06 23:41:41.411386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52f17d88136a'
down_revision = '013e107d4867'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('sleepiness', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'sleepiness')
    # ### end Alembic commands ###
