
from typing import Any, Dict, Optional

class UserDetails:

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
        return self.email

    def es_admin(self) -> bool:
        return self.rol == "ADMIN"

    def es_cliente(self) -> bool:
        return self.rol == "CLIENTE"

    def tiene_rol(self, nombre_rol: str) -> bool:
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

