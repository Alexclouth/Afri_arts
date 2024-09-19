"""Initial migration

Revision ID: 97da0ae10778
Revises: 94ee79ff4f63
Create Date: 2024-09-06 15:38:09.126040

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '97da0ae10778'
down_revision = '94ee79ff4f63'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artwork',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.Column('image', sa.String(length=256), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('art_type', sa.String(length=128), nullable=False),
    sa.Column('style', sa.String(length=128), nullable=False),
    sa.Column('available', sa.Boolean(), nullable=True),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('post')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('date_posted', mysql.DATETIME(), nullable=False),
    sa.Column('content', mysql.TEXT(), nullable=False),
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='post_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('artwork')
    # ### end Alembic commands ###
