"""empty message

Revision ID: 39fe993c1099
Revises: 3ae55efc8911
Create Date: 2020-05-16 16:06:56.397754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39fe993c1099'
down_revision = '3ae55efc8911'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'genres')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
