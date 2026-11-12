
from typing import Optional
from .base_dto import BaseDto


class MascotaRequest(BaseDto):
    nombre: str
    especie: str
    raza: Optional[str] = None
    sexo: Optional[str] = None
    fecha_nacimiento: Optional[str] = None

    def __init__(
        self,
        nombre: str = "",
        especie: str = "",
        raza: Optional[str] = None,
        sexo: Optional[str] = None,
        fecha_nacimiento: Optional[str] = None,
        fechaNacimiento: Optional[str] = None,
        **kwargs,
    ):
        fecha = fechaNacimiento or fecha_nacimiento
        super().__init__(
            nombre=nombre,
            especie=especie,
            raza=raza,
            sexo=sexo,
            fecha_nacimiento=fecha,
            **kwargs,
        )
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.sexo = sexo
        self.fecha_nacimiento = fecha
        self.fechaNacimiento = fecha


class MascotaResponse(BaseDto):
    id: int
    nombre: str
    especie: str
    raza: Optional[str] = None
    sexo: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    usuario_id: int
    propietario_nombre: Optional[str] = None
    created_at: Optional[str] = None

    def __init__(
        self,
        id: int = 0,
        nombre: str = "",
        especie: str = "",
        usuario_id: int = 0,
        raza: Optional[str] = None,
        sexo: Optional[str] = None,
        fecha_nacimiento: Optional[str] = None,
        propietario_nombre: Optional[str] = None,
        created_at: Optional[str] = None,
        fechaNacimiento: Optional[str] = None,
        usuarioId: Optional[int] = None,
        propietarioNombre: Optional[str] = None,
        createdAt: Optional[str] = None,
        **kwargs,
    ):
        fecha = fechaNacimiento or fecha_nacimiento
        u_id = usuarioId if usuarioId is not None else usuario_id
        prop = propietarioNombre or propietario_nombre
        creado = createdAt or created_at
        super().__init__(
            id=id,
            nombre=nombre,
            especie=especie,
            raza=raza,
            sexo=sexo,
            fecha_nacimiento=fecha,
            usuario_id=u_id,
            propietario_nombre=prop,
            created_at=creado,
            **kwargs,
        )
        self.id = id
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.sexo = sexo
        self.fecha_nacimiento = fecha
        self.fechaNacimiento = fecha
        self.usuario_id = u_id
        self.usuarioId = u_id
        self.propietario_nombre = prop
        self.propietarioNombre = prop
        self.created_at = creado
        self.createdAt = creado

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "especie": self.especie,
            "raza": self.raza,
            "sexo": self.sexo,
            "fechaNacimiento": self.fecha_nacimiento,
            "usuarioId": self.usuario_id,
            "propietarioNombre": self.propietario_nombre,
            "createdAt": self.created_at,
        }

