"""

Revision ID: 14e1195634ee
Revises: e76ef09e2be6
Create Date: 2025-04-29 11:05:43.885103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14e1195634ee'
down_revision = 'e76ef09e2be6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment')
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

    op.create_table('payment',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], name='payment_order_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='payment_pkey')
    )
    # ### end Alembic commands ###
