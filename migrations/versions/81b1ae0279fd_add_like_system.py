"""Add like system

Revision ID: 81b1ae0279fd
Revises: a5c9e04550ba
Create Date: 2024-09-12 07:56:31.207640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81b1ae0279fd'
down_revision = 'a5c9e04550ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('likes',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('artwork_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artwork_id'], ['artwork.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likes')
    # ### end Alembic commands ###
