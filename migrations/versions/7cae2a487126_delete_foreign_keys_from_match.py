"""delete foreign keys from match

Revision ID: 7cae2a487126
Revises: 97df144eaa3b
Create Date: 2022-11-27 13:19:14.579488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cae2a487126'
down_revision = '97df144eaa3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('match', schema=None) as batch_op:
        batch_op.drop_constraint('match_tournament_name_fkey', type_='foreignkey')
        batch_op.drop_constraint('match_team2_name_fkey', type_='foreignkey')
        batch_op.drop_constraint('match_team1_name_fkey', type_='foreignkey')
        batch_op.drop_column('tournament_name')
        batch_op.drop_column('team1_name')
        batch_op.drop_column('team2_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('match', schema=None) as batch_op:
        batch_op.add_column(sa.Column('team2_name', sa.VARCHAR(length=150), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('team1_name', sa.VARCHAR(length=150), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('tournament_name', sa.VARCHAR(length=150), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('match_team1_name_fkey', 'team', ['team1_name'], ['name'])
        batch_op.create_foreign_key('match_team2_name_fkey', 'team', ['team2_name'], ['name'])
        batch_op.create_foreign_key('match_tournament_name_fkey', 'team', ['tournament_name'], ['name'])

    # ### end Alembic commands ###