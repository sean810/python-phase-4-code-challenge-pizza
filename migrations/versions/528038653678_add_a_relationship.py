"""Add a relationship

Revision ID: 528038653678
Revises: b45bb07c404e
Create Date: 2025-01-20 22:48:11.388353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '528038653678'
down_revision = 'b45bb07c404e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurants', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('address',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurants', schema=None) as batch_op:
        batch_op.alter_column('address',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###
