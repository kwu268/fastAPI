"""add content column to post table

Revision ID: b7933ab7b00d
Revises: 483f90772ef2
Create Date: 2022-07-08 11:11:29.576339

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7933ab7b00d'
down_revision = '483f90772ef2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
