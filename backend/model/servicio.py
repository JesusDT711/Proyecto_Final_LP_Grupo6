
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional, Union
from .base import (
    Base,
    Column,
    BigInteger,
    String,
    Numeric,
    Integer,
    Boolean,
    DateTime,
    func,
    relationship,
)


class Servicio(Base):

    __tablename__ = "servicios"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(500), nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    duracion_minutos = Column(Integer, nullable=False)
    activo = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relaciones: Un servicio puede estar asociado a múltiples reservas históricas y futuras
    reservas = relationship(
        "Reserva",
        back_populates="servicio",
        passive_deletes="all",
    )

    def __init__(
        self,
        nombre: Optional[str] = None,
        precio: Optional[Union[Decimal, float, str]] = None,
        duracion_minutos: Optional[int] = None,
        descripcion: Optional[str] = None,
        activo: bool = True,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if id is not None:
            self.id = id
        if nombre is not None:
            self.nombre = nombre
        if descripcion is not None:
            self.descripcion = descripcion
        if precio is not None:
            self.precio = Decimal(str(precio))
        if duracion_minutos is not None:
            self.duracion_minutos = duracion_minutos
        self.activo = activo
        if created_at is not None:
            self.created_at = created_at

    def __repr__(self) -> str:
        return (
            f"<Servicio(id={self.id}, nombre='{self.nombre}', precio={self.precio}, "
            f"duracion_minutos={self.duracion_minutos}, activo={self.activo})>"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": float(self.precio) if self.precio is not None else 0.0,
            "duracionMinutos": self.duracion_minutos,
            "duracion_minutos": self.duracion_minutos,
            "activo": self.activo,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

