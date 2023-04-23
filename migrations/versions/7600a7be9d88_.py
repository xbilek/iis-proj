"""empty message

Revision ID: 7600a7be9d88
Revises: d6a3ecde0162
Create Date: 2022-11-24 22:05:19.382984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7600a7be9d88'
down_revision = 'd6a3ecde0162'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('match', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id1', sa.Integer(), nullable=False))
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('match', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
        batch_op.drop_column('id1')

    # ### end Alembic commands ###
