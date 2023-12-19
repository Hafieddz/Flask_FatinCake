"""membuat tabel role dan menghubungkan dengan tabel user

Revision ID: f8dae0767822
Revises: f43fcb7eabad
Create Date: 2023-10-30 22:50:29.870273

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8dae0767822'
down_revision = 'f43fcb7eabad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password_hash', sa.String(length=220), nullable=False),
    sa.Column('nama_depan', sa.String(length=30), nullable=False),
    sa.Column('nama_belakang', sa.String(length=30), nullable=True),
    sa.Column('no_telp', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('roles', sa.String(length=20), server_default='user', nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('role')
    op.drop_table('users')
    # ### end Alembic commands ###
