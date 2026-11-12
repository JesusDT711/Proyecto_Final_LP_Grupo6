
from typing import Optional
from .base_dto import BaseDto


class LoginRequest(BaseDto):
    email: str
    password: str

    def __init__(self, email: str = "", password: str = "", **kwargs):
        super().__init__(email=email, password=password, **kwargs)
        self.email = email
        self.password = password


class RegistroRequest(BaseDto):
    nombre_completo: str
    email: str
    password: str
    telefono: Optional[str] = None

    def __init__(
        self,
        nombre_completo: str = "",
        email: str = "",
        password: str = "",
        telefono: Optional[str] = None,
        nombreCompleto: Optional[str] = None,
        **kwargs,
    ):
        nombre = nombreCompleto or nombre_completo
        super().__init__(nombre_completo=nombre, email=email, password=password, telefono=telefono, **kwargs)
        self.nombre_completo = nombre
        self.email = email
        self.password = password
        self.telefono = telefono


class AuthResponse(BaseDto):
    token: str
    email: str
    nombre_completo: str
    rol: str

    def __init__(
        self,
        token: str = "",
        email: str = "",
        nombre_completo: str = "",
        rol: str = "",
        nombreCompleto: Optional[str] = None,
        **kwargs,
    ):
        nombre = nombreCompleto or nombre_completo
        super().__init__(token=token, email=email, nombre_completo=nombre, rol=rol, **kwargs)
        self.token = token
        self.email = email
        self.nombre_completo = nombre
        self.nombreCompleto = nombre
        self.rol = rol

    def to_dict(self):
        return {
            "token": self.token,
            "email": self.email,
            "nombreCompleto": self.nombre_completo,
            "rol": self.rol,
        }


class MensajeResponse(BaseDto):
    """
    Mensaje genérico de confirmación de operaciones.
    """
    mensaje: str

    def __init__(self, mensaje: str = "", **kwargs):
        super().__init__(mensaje=mensaje, **kwargs)
        self.mensaje = mensaje

    def to_dict(self):
        return {"mensaje": self.mensaje}

