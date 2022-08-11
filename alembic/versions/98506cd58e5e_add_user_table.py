"""add user table

Revision ID: 98506cd58e5e
Revises: 8ac7b0db26fa
Create Date: 2022-08-11 16:14:13.166680

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '98506cd58e5e'
down_revision = '8ac7b0db26fa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                              nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade():
    op.drop_table('users')
    pass
