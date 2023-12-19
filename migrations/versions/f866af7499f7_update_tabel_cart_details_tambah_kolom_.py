"""update tabel cart_details --> tambah kolom message

Revision ID: f866af7499f7
Revises: 29315022511d
Create Date: 2023-12-02 22:55:08.967209

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f866af7499f7'
down_revision = '29315022511d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.drop_index('id')

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