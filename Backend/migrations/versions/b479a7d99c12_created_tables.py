"""Created tables

Revision ID: b479a7d99c12
Revises: 
Create Date: 2023-11-18 15:38:02.266741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b479a7d99c12'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('video_url', sa.String(), nullable=True),
    sa.Column('title', sa.Integer(), nullable=True),
    sa.Column('description', sa.Integer(), nullable=True),
    sa.Column('content', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('farmer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('profile_img', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('profile_img', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('farmer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['farmer_id'], ['farmer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product')
    op.drop_table('user')
    op.drop_table('farmer')
    op.drop_table('course')
    # ### end Alembic commands ###
