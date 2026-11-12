
from typing import Any, Dict, Optional
try:
    from config.settings import settings
    from util.seguridad_util import SeguridadUtil
except ImportError:
    from backend.config.settings import settings
    from backend.util.seguridad_util import SeguridadUtil


class JwtService:
    def __init__(
        self,
        secret_key: Optional[str] = None,
        expiracion_horas: Optional[int] = None,
    ):
        self.secret_key = secret_key or settings.JWT_SECRET_KEY
        self.expiracion_segundos = (expiracion_horas or settings.JWT_EXPIRATION_HOURS) * 3600

    def generar_token(self, email: str, rol: str, nombre_completo: str) -> str:
        return SeguridadUtil.generar_token(
            email=email,
            rol=rol,
            nombre_completo=nombre_completo,
            secret=self.secret_key,
            expiracion_segundos=self.expiracion_segundos,
        )

    def validar_token(self, token: str) -> Optional[Dict[str, Any]]:
        return SeguridadUtil.validar_token(token, secret=self.secret_key)

    def obtener_email_de_token(self, token: str) -> Optional[str]:
        payload = self.validar_token(token)
        if payload:
            return payload.get("email") or payload.get("sub")
        return None

    def obtener_rol_de_token(self, token: str) -> Optional[str]:
        payload = self.validar_token(token)
        if payload:
            return payload.get("rol")
        return None

