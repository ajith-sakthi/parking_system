"""remove column in the District table

Revision ID: 5aaae1ee0147
Revises: d7b1db892e84
Create Date: 2024-07-06 18:16:50.701449

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '5aaae1ee0147'
down_revision: Union[str, None] = 'd7b1db892e84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('districts', 'pending_status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('districts', sa.Column('pending_status', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1.Approved,-1.Pending,'))
    # ### end Alembic commands ###
