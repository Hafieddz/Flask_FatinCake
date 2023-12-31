"""update tabel cart_details --> tambah kolom message

Revision ID: 13e8517f5941
Revises: c1acb6c5233d
Create Date: 2023-12-02 22:56:42.963842

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13e8517f5941'
down_revision = 'c1acb6c5233d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart_details', schema=None) as batch_op:
        batch_op.add_column(sa.Column('message', sa.Text(), nullable=False))
        batch_op.create_foreign_key(None, 'cake', ['id_kue'], ['id_kue'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart_details', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('message')

    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.create_index('id', ['user_id'], unique=False)

    # ### end Alembic commands ###
