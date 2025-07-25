"""Add fields to Resume model

Revision ID: b9a021d683fa
Revises: df2a3611ea6c
Create Date: 2025-07-22 22:47:05.517058

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9a021d683fa'
down_revision: Union[str, Sequence[str], None] = 'df2a3611ea6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resumes', sa.Column('file_url', sa.String(), nullable=False))
    op.add_column('resumes', sa.Column('file_type', sa.String(), nullable=False))
    op.add_column('resumes', sa.Column('parsed_data', sa.JSON(), nullable=True))
    op.alter_column('resumes', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('resumes', 'content')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resumes', sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.alter_column('resumes', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('resumes', 'parsed_data')
    op.drop_column('resumes', 'file_type')
    op.drop_column('resumes', 'file_url')
    # ### end Alembic commands ###
