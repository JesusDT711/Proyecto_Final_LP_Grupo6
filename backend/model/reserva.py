
from datetime import datetime
from typing import Any, Dict, Optional, Union
from .base import (
    Base,
    Column,
    BigInteger,
    String,
    DateTime,
    ForeignKey,
    SqlEnum,
    Index,
    func,
    relationship,
)
from .estado_reserva import EstadoReserva


class Reserva(Base):

    __tablename__ = "reservas"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    fecha_hora = Column(DateTime, nullable=False)
    fecha_hora_fin = Column(DateTime, nullable=False)
    mascota_id = Column(
        BigInteger,
        ForeignKey("mascotas.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    usuario_id = Column(
        BigInteger,
        ForeignKey("usuarios.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    servicio_id = Column(
        BigInteger,
        ForeignKey("servicios.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    observaciones = Column(String(500), nullable=True)
    estado = Column(
        SqlEnum(
            EstadoReserva,
            name="estado_reserva_enum",
            native_enum=False,
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
        default=EstadoReserva.CONFIRMADA,
    )
    creada_en = Column(DateTime, nullable=False, server_default=func.now())

    # Índices para acelerar validaciones de horarios y filtrado por estado
    __table_args__ = (
        Index("idx_reservas_fechas", "fecha_hora", "fecha_hora_fin"),
        Index("idx_reservas_estado", "estado"),
    )

    # Relaciones
    mascota = relationship("Mascota", back_populates="reservas")
    usuario = relationship(
        "Usuario",
        back_populates="reservas",
        foreign_keys=[usuario_id],
    )
    servicio = relationship("Servicio", back_populates="reservas")
    atencion = relationship("Atencion", back_populates="reserva", uselist=False)

    def __init__(
        self,
        fecha_hora: Optional[datetime] = None,
        fecha_hora_fin: Optional[datetime] = None,
        mascota_id: Optional[int] = None,
        usuario_id: Optional[int] = None,
        servicio_id: Optional[int] = None,
        observaciones: Optional[str] = None,
        estado: Union[EstadoReserva, str] = EstadoReserva.CONFIRMADA,
        id: Optional[int] = None,
        creada_en: Optional[datetime] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if id is not None:
            self.id = id
        if fecha_hora is not None:
            self.fecha_hora = fecha_hora
        if fecha_hora_fin is not None:
            self.fecha_hora_fin = fecha_hora_fin
        if mascota_id is not None:
            self.mascota_id = mascota_id
        if usuario_id is not None:
            self.usuario_id = usuario_id
        if servicio_id is not None:
            self.servicio_id = servicio_id
        if observaciones is not None:
            self.observaciones = observaciones

        if isinstance(estado, EstadoReserva):
            self.estado = estado
        elif isinstance(estado, str):
            self.estado = EstadoReserva(estado)
        else:
            self.estado = EstadoReserva.CONFIRMADA

        if creada_en is not None:
            self.creada_en = creada_en

    def __repr__(self) -> str:
        return (
            f"<Reserva(id={self.id}, fecha_hora='{self.fecha_hora}', "
            f"mascota_id={self.mascota_id}, usuario_id={self.usuario_id}, "
            f"servicio_id={self.servicio_id}, estado='{self.estado}')>"
        )

    def to_dict(self) -> Dict[str, Any]:

        estado_str = self.estado.value if hasattr(self.estado, "value") else str(self.estado)
        return {
            "id": self.id,
            "servicioId": self.servicio_id,
            "servicio_id": self.servicio_id,
            "servicioNombre": self.servicio.nombre if self.servicio else None,
            "clienteEmail": self.usuario.email if self.usuario else None,
            "clienteNombre": self.usuario.nombre_completo if self.usuario else None,
            "mascotaId": self.mascota_id,
            "mascota_id": self.mascota_id,
            "nombreMascota": self.mascota.nombre if self.mascota else None,
            "fechaHora": self.fecha_hora.isoformat() if self.fecha_hora else None,
            "fecha_hora": self.fecha_hora.isoformat() if self.fecha_hora else None,
            "fechaHoraFin": self.fecha_hora_fin.isoformat() if self.fecha_hora_fin else None,
            "fecha_hora_fin": self.fecha_hora_fin.isoformat() if self.fecha_hora_fin else None,
            "estado": estado_str,
            "observaciones": self.observaciones,
            "creadaEn": self.creada_en.isoformat() if self.creada_en else None,
            "creada_en": self.creada_en.isoformat() if self.creada_en else None,
        }

