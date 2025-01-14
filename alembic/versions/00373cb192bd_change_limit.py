"""change limit

Revision ID: 00373cb192bd
Revises: 043bd5d5b454
Create Date: 2025-01-14 11:11:43.598045

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00373cb192bd'
down_revision: Union[str, None] = '043bd5d5b454'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('books', 'title',
               existing_type=sa.VARCHAR(length=75),
               type_=sa.String(length=100),
               existing_nullable=False)
    op.alter_column('books', 'author',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.String(length=100),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('books', 'author',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=30),
               existing_nullable=False)
    op.alter_column('books', 'title',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=75),
               existing_nullable=False)
    # ### end Alembic commands ###
