"""crreated post table

Revision ID: 483f90772ef2
Revises: 
Create Date: 2022-07-08 10:51:15.185072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '483f90772ef2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False))

    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
