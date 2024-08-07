"""create table testuser

Revision ID: 9a6c357321a5
Revises: 18fde8a3580e
Create Date: 2024-07-18 09:53:51.885970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a6c357321a5'
down_revision: Union[str, None] = '18fde8a3580e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('testusers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=True),
    sa.Column('last_name', sa.String(length=20), nullable=True),
    sa.Column('user_name', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=30), nullable=True),
    sa.Column('contact_no', sa.String(length=14), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('testusers')
    # ### end Alembic commands ###
