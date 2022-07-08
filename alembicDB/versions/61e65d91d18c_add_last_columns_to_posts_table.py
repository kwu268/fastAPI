"""add last columns to posts table

Revision ID: 61e65d91d18c
Revises: 45c2ba01111b
Create Date: 2022-07-08 11:26:46.308564

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61e65d91d18c'
down_revision = '45c2ba01111b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),
        op.add_column('posts', sa.Column(
            'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()'))
        ))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
