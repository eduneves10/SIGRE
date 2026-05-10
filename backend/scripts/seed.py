"""
Utilitário CLI para criação manual do administrador padrão.

O seed é executado automaticamente no startup da aplicação via lifespan (main.py).
Use este script apenas quando precisar recriar o admin fora do contexto do servidor
(ex.: ambiente de CI, restore de banco, etc.).

Uso:
    ADMIN_SEED_PASSWORD='SuaSenha' python scripts/seed.py
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session
from app.try_database import SessionLocal
from app.models.user import Usuario
from app.services.auth.security import hash_password

_ADMIN_EMAIL = "campusananindeua@uepa.br"
_ADMIN_USERNAME = "admin"
_ADMIN_NAME = "Campus Ananindeua"


def seed_initial_data():
    password = os.environ.get("ADMIN_SEED_PASSWORD", "").strip()
    if not password:
        print(
            "Erro: variável de ambiente ADMIN_SEED_PASSWORD não definida. "
            "Defina-a antes de executar o seed."
        )
        sys.exit(1)

    db: Session = SessionLocal()
    try:
        if db.query(Usuario).filter(Usuario.email == _ADMIN_EMAIL).first():
            print(f"Admin {_ADMIN_EMAIL} já existe — seed ignorado.")
            return

        db.add(Usuario(
            nome=_ADMIN_NAME,
            email=_ADMIN_EMAIL,
            username=_ADMIN_USERNAME,
            senha=hash_password(password),
            tipo_usuario=3,
            status="aprovado",
        ))
        db.commit()
        print(f"Admin criado: {_ADMIN_EMAIL}")
    except Exception as e:
        print(f"Erro ao executar seed: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_initial_data()
