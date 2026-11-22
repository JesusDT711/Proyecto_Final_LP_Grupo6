from typing import Any, Generator
from .settings import settings

try:
    from sqlalchemy import create_engine
    from sqlalchemy.engine import URL
    from sqlalchemy.orm import sessionmaker

    SQLALCHEMY_AVAILABLE = True

except ImportError:
    SQLALCHEMY_AVAILABLE = False
    create_engine = None
    URL = None
    sessionmaker = None


_engine = None
_SessionLocal = None


def get_engine(use_sqlite_fallback: bool = False):
    global _engine, _SessionLocal

    if not SQLALCHEMY_AVAILABLE:
        raise RuntimeError("SQLAlchemy no está instalado.")

    if _engine is None:

        if use_sqlite_fallback:
            db_url = settings.SQLITE_URL
            connect_args = {"check_same_thread": False}

        else:
            db_url = URL.create(
                drivername="mysql+pymysql",
                username=settings.DB_USER,
                password=settings.DB_PASSWORD,
                host=settings.DB_HOST,
                port=int(settings.DB_PORT),
                database=settings.DB_NAME,
                query={"charset": "utf8mb4"},
            )

            connect_args = {
                "ssl": {"ssl": {}}
            }

        _engine = create_engine(
            db_url,
            echo=settings.DEBUG,
            pool_pre_ping=True,
            connect_args=connect_args,
        )

        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=_engine,
        )

    return _engine


def get_session_factory():
    global _SessionLocal

    if _SessionLocal is None:
        get_engine()

    return _SessionLocal


def get_db() -> Generator[Any, None, None]:
    factory = get_session_factory()

    if factory is None:
        raise RuntimeError(
            "No se pudo crear la sesión de base de datos."
        )

    session = factory()

    try:
        yield session
    finally:
        session.close()


def init_db(engine=None):
    if not SQLALCHEMY_AVAILABLE:
        raise RuntimeError("SQLAlchemy no está instalado.")

    eng = engine or get_engine()

    from model.base import Base

    if not Base.metadata.tables:
        raise RuntimeError(
            "No se encontraron modelos registrados."
        )

    Base.metadata.create_all(bind=eng)

    return True