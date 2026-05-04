"""empty message

Revision ID: 7387b3b65b31
Revises: a4158691be0f, df1f16ab9359
Create Date: 2026-05-04 02:03:40.899872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7387b3b65b31'
down_revision: Union[str, Sequence[str], None] = ('a4158691be0f', 'df1f16ab9359')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
