
from datetime import date, datetime
from typing import Any, Dict, Optional
from .base import (
    Base,
    Column,
    BigInteger,
    String,
    Date,
    ForeignKey,
    DateTime,
    Index,
    func,
    relationship,
)


class Mascota(Base):

    __tablename__ = "mascotas"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    especie = Column(String(50), nullable=False)
    raza = Column(String(100), nullable=True)
    sexo = Column(String(15), nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    usuario_id = Column(
        BigInteger,
        ForeignKey("usuarios.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # Índices adicionales definidos en el script SQL
    __table_args__ = (
        Index("idx_mascotas_usuario", "usuario_id"),
    )

    # Relaciones
    usuario = relationship("Usuario", back_populates="mascotas")
    reservas = relationship(
        "Reserva",
        back_populates="mascota",
        passive_deletes="all",
    )

    def __init__(
        self,
        nombre: Optional[str] = None,
        especie: Optional[str] = None,
        usuario_id: Optional[int] = None,
        raza: Optional[str] = None,
        sexo: Optional[str] = None,
        fecha_nacimiento: Optional[date] = None,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if id is not None:
            self.id = id
        if nombre is not None:
            self.nombre = nombre
        if especie is not None:
            self.especie = especie
        if raza is not None:
            self.raza = raza
        if sexo is not None:
            self.sexo = sexo
        if fecha_nacimiento is not None:
            self.fecha_nacimiento = fecha_nacimiento
        if usuario_id is not None:
            self.usuario_id = usuario_id
        if created_at is not None:
            self.created_at = created_at

    def __repr__(self) -> str:
        return (
            f"<Mascota(id={self.id}, nombre='{self.nombre}', especie='{self.especie}', "
            f"raza='{self.raza}', usuario_id={self.usuario_id})>"
        )

    def to_dict(self) -> Dict[str, Any]:

        return {
            "id": self.id,
            "nombre": self.nombre,
            "especie": self.especie,
            "raza": self.raza,
            "sexo": self.sexo,
            "fechaNacimiento": self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            "fecha_nacimiento": self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            "usuarioId": self.usuario_id,
            "usuario_id": self.usuario_id,
            "propietarioNombre": self.usuario.nombre_completo if self.usuario else None,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

