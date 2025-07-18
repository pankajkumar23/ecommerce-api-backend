"""

Revision ID: 87d454e631cd
Revises: a789c9b1c279
Create Date: 2025-04-30 15:12:49.168669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87d454e631cd'
down_revision = 'a789c9b1c279'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.alter_column('payment_method',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('payment_amount',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
        batch_op.alter_column('payment_status',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.create_foreign_key(None, 'orders', ['order_id'], ['id'])

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('discount',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('discount',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('payment_status',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('payment_amount',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
        batch_op.alter_column('payment_method',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###
