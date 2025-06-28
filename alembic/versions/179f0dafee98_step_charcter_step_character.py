"""step_charcter->step_character

Revision ID: 179f0dafee98
Revises: e1d6772c5ed9
Create Date: 2025-06-26 15:28:32.317347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '179f0dafee98'
down_revision: Union[str, None] = 'e1d6772c5ed9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. 새 컬럼을 nullable=True 로 추가
    op.add_column('steps',
        sa.Column('step_character', sa.String(length=100), nullable=True)
    )
    # 2. 기존 컬럼 데이터를 복사
    op.execute("""
        UPDATE steps
        SET step_character = step_charcter
        WHERE step_character IS NULL;
    """)
    # 3. 옛 컬럼 삭제
    op.drop_column('steps', 'step_charcter')
    # 4. 새 컬럼을 NOT NULL 로 변경
    op.alter_column('steps', 'step_character', nullable=False)

def downgrade():
    # 리버스: 옛 컬럼 복원 후 데이터 복사, 새 컬럼 삭제
    op.add_column('steps',
        sa.Column('step_charcter', sa.String(length=100), nullable=True)
    )
    op.execute("""
        UPDATE steps
        SET step_charcter = step_character
        WHERE step_charcter IS NULL;
    """)
    op.drop_column('steps', 'step_character')
    op.alter_column('steps', 'step_charcter', nullable=False)
