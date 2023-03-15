"""empty message

Revision ID: 5564efde34c5
Revises: 032f65b1ca2e
Create Date: 2023-02-10 12:48:46.273628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5564efde34c5'
down_revision = '032f65b1ca2e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.alter_column('list_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.alter_column('list_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
