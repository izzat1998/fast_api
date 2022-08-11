"""add last few columns to posts

Revision ID: e1f3adfbe522
Revises: aefdf5a60799
Create Date: 2022-08-11 16:31:00.575795

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e1f3adfbe522'
down_revision = 'aefdf5a60799'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created')
    pass
