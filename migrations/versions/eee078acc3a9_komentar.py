"""komentar

Revision ID: eee078acc3a9
Revises: abbc94971459
Create Date: 2022-11-24 20:55:57.239034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eee078acc3a9'
down_revision = 'abbc94971459'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)
        batch_op.create_unique_constraint(None, ['name'])

    with op.batch_alter_table('tournament', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)
        batch_op.create_unique_constraint(None, ['name'])

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('admin', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('admin')

    with op.batch_alter_table('tournament', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)
        batch_op.drop_column('id')

    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)
        batch_op.drop_column('id')

    # ### end Alembic commands ###