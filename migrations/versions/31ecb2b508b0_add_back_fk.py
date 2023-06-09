"""add back fk

Revision ID: 31ecb2b508b0
Revises: dae31df349a1
Create Date: 2022-11-27 13:44:37.840397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31ecb2b508b0'
down_revision = 'dae31df349a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('match', schema=None) as batch_op:
        batch_op.add_column(sa.Column('team1_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('team2_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'team', ['team1_id'], ['id'])
        batch_op.create_foreign_key(None, 'team', ['team2_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('match', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('team2_id')
        batch_op.drop_column('team1_id')

    # ### end Alembic commands ###
