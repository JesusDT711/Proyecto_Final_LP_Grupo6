"""
Servicio para cargar detalles de usuario desde la base de datos o repositorio.
Equivalente a UsuarioDetailsServiceImpl.java del proyecto modelo de referencia.
"""

from typing import Optional
try:
    from exception.api_exception import ApiException
    from repository.usuario_repository import UsuarioRepository
    from util.email_util import EmailUtil
except ImportError:
    from backend.exception.api_exception import ApiException
    from backend.repository.usuario_repository import UsuarioRepository
    from backend.util.email_util import EmailUtil

from .user_details import UserDetails


class UserDetailsService:
    """
    Carga la información de seguridad de un usuario a partir de su correo electrónico.
    """

    def __init__(self, usuario_repository: UsuarioRepository):
        self.usuario_repository = usuario_repository

    def load_user_by_email(self, email: str) -> UserDetails:
        """
        Busca un usuario por su email y retorna su objeto UserDetails.
        Lanza ApiException(404) si el usuario no existe.
        """
        email_clean = EmailUtil.normalizar(email)
        usuario = self.usuario_repository.buscar_por_email(email_clean)
        if usuario is None:
            raise ApiException(404, f"Usuario no encontrado con correo: {email}")

        rol_nombre = usuario.rol.nombre if usuario.rol else "CLIENTE"
        return UserDetails(
            id=usuario.id,
            email=usuario.email,
            nombre_completo=usuario.nombre_completo,
            rol=rol_nombre,
        )
