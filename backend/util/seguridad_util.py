"""
Utilidades de seguridad y autenticación:
hash de contraseñas y generación/validación de tokens JWT.
"""

import bcrypt
from jose import jwt, JWTError

from typing import Any, Dict, Optional
import time


class SeguridadUtil:

    @staticmethod
    def encriptar_password(password: str) -> str:
        """
        Genera un hash seguro de contraseña utilizando bcrypt.
        """

        if not password:
            raise ValueError("La contraseña no puede estar vacía.")

        password_bytes = password.encode("utf-8")

        if len(password_bytes) > 72:
            raise ValueError(
                "La contraseña supera el límite permitido por bcrypt."
            )

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)

        return hashed.decode("utf-8")

    @staticmethod
    def verificar_password(password: str, hashed: str) -> bool:
        """
        Verifica una contraseña frente a su hash bcrypt.
        """

        if not password or not hashed:
            return False

        try:
            return bcrypt.checkpw(
                password.encode("utf-8"),
                hashed.encode("utf-8")
            )
        except (ValueError, TypeError):
            return False

    @staticmethod
    def generar_token(
        email: str,
        rol: str,
        nombre_completo: str,
        secret: str,
        expiracion_segundos: int = 86400,
    ) -> str:
        """
        Genera un token JWT firmado mediante HS256.
        """

        ahora = int(time.time())

        payload = {
            "sub": email,
            "email": email,
            "rol": rol,
            "nombreCompleto": nombre_completo,
            "iat": ahora,
            "exp": ahora + expiracion_segundos,
        }

        return jwt.encode(
            payload,
            secret,
            algorithm="HS256"
        )

    @staticmethod
    def validar_token(
        token: str,
        secret: str
    ) -> Optional[Dict[str, Any]]:
        """
        Valida la firma y expiración de un token JWT.
        """

        if not token:
            return None

        try:
            return jwt.decode(
                token,
                secret,
                algorithms=["HS256"]
            )

        except JWTError:
            return None