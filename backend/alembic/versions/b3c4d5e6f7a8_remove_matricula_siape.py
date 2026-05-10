"""Remove matricula e siape da tabela usuarios; torna matricula opcional em solicitacoes

Revision ID: b3c4d5e6f7a8
Revises: 7387b3b65b31
Create Date: 2026-05-10 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'b3c4d5e6f7a8'
down_revision: Union[str, None] = '7387b3b65b31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Remove matricula e siape da tabela de usuarios
    op.drop_column('usuarios', 'matricula')
    op.drop_column('usuarios', 'siape')

    # Torna matricula opcional na tabela de solicitacoes
    op.alter_column(
        'solicitacoes', 'matricula',
        existing_type=sa.String(length=50),
        nullable=True,
    )


def downgrade() -> None:
    # Restaura matricula como obrigatoria em solicitacoes
    op.alter_column(
        'solicitacoes', 'matricula',
        existing_type=sa.String(length=50),
        nullable=False,
    )

    # Recria colunas em usuarios
    op.add_column('usuarios', sa.Column('siape',     sa.String(length=50), nullable=True))
    op.add_column('usuarios', sa.Column('matricula', sa.String(length=50), nullable=True))
