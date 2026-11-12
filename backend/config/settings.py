"""
Configuraciones globales del sistema Veterinaria Huellitas.
Lee variables de entorno o archivo .env con valores por defecto de desarrollo.
"""

import os
from pathlib import Path
from typing import List


class Settings:
    """
    Configuración centralizada de la aplicación.
    Equivalente a application.properties y AppConfig.java en Spring Boot.
    """

    # Entorno
    APP_NAME: str = "Veterinaria Huellitas Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

    # Zona horaria (equivalente al Bean Clock con ZoneId America/Lima en AppConfig.java)
    TIMEZONE: str = os.getenv("TIMEZONE", "America/Lima")

    # Horario de atención (huellitas.horario.apertura / cierre)
    HORARIO_APERTURA: str = os.getenv("HORARIO_APERTURA", "09:00")
    HORARIO_CIERRE: str = os.getenv("HORARIO_CIERRE", "21:00")

    # Seguridad y JWT (equivalente a jwt.secret y jwt.expiration)
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "clave_super_secreta_veterinaria_huellitas_lp_2026")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

    # Base de Datos MySQL
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_NAME: str = os.getenv("DB_NAME", "veterinaria_huellitas")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")

    # URL de conexión MySQL (SQLAlchemy)
    @property
    def DATABASE_URL(self) -> str:
        env_url = os.getenv("DATABASE_URL")
        if env_url:
            return env_url
        if self.DB_PASSWORD:
            return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
        return f"mysql+pymysql://{self.DB_USER}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"

    # URL alternativa de SQLite para pruebas rápidas sin MySQL local
    SQLITE_URL: str = "sqlite:///./veterinaria_huellitas_dev.db"

    # CORS para comunicación con el frontend (Angular en localhost:4200)
    CORS_ORIGINS: List[str] = [
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "http://localhost:3000",
        "http://localhost:8080",
    ]


# Instancia singleton de configuración
settings = Settings()
