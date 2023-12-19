"""buat tabel cart dan cart_details

Revision ID: f3978f7bb595
Revises: 4dca81a3dd3d
Create Date: 2023-11-29 13:58:33.210769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3978f7bb595'
down_revision = '4dca81a3dd3d'
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
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_cart', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('sub_total', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['id_cart'], ['cart.id_cart'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cart_details')
    op.drop_table('cart')
    # ### end Alembic commands ###
