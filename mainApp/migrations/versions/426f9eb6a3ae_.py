"""

Revision ID: 426f9eb6a3ae
Revises: ab3101e71564
Create Date: 2025-04-24 16:32:27.894466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '426f9eb6a3ae'
down_revision = 'ab3101e71564'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('discount', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_column('discount')

    # ### end Alembic commands ###
