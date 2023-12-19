"""buat tabel cart dan cart_details

Revision ID: dc7ab549ad6c
Revises: 46be649a1773
Create Date: 2023-11-29 12:47:47.238016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc7ab549ad6c'
down_revision = '46be649a1773'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cart',
    sa.Column('id_cart', sa.Integer(), nullable=False),
    sa.Column('total_price', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id_cart')
    )
    op.create_table('cart_details',
    sa.Column('id_cart', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('sub_total', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['id_cart'], ['cart.id_cart'], ),
    sa.PrimaryKeyConstraint('id_cart')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cart_details')
    op.drop_table('cart')
    # ### end Alembic commands ###