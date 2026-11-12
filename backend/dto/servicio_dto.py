
from decimal import Decimal
from typing import Optional, Union
from .base_dto import BaseDto


class ServicioRequest(BaseDto):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    duracion_minutos: int
    activo: Optional[bool] = True

    def __init__(
        self,
        nombre: str = "",
        precio: Union[float, Decimal, str] = 0.0,
        duracion_minutos: int = 30,
        descripcion: Optional[str] = None,
        activo: Optional[bool] = True,
        duracionMinutos: Optional[int] = None,
        **kwargs,
    ):
        duracion = duracionMinutos if duracionMinutos is not None else duracion_minutos
        super().__init__(
            nombre=nombre,
            precio=float(precio),
            duracion_minutos=duracion,
            descripcion=descripcion,
            activo=activo,
            **kwargs,
        )
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = float(precio)
        self.duracion_minutos = duracion
        self.duracionMinutos = duracion
        self.activo = activo


class ServicioResponse(BaseDto):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    duracion_minutos: int
    activo: bool
    created_at: Optional[str] = None

    def __init__(
        self,
        id: int = 0,
        nombre: str = "",
        precio: Union[float, Decimal, str] = 0.0,
        duracion_minutos: int = 30,
        descripcion: Optional[str] = None,
        activo: bool = True,
        created_at: Optional[str] = None,
        duracionMinutos: Optional[int] = None,
        createdAt: Optional[str] = None,
        **kwargs,
    ):
        duracion = duracionMinutos if duracionMinutos is not None else duracion_minutos
        creado = createdAt or created_at
        super().__init__(
            id=id,
            nombre=nombre,
            precio=float(precio),
            duracion_minutos=duracion,
            descripcion=descripcion,
            activo=activo,
            created_at=creado,
            **kwargs,
        )
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = float(precio)
        self.duracion_minutos = duracion
        self.duracionMinutos = duracion
        self.activo = activo
        self.created_at = creado
        self.createdAt = creado

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "duracionMinutos": self.duracion_minutos,
            "activo": self.activo,
            "createdAt": self.created_at,
        }

