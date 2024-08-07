"""change the column name in branch table

Revision ID: 679e48917c38
Revises: 336442ff8d3a
Create Date: 2024-07-08 10:39:23.636002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '679e48917c38'
down_revision: Union[str, None] = '336442ff8d3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('branches', 'approved_status',
               existing_type=mysql.TINYINT(),
               comment='0.Rejected, 1.Approved, -1.Pending',
               existing_comment='1.Approved, -1.Pending',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('branches', 'approved_status',
               existing_type=mysql.TINYINT(),
               comment='1.Approved, -1.Pending',
               existing_comment='0.Rejected, 1.Approved, -1.Pending',
               existing_nullable=True)
    # ### end Alembic commands ###
