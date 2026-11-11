
from datetime import datetime
from typing import Any, Dict, List, Optional
from .base import (
    Base,
    Column,
    BigInteger,
    String,
    ForeignKey,
    DateTime,
    func,
    relationship,
)


class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    nombre_completo = Column(String(255), nullable=False)
    telefono = Column(String(15), nullable=True)
    rol_id = Column(
        BigInteger,
        ForeignKey("roles.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relaciones
    rol = relationship("Rol", back_populates="usuarios")
    mascotas = relationship("Mascota", back_populates="usuario", cascade="all, delete-orphan")
    reservas = relationship(
        "Reserva",
        back_populates="usuario",
        foreign_keys="Reserva.usuario_id",
        passive_deletes="all",
    )
    atenciones_realizadas = relationship(
        "Atencion",
        back_populates="atendido_por",
        foreign_keys="Atencion.atendido_por_id",
    )

    def __init__(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        nombre_completo: Optional[str] = None,
        telefono: Optional[str] = None,
        rol_id: Optional[int] = None,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if id is not None:
            self.id = id
        if email is not None:
            self.email = email
        if password is not None:
            self.password = password
        if nombre_completo is not None:
            self.nombre_completo = nombre_completo
        if telefono is not None:
            self.telefono = telefono
        if rol_id is not None:
            self.rol_id = rol_id
        if created_at is not None:
            self.created_at = created_at

    def __repr__(self) -> str:
        return (
            f"<Usuario(id={self.id}, email='{self.email}', "
            f"nombre_completo='{self.nombre_completo}', rol_id={self.rol_id})>"
        )

    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:    
        data: Dict[str, Any] = {
            "id": self.id,
            "email": self.email,
            "nombreCompleto": self.nombre_completo,
            "nombre_completo": self.nombre_completo,
            "telefono": self.telefono,
            "rolId": self.rol_id,
            "rol_id": self.rol_id,
            "rol": self.rol.nombre if self.rol else None,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_sensitive:
            data["password"] = self.password
        return data

