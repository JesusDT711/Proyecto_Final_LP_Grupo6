"""
Filtro de autenticación JWT.
Equivalente a JwtAuthFilter.java del proyecto modelo de referencia.
"""

from typing import Optional
from .jwt_service import JwtService
from .user_details import UserDetails
from .user_details_service import UserDetailsService


class SecurityFilter:
    """
    Filtro de seguridad que procesa la cabecera 'Authorization: Bearer <token>',
    valida la firma del JWT y autentica al usuario.
    """

    def __init__(
        self,
        jwt_service: Optional[JwtService] = None,
        user_details_service: Optional[UserDetailsService] = None,
    ):
        self.jwt_service = jwt_service or JwtService()
        self.user_details_service = user_details_service

    def extraer_token_de_header(self, auth_header: Optional[str]) -> Optional[str]:
        """
        Extrae el token Bearer de la cabecera Authorization.
        """
        if not auth_header:
            return None

        partes = auth_header.strip().split()
        if len(partes) == 2 and partes[0].lower() == "bearer":
            return partes[1]
        return None

    def autenticar(self, auth_header: Optional[str]) -> Optional[UserDetails]:
        """
        Valida la cabecera Authorization y retorna el usuario autenticado (UserDetails)
        o None si el token no existe, está expirado o fue alterado.
        """
        token = self.extraer_token_de_header(auth_header)
        if not token:
            return None

        payload = self.jwt_service.validar_token(token)
        if not payload:
            return None

        email = payload.get("email") or payload.get("sub")
        if not email:
            return None

        # Si tenemos UserDetailsService conectado, cargamos de la BD
        if self.user_details_service is not None:
            try:
                return self.user_details_service.load_user_by_email(email)
            except Exception:
                return None

        # Si no se proveyó repositorio, reconstruimos UserDetails a partir del payload del JWT
        return UserDetails(
            id=payload.get("id"),
            email=email,
            nombre_completo=payload.get("nombreCompleto") or payload.get("nombre_completo", ""),
            rol=payload.get("rol", "CLIENTE"),
        )
