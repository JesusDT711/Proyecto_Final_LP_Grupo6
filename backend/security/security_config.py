"""
Configuración de seguridad y reglas de autorización basadas en roles.
Equivalente a SecurityConfig.java del proyecto modelo de referencia.
"""

from functools import wraps
from typing import Callable, Optional
try:
    from exception.api_exception import ApiException
except ImportError:
    from backend.exception.api_exception import ApiException

from .user_details import UserDetails


class SecurityConfig:
    """
    Reglas centralizadas de autorización y control de acceso por ruta y método HTTP.
    
    Reglas de negocio (idénticas a SecurityConfig.java):
    - /api/auth/** : Acceso público sin autenticación (permitAll).
    - /api/admin/** : Exclusivo para administradores (ROLE_ADMIN).
    - GET /api/servicios/** : Permitido para CLIENTE y ADMIN.
    - POST, PUT, DELETE /api/servicios/** : Exclusivo para ADMIN.
    - /api/reservas/** : Exclusivo para clientes (ROLE_CLIENTE).
    - /api/mascotas/** : CLIENTE (propias) y ADMIN.
    - /api/atenciones/** : Personal médico (ROLE_ADMIN).
    """

    MENSAJE_401 = "Debes iniciar sesión para acceder a este recurso"
    MENSAJE_403 = "No tienes permisos para realizar esta acción"

    @classmethod
    def validar_acceso(
        cls,
        ruta: str,
        metodo: str = "GET",
        usuario: Optional[UserDetails] = None,
    ) -> None:
        """
        Evalúa si la petición a 'ruta' con 'metodo' está autorizada para 'usuario'.
        Lanza ApiException(401) si falta autenticación o ApiException(403) si no tiene el rol.
        """
        ruta_clean = ruta.strip().lower()
        metodo_upper = metodo.strip().upper()

        # 1. Endpoints públicos (/api/auth/**, documentación)
        if ruta_clean.startswith("/api/auth"):
            return

        # 2. Toda otra ruta requiere usuario autenticado
        if usuario is None:
            raise ApiException(401, cls.MENSAJE_401)

        # 3. Rutas administrativas (/api/admin/**)
        if ruta_clean.startswith("/api/admin"):
            if not usuario.es_admin():
                raise ApiException(403, cls.MENSAJE_403)
            return

        # 4. Servicios (/api/servicios/**)
        if ruta_clean.startswith("/api/servicios"):
            if metodo_upper == "GET":
                # Consultar catálogo lo pueden hacer ADMIN y CLIENTE
                return
            else:
                # Crear, editar o eliminar servicios requiere ADMIN
                if not usuario.es_admin():
                    raise ApiException(403, cls.MENSAJE_403)
                return

        # 5. Reservas (/api/reservas/**)
        if ruta_clean.startswith("/api/reservas"):
            # En la clínica, agendar y cancelar citas es potestad del CLIENTE
            if not usuario.es_cliente():
                raise ApiException(403, cls.MENSAJE_403)
            return

        # 6. Atenciones / Expedientes clínicos (/api/atenciones/**)
        if ruta_clean.startswith("/api/atenciones"):
            if not usuario.es_admin():
                raise ApiException(403, cls.MENSAJE_403)
            return

        # 7. Mascotas (/api/mascotas/**)
        if ruta_clean.startswith("/api/mascotas"):
            # Clientes gestionan sus mascotas; admin puede supervisar
            if not (usuario.es_cliente() or usuario.es_admin()):
                raise ApiException(403, cls.MENSAJE_403)
            return


# -------------------------------------------------------------
# Decoradores para protección de métodos en servicios o controladores
# -------------------------------------------------------------

def requerir_autenticacion(func: Callable):
    """Decorador que exige que el primer argumento de usuario sea un UserDetails válido."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Buscar usuario en kwargs o args
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
    """Decorador que exige rol ADMIN."""
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
    """Decorador que exige rol CLIENTE."""
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
