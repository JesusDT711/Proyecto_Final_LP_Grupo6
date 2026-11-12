
from typing import Any, Dict, Optional
from .base import Base, Column, BigInteger, String, relationship


class Rol(Base):

    __tablename__ = "roles"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(20), nullable=False, unique=True)

    # Relación: Un rol puede tener muchos usuarios asignados
    usuarios = relationship("Usuario", back_populates="rol", passive_deletes="all")

    def __init__(self, nombre: Optional[str] = None, id: Optional[int] = None, **kwargs):
        super().__init__(**kwargs)
        if id is not None:
            self.id = id
        if nombre is not None:
            self.nombre = nombre

    def __repr__(self) -> str:
        return f"<Rol(id={self.id}, nombre='{self.nombre}')>"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "nombre": self.nombre,
        }

