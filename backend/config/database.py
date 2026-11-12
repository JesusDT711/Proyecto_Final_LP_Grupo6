"""
Configuración de la conexión a Base de Datos relacional MySQL con SQLAlchemy.
Provee engine, sessionmaker y generador de sesiones get_db().
"""

from typing import Any, Generator, Optional
from .settings import settings

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, Session
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    create_engine = None
    sessionmaker = None
    Session = Any


# Variable para almacenar el engine activo
_engine = None
_SessionLocal = None


def get_engine(use_sqlite_fallback: bool = False):
    """
    Crea o recupera el engine de SQLAlchemy.
    Permite alternar entre MySQL (por defecto) o SQLite para testing local.
    """
    global _engine, _SessionLocal
    if not SQLALCHEMY_AVAILABLE:
        return None

    if _engine is None:
        db_url = settings.SQLITE_URL if use_sqlite_fallback else settings.DATABASE_URL
        connect_args = {"check_same_thread": False} if "sqlite" in db_url else {}

        try:
            _engine = create_engine(
                db_url,
                echo=settings.DEBUG,
                pool_pre_ping=True,
                connect_args=connect_args,
            )
            _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
        except Exception as e:
            # Si falla la conexión a MySQL en desarrollo, fallback seguro a SQLite
            if not use_sqlite_fallback:
                return get_engine(use_sqlite_fallback=True)
            raise e

    return _engine


def get_session_factory():
    """Retorna la fábrica de sesiones SessionLocal."""
    global _SessionLocal
    if _SessionLocal is None:
        get_engine()
    return _SessionLocal


def get_db() -> Generator[Any, None, None]:
    """
    Generador de sesión de base de datos para inyección de dependencias
    (compatible con FastAPI Depends(get_db) o bloques with).
    """
    factory = get_session_factory()
    if factory is None:
        yield None
        return

    session = factory()
    try:
        yield session
    finally:
        session.close()


def init_db(engine=None):
    """
    Inicializa las tablas de la base de datos a partir de los modelos declarativos de SQLAlchemy.
    """
    if not SQLALCHEMY_AVAILABLE:
        return False

    eng = engine or get_engine()
    if eng is None:
        return False

    try:
        from model.base import Base
    except ImportError:
        from backend.model.base import Base

    if hasattr(Base, "metadata") and Base.metadata is not None:
        Base.metadata.create_all(bind=eng)
        return True
    return False
