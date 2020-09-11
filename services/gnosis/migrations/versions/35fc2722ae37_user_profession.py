"""user profession

Revision ID: 35fc2722ae37
Revises: 8bd8af807a0d
Create Date: 2020-09-04 08:33:37.141467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35fc2722ae37'
down_revision = '8bd8af807a0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('profession', sa.String(length=120), nullable=True))
    op.create_index(op.f('ix_user_profession'), 'user', ['profession'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_profession'), table_name='user')
    op.drop_column('user', 'profession')
    # ### end Alembic commands ###
