"""add a new column current_parking_space and change a column name as total_parking_space

Revision ID: 326b83ed97ec
Revises: d4f135ee9d1d
Create Date: 2024-07-04 15:56:58.959272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '326b83ed97ec'
down_revision: Union[str, None] = 'd4f135ee9d1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('parking_stations', sa.Column('total_parking_space', sa.Integer(), nullable=True))
    op.add_column('parking_stations', sa.Column('current_parking_space', sa.Integer(), nullable=True))
    op.drop_column('parking_stations', 'parking_capacity')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('parking_stations', sa.Column('parking_capacity', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('parking_stations', 'current_parking_space')
    op.drop_column('parking_stations', 'total_parking_space')
    # ### end Alembic commands ###
