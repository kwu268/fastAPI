"""add user table

Revision ID: 4870c317864e
Revises: b7933ab7b00d
Create Date: 2022-07-08 11:14:36.625094

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4870c317864e'
down_revision = 'b7933ab7b00d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
        sa.Column('id', sa.Integer(), nullable = False),
        sa.Column('email', sa.String(), nullable = False),
        sa.Column('password', sa.String(), nullable = False),
        sa.Column('created_at', sa.TIMESTAMP(timezone = True), server_default=sa.text('now()'), nullable = False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
