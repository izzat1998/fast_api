"""add content columnm to posts table

Revision ID: 8ac7b0db26fa
Revises: c59c20b06bcd
Create Date: 2022-08-11 16:07:41.896086

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8ac7b0db26fa'
down_revision = 'c59c20b06bcd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
