"""create a new column in manager table

Revision ID: 9b7b815dcf1d
Revises: 5081f84605e5
Create Date: 2024-07-10 12:54:50.848434

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b7b815dcf1d'
down_revision: Union[str, None] = '5081f84605e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('managers', sa.Column('created_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('managers', 'created_at')
    # ### end Alembic commands ###
