import os
import logging
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.config import get_settings
from app.try_database import Base, engine
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    auth, users, rooms, reservations, calendar, google,
    room_types, dashboard, professors, disciplines,
    courses, reports, periods, solicitations
)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

logger = logging.getLogger(__name__)

_ADMIN_EMAIL = "campusananindeua@uepa.br"
_ADMIN_USERNAME = "admin"
_ADMIN_NAME = "Campus Ananindeua"


def _seed_admin() -> None:
    """Garante que o administrador padrão exista ao iniciar a aplicação."""
    from app.try_database import SessionLocal
    from app.models.user import Usuario
    from app.services.auth.security import hash_password

    settings = get_settings()
    password = settings.ADMIN_SEED_PASSWORD.strip()
    if not password:
        logger.warning(
            "ADMIN_SEED_PASSWORD não definida — administrador padrão não foi criado."
        )
        return

    db = SessionLocal()
    try:
        if db.query(Usuario).filter(Usuario.email == _ADMIN_EMAIL).first():
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
        logger.info("Administrador padrão criado: %s", _ADMIN_EMAIL)
    except Exception:
        db.rollback()
        logger.exception("Erro ao criar administrador padrão.")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine, checkfirst=True)
    _seed_admin()
    yield

settings = get_settings()
app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https?://.*",  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    SessionMiddleware, 
    secret_key=settings.JWT_SECRET,
    session_cookie="sigre_session",
    same_site="lax",
    https_only=False,
    max_age=3600
)

app.include_router(solicitations.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(rooms.router)
app.include_router(room_types.router)
app.include_router(reservations.router)
app.include_router(calendar.router)
app.include_router(google.router)
app.include_router(dashboard.router)
app.include_router(professors.router)
app.include_router(disciplines.router)
app.include_router(courses.router)
app.include_router(reports.router)
app.include_router(periods.router)

@app.get("/health")
def health():
	return {"status": "ok"}
