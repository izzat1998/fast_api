"""create posts table

Revision ID: c59c20b06bcd
Revises: 
Create Date: 2022-08-11 15:47:44.450479

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c59c20b06bcd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')
