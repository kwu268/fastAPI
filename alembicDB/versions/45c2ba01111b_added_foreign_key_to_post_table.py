"""added foreign key to post table

Revision ID: 45c2ba01111b
Revises: 4870c317864e
Create Date: 2022-07-08 11:23:18.309521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45c2ba01111b'
down_revision = '4870c317864e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer, nullable = False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'user_id')
    pass
