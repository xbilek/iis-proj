"""tournament id

Revision ID: 933b48bf3fb8
Revises: 0885a70c7018
Create Date: 2022-11-24 21:14:26.818085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '933b48bf3fb8'
down_revision = '0885a70c7018'
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

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
