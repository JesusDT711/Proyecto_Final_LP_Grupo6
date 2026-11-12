
from functools import wraps
from typing import Callable, Optional
try:
    from exception.api_exception import ApiException
except ImportError:
    from backend.exception.api_exception import ApiException

from .user_details import UserDetails


class SecurityConfig:

    MENSAJE_401 = "Debes iniciar sesión para acceder a este recurso"
    MENSAJE_403 = "No tienes permisos para realizar esta acción"

    @classmethod
    def validar_acceso(
        cls,
        ruta: str,
        metodo: str = "GET",
        usuario: Optional[UserDetails] = None,
    ) -> None:
        ruta_clean = ruta.strip().lower()
        metodo_upper = metodo.strip().upper()

        if ruta_clean.startswith("/api/auth"):
            return

        if usuario is None:
            raise ApiException(401, cls.MENSAJE_401)

        if ruta_clean.startswith("/api/admin"):
            if not usuario.es_admin():
                raise ApiException(403, cls.MENSAJE_403)
            return

        if ruta_clean.startswith("/api/servicios"):
            if metodo_upper == "GET":
                return
            else:
                if not usuario.es_admin():
                    raise ApiException(403, cls.MENSAJE_403)
                return

        if ruta_clean.startswith("/api/reservas"):
            if not usuario.es_cliente():
                raise ApiException(403, cls.MENSAJE_403)
            return

        if ruta_clean.startswith("/api/atenciones"):
            if not usuario.es_admin():
                raise ApiException(403, cls.MENSAJE_403)
            return

        if ruta_clean.startswith("/api/mascotas"):
            if not (usuario.es_cliente() or usuario.es_admin()):
                raise ApiException(403, cls.MENSAJE_403)
            return


def requerir_autenticacion(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        usuario = kwargs.get("usuario") or kwargs.get("user")
        if usuario is None:
            for a in args:
                if isinstance(a, UserDetails):
                    usuario = a
                    break

        if usuario is None:
            raise ApiException(401, SecurityConfig.MENSAJE_401)
        return func(*args, **kwargs)
    return wrapper


def requerir_admin(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        usuario = kwargs.get("usuario") or kwargs.get("user")
        if usuario is None:
            for a in args:
                if isinstance(a, UserDetails):
                    usuario = a
                    break

        if usuario is None:
            raise ApiException(401, SecurityConfig.MENSAJE_401)
        if not usuario.es_admin():
            raise ApiException(403, SecurityConfig.MENSAJE_403)
        return func(*args, **kwargs)
    return wrapper


def requerir_cliente(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        usuario = kwargs.get("usuario") or kwargs.get("user")
        if usuario is None:
            for a in args:
                if isinstance(a, UserDetails):
                    usuario = a
                    break

        if usuario is None:
            raise ApiException(401, SecurityConfig.MENSAJE_401)
        if not usuario.es_cliente():
            raise ApiException(403, SecurityConfig.MENSAJE_403)
        return func(*args, **kwargs)
    return wrapper

