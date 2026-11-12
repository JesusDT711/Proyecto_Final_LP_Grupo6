"""
Utilidades de seguridad y autenticación (hash de contraseñas y tokens JWT).
Equivalente a PasswordEncoder y JwtUtils del proyecto Spring Boot de referencia.
"""

import base64
import hashlib
import hmac
import json
import time
from typing import Any, Dict, Optional

try:
    import bcrypt
    HAS_BCRYPT = True
except ImportError:
    HAS_BCRYPT = False

try:
    import jwt
    HAS_PYJWT = True
except ImportError:
    HAS_PYJWT = False

# Clave secreta por defecto para tokens de desarrollo
JWT_SECRET_KEY = "clave_super_secreta_veterinaria_huellitas_lp_2026"
JWT_EXPIRATION_SECONDS = 86400  # 24 horas


class SeguridadUtil:
    """
    Herramientas de encriptación de contraseñas y generación/validación de tokens JWT.
    """

    @staticmethod
    def encriptar_password(password: str) -> str:
        """
        Genera un hash seguro para la contraseña del usuario.
        Utiliza bcrypt si está disponible, o PBKDF2-HMAC-SHA256 como fallback universal.
        """
        if not password:
            return ""

        if HAS_BCRYPT:
            salt = bcrypt.gensalt()
            return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
        else:
            salt = b"huellitas_salt_2026"
            derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
            return "pbkdf2_sha256$" + derived.hex()

    @staticmethod
    def verificar_password(password: str, hashed: str) -> bool:
        """
        Verifica si la contraseña en texto plano coincide con el hash almacenado.
        """
        if not password or not hashed:
            return False

        if HAS_BCRYPT and (hashed.startswith("$2a$") or hashed.startswith("$2b$")):
            try:
                return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
            except Exception:
                return False
        elif hashed.startswith("pbkdf2_sha256$"):
            salt = b"huellitas_salt_2026"
            derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
            expected = "pbkdf2_sha256$" + derived.hex()
            return hmac.compare_digest(hashed, expected)
        else:
            # Fallback para pruebas si se almacena texto o hash simple
            return password == hashed

    @staticmethod
    def generar_token(
        email: str,
        rol: str,
        nombre_completo: str,
        secret: str = JWT_SECRET_KEY,
        expiracion_segundos: int = JWT_EXPIRATION_SECONDS,
    ) -> str:
        """
        Genera un token JWT estándar para la sesión autenticada.
        """
        payload = {
            "sub": email,
            "email": email,
            "rol": rol,
            "nombreCompleto": nombre_completo,
            "iat": int(time.time()),
            "exp": int(time.time()) + expiracion_segundos,
        }

        if HAS_PYJWT:
            return jwt.encode(payload, secret, algorithm="HS256")
        else:
            # Implementación nativa de JWT HS256 sin librerías externas
            header = {"alg": "HS256", "typ": "JWT"}
            h_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
            p_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
            signing_input = f"{h_b64}.{p_b64}".encode()
            sig = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
            sig_b64 = base64.urlsafe_b64encode(sig).decode().rstrip("=")
            return f"{h_b64}.{p_b64}.{sig_b64}"

    @staticmethod
    def validar_token(token: str, secret: str = JWT_SECRET_KEY) -> Optional[Dict[str, Any]]:
        """
        Decodifica y valida la firma y expiración de un token JWT.
        """
        if not token:
            return None

        if HAS_PYJWT:
            try:
                return jwt.decode(token, secret, algorithms=["HS256"])
            except Exception:
                return None
        else:
            try:
                parts = token.split(".")
                if len(parts) != 3:
                    return None
                h_b64, p_b64, sig_b64 = parts
                signing_input = f"{h_b64}.{p_b64}".encode()
                sig = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
                sig_calc = base64.urlsafe_b64encode(sig).decode().rstrip("=")
                if not hmac.compare_digest(sig_b64, sig_calc):
                    return None
                
                # Decodificar payload
                rem = len(p_b64) % 4
                if rem > 0:
                    p_b64 += "=" * (4 - rem)
                payload_str = base64.urlsafe_b64decode(p_b64).decode()
                payload = json.loads(payload_str)
                if payload.get("exp", 0) < time.time():
                    return None
                return payload
            except Exception:
                return None

