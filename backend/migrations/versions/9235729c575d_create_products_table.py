"""create products table

Revision ID: 9235729c575d
Revises: 8deb73f41c7c
Create Date: 2025-01-27 16:43:18.480247

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9235729c575d'
down_revision: Union[str, None] = '8deb73f41c7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('sku', sa.String(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('sub_category', sa.String(), nullable=False),
    sa.Column('brand', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    # ### end Alembic commands ###
