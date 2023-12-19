"""update pass

Revision ID: b782a777a720
Revises: 6838f28d938f
Create Date: 2023-10-23 01:21:22.365721

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b782a777a720'
down_revision = '6838f28d938f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=mysql.VARCHAR(length=150),
               type_=sa.String(length=220),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=220),
               type_=mysql.VARCHAR(length=150),
               existing_nullable=False)

    # ### end Alembic commands ###