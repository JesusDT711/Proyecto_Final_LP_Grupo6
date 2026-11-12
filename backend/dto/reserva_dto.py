
from typing import Optional
from .base_dto import BaseDto


class ReservaRequest(BaseDto):
    servicio_id: int
    fecha_hora: str
    mascota_id: Optional[int] = None
    nombre_mascota: Optional[str] = None
    observaciones: Optional[str] = None

    def __init__(
        self,
        servicio_id: int = 0,
        fecha_hora: str = "",
        mascota_id: Optional[int] = None,
        nombre_mascota: Optional[str] = None,
        observaciones: Optional[str] = None,
        servicioId: Optional[int] = None,
        fechaHora: Optional[str] = None,
        mascotaId: Optional[int] = None,
        nombreMascota: Optional[str] = None,
        **kwargs,
    ):
        s_id = servicioId if servicioId is not None else servicio_id
        f_hora = fechaHora or fecha_hora
        m_id = mascotaId if mascotaId is not None else mascota_id
        n_mascota = nombreMascota or nombre_mascota

        super().__init__(
            servicio_id=s_id,
            fecha_hora=f_hora,
            mascota_id=m_id,
            nombre_mascota=n_mascota,
            observaciones=observaciones,
            **kwargs,
        )
        self.servicio_id = s_id
        self.servicioId = s_id
        self.fecha_hora = f_hora
        self.fechaHora = f_hora
        self.mascota_id = m_id
        self.mascotaId = m_id
        self.nombre_mascota = n_mascota
        self.nombreMascota = n_mascota
        self.observaciones = observaciones


class ReservaResponse(BaseDto):
    id: int
    servicio_id: int
    servicio_nombre: str
    cliente_email: str
    cliente_nombre: str
    mascota_id: Optional[int] = None
    nombre_mascota: Optional[str] = None
    fecha_hora: str
    fecha_hora_fin: str
    estado: str
    observaciones: Optional[str] = None
    creada_en: Optional[str] = None

    def __init__(
        self,
        id: int = 0,
        servicio_id: int = 0,
        servicio_nombre: str = "",
        cliente_email: str = "",
        cliente_nombre: str = "",
        fecha_hora: str = "",
        fecha_hora_fin: str = "",
        estado: str = "CONFIRMADA",
        mascota_id: Optional[int] = None,
        nombre_mascota: Optional[str] = None,
        observaciones: Optional[str] = None,
        creada_en: Optional[str] = None,
        servicioId: Optional[int] = None,
        servicioNombre: Optional[str] = None,
        clienteEmail: Optional[str] = None,
        clienteNombre: Optional[str] = None,
        mascotaId: Optional[int] = None,
        nombreMascota: Optional[str] = None,
        fechaHora: Optional[str] = None,
        fechaHoraFin: Optional[str] = None,
        creadaEn: Optional[str] = None,
        **kwargs,
    ):
        s_id = servicioId if servicioId is not None else servicio_id
        s_nom = servicioNombre or servicio_nombre
        c_mail = clienteEmail or cliente_email
        c_nom = clienteNombre or cliente_nombre
        m_id = mascotaId if mascotaId is not None else mascota_id
        n_masc = nombreMascota or nombre_mascota
        f_ini = fechaHora or fecha_hora
        f_fin = fechaHoraFin or fecha_hora_fin
        creada = creadaEn or creada_en

        super().__init__(
            id=id,
            servicio_id=s_id,
            servicio_nombre=s_nom,
            cliente_email=c_mail,
            cliente_nombre=c_nom,
            mascota_id=m_id,
            nombre_mascota=n_masc,
            fecha_hora=f_ini,
            fecha_hora_fin=f_fin,
            estado=estado,
            observaciones=observaciones,
            creada_en=creada,
            **kwargs,
        )
        self.id = id
        self.servicio_id = s_id
        self.servicioId = s_id
        self.servicio_nombre = s_nom
        self.servicioNombre = s_nom
        self.cliente_email = c_mail
        self.clienteEmail = c_mail
        self.cliente_nombre = c_nom
        self.clienteNombre = c_nom
        self.mascota_id = m_id
        self.mascotaId = m_id
        self.nombre_mascota = n_masc
        self.nombreMascota = n_masc
        self.fecha_hora = f_ini
        self.fechaHora = f_ini
        self.fecha_hora_fin = f_fin
        self.fechaHoraFin = f_fin
        self.estado = estado
        self.observaciones = observaciones
        self.creada_en = creada
        self.creadaEn = creada

    def to_dict(self):
        return {
            "id": self.id,
            "servicioId": self.servicio_id,
            "servicioNombre": self.servicio_nombre,
            "clienteEmail": self.cliente_email,
            "clienteNombre": self.cliente_nombre,
            "mascotaId": self.mascota_id,
            "nombreMascota": self.nombre_mascota,
            "fechaHora": self.fecha_hora,
            "fechaHoraFin": self.fecha_hora_fin,
            "estado": self.estado,
            "observaciones": self.observaciones,
            "creadaEn": self.creada_en,
        }

