
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional, Union
from .base import (
    Base,
    Column,
    BigInteger,
    String,
    Numeric,
    DateTime,
    ForeignKey,
    func,
    relationship,
)


class Atencion(Base):

    __tablename__ = "atenciones"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    reserva_id = Column(
        BigInteger,
        ForeignKey("reservas.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        unique=True,
    )
    peso_kg = Column(Numeric(5, 2), nullable=True)
    diagnostico_o_detalle = Column(String(1000), nullable=False)
    tratamiento_o_indicaciones = Column(String(1000), nullable=True)
    fecha_atencion = Column(DateTime, nullable=False, server_default=func.now())
    atendido_por_id = Column(
        BigInteger,
        ForeignKey("usuarios.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )

    # Relaciones
    reserva = relationship("Reserva", back_populates="atencion")
    atendido_por = relationship(
        "Usuario",
        back_populates="atenciones_realizadas",
        foreign_keys=[atendido_por_id],
    )

    def __init__(
        self,
        reserva_id: Optional[int] = None,
        diagnostico_o_detalle: Optional[str] = None,
        tratamiento_o_indicaciones: Optional[str] = None,
        peso_kg: Optional[Union[Decimal, float, str]] = None,
        atendido_por_id: Optional[int] = None,
        id: Optional[int] = None,
        fecha_atencion: Optional[datetime] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if id is not None:
            self.id = id
        if reserva_id is not None:
            self.reserva_id = reserva_id
        if peso_kg is not None:
            self.peso_kg = Decimal(str(peso_kg))
        if diagnostico_o_detalle is not None:
            self.diagnostico_o_detalle = diagnostico_o_detalle
        if tratamiento_o_indicaciones is not None:
            self.tratamiento_o_indicaciones = tratamiento_o_indicaciones
        if atendido_por_id is not None:
            self.atendido_por_id = atendido_por_id
        if fecha_atencion is not None:
            self.fecha_atencion = fecha_atencion

    def __repr__(self) -> str:
        return (
            f"<Atencion(id={self.id}, reserva_id={self.reserva_id}, "
            f"peso_kg={self.peso_kg}, atendido_por_id={self.atendido_por_id})>"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "reservaId": self.reserva_id,
            "reserva_id": self.reserva_id,
            "pesoKg": float(self.peso_kg) if self.peso_kg is not None else None,
            "peso_kg": float(self.peso_kg) if self.peso_kg is not None else None,
            "diagnosticoODetalle": self.diagnostico_o_detalle,
            "diagnostico_o_detalle": self.diagnostico_o_detalle,
            "tratamientoOIndicaciones": self.tratamiento_o_indicaciones,
            "tratamiento_o_indicaciones": self.tratamiento_o_indicaciones,
            "fechaAtencion": self.fecha_atencion.isoformat() if self.fecha_atencion else None,
            "fecha_atencion": self.fecha_atencion.isoformat() if self.fecha_atencion else None,
            "atendidoPorId": self.atendido_por_id,
            "atendido_por_id": self.atendido_por_id,
            "atendidoPorNombre": self.atendido_por.nombre_completo if self.atendido_por else None,
        }

