"""many to many

Revision ID: 12bf42f82cdd
Revises: 3d60a43953c8
Create Date: 2022-11-25 11:24:18.266789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12bf42f82cdd'
down_revision = '3d60a43953c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_team', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('user_team_member_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])
        batch_op.drop_column('member_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_team', schema=None) as batch_op:
        batch_op.add_column(sa.Column('member_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('user_team_member_id_fkey', 'user', ['member_id'], ['id'])
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
