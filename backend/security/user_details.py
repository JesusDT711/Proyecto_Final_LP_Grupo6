"""
Representación del usuario autenticado en el contexto de seguridad.
Equivalente a UsuarioDetailsImpl.java del proyecto modelo de referencia.
"""

from typing import Any, Dict, Optional


class UserDetails:
    """
    Contenedor de identidad y roles del usuario autenticado en el sistema.
    """

    def __init__(
        self,
        id: Optional[int],
        email: str,
        nombre_completo: str,
        rol: str,
    ):
        self.id = id
        self.email = email
        self.nombre_completo = nombre_completo
        self.rol = rol.upper() if rol else "CLIENTE"

    @property
    def username(self) -> str:
        """En este sistema, el correo es el identificador (username) principal."""
        return self.email

    def es_admin(self) -> bool:
        """Indica si el usuario cuenta con privilegios de ADMINISTRADOR."""
        return self.rol == "ADMIN"

    def es_cliente(self) -> bool:
        """Indica si el usuario tiene el rol de CLIENTE."""
        return self.rol == "CLIENTE"

    def tiene_rol(self, nombre_rol: str) -> bool:
        """Verifica si el usuario posee un rol específico."""
        return self.rol == nombre_rol.strip().upper()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email,
            "nombreCompleto": self.nombre_completo,
            "rol": self.rol,
        }

    def __repr__(self) -> str:
        return f"<UserDetails(email='{self.email}', rol='{self.rol}')>"
