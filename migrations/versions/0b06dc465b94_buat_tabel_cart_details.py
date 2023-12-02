"""buat tabel cart_details

Revision ID: 0b06dc465b94
Revises: 7db286a7c790
Create Date: 2023-11-28 19:37:23.520753

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b06dc465b94'
down_revision = '7db286a7c790'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cart_details',
    sa.Column('id_cart', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_cart'], ['cart.id_cart'], ),
    sa.PrimaryKeyConstraint('id_cart')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cart_details')
    # ### end Alembic commands ###
