"""add contact description

Revision ID: a7dda3219fcd
Revises: 738fb6728d81
Create Date: 2022-12-09 12:22:47.164189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7dda3219fcd'
down_revision = '738fb6728d81'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('description', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contacts', 'description')
    # ### end Alembic commands ###
