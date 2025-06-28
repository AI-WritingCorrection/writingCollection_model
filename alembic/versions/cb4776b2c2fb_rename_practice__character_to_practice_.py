"""rename practice__character to practice_character

Revision ID: cb4776b2c2fb
Revises: 79bc41e652c3
Create Date: 2025-06-27 20:57:34.350202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb4776b2c2fb'
down_revision: Union[str, None] = '79bc41e652c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # practice__character → practice_character로 이름 변경
    op.alter_column(
        'practices',                      # 테이블명
        'practice__character',            # 기존 컬럼명
        new_column_name='practice_character',
        existing_type=sa.String(length=100),
        nullable=False
    )

def downgrade():
    # 롤백 시 다시 원래 이름으로
    op.alter_column(
        'practices',
        'practice_character',
        new_column_name='practice__character',
        existing_type=sa.String(length=100),
        nullable=False
    )
