"""empty message

Revision ID: 4dd4105bbef9
Revises: 4d9f0fb7fa3c
Create Date: 2020-05-16 17:48:05.341301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4dd4105bbef9'
down_revision = '4d9f0fb7fa3c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('website', sa.String(length=500), nullable=True))
    op.drop_column('Artist', 'webpage_link')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('webpage_link', sa.VARCHAR(length=500), autoincrement=False, nullable=False))
    op.drop_column('Artist', 'website')
    # ### end Alembic commands ###
