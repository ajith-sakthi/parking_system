"""add a new column current_parking_space and change a column name as total_parking_space

Revision ID: 3880da6fa21f
Revises: 37b4b72999c6
Create Date: 2024-07-04 15:55:40.798094

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3880da6fa21f'
down_revision: Union[str, None] = '37b4b72999c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
