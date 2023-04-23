"""fk match

Revision ID: b13358e3cf0b
Revises: 19a3886442ea
Create Date: 2022-11-24 22:09:28.397134

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b13358e3cf0b'
down_revision = '19a3886442ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.add_column(sa.Column('team_id_1', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('team_id_2', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('tournament_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'team', ['team_id_1'], ['id'])
        batch_op.create_foreign_key(None, 'tournament', ['tournament_id'], ['id'])
        batch_op.create_foreign_key(None, 'team', ['team_id_2'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('tournament_id')
        batch_op.drop_column('team_id_2')
        batch_op.drop_column('team_id_1')

    # ### end Alembic commands ###
