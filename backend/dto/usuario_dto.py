
from typing import Optional
from .base_dto import BaseDto


class UsuarioUpdateRequest(BaseDto):
    nombre_completo: str
    email: str
    password: Optional[str] = None
    rol: Optional[str] = None
    telefono: Optional[str] = None

    def __init__(
        self,
        nombre_completo: str = "",
        email: str = "",
        password: Optional[str] = None,
        rol: Optional[str] = None,
        telefono: Optional[str] = None,
        nombreCompleto: Optional[str] = None,
        **kwargs,
    ):
        nombre = nombreCompleto or nombre_completo
        super().__init__(
            nombre_completo=nombre,
            email=email,
            password=password,
            rol=rol,
            telefono=telefono,
            **kwargs,
        )
        self.nombre_completo = nombre
        self.email = email
        self.password = password
        self.rol = rol
        self.telefono = telefono


class UsuarioResponse(BaseDto):
    id: int
    email: str
    nombre_completo: str
    rol: str
    telefono: Optional[str] = None
    created_at: Optional[str] = None

    def __init__(
        self,
        id: int = 0,
        email: str = "",
        nombre_completo: str = "",
        rol: str = "",
        telefono: Optional[str] = None,
        created_at: Optional[str] = None,
        nombreCompleto: Optional[str] = None,
        createdAt: Optional[str] = None,
        **kwargs,
    ):
        nombre = nombreCompleto or nombre_completo
        creado = createdAt or created_at
        super().__init__(
            id=id,
            email=email,
            nombre_completo=nombre,
            rol=rol,
            telefono=telefono,
            created_at=creado,
            **kwargs,
        )
        self.id = id
        self.email = email
        self.nombre_completo = nombre
        self.nombreCompleto = nombre
        self.rol = rol
        self.telefono = telefono
        self.created_at = creado
        self.createdAt = creado

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombreCompleto": self.nombre_completo,
            "rol": self.rol,
            "telefono": self.telefono,
            "createdAt": self.created_at,
        }

