"""add foreign-key to posts table

Revision ID: aefdf5a60799
Revises: 98506cd58e5e
Create Date: 2022-08-11 16:22:09.863165

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'aefdf5a60799'
down_revision = '98506cd58e5e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table="users", local_cols=['owner_id'],
                          remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', 'posts')
    op.drop_column('posts', 'owner_id')
    pass
