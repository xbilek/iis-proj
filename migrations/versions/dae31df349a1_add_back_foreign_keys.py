"""add back foreign keys

Revision ID: dae31df349a1
Revises: 7cae2a487126
Create Date: 2022-11-27 13:40:30.503826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dae31df349a1'
down_revision = '7cae2a487126'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('match', schema=None) as batch_op:
        batch_op.add_column(sa.Column('team1_id', sa.String(length=150), nullable=True))
        batch_op.add_column(sa.Column('team2_id', sa.String(length=150), nullable=True))
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
