"""added avatar url to Users

Revision ID: aaabb187d11e
Revises: 056b4705c0e2
Create Date: 2020-03-10 05:32:15.161623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aaabb187d11e'
down_revision = '056b4705c0e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('avatar_url', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'avatar_url')
    # ### end Alembic commands ###
