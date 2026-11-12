
from typing import Any, Optional
try:
    from model.rol import Rol
except ImportError:
    from backend.model.rol import Rol
from .base_repository import BaseRepository


class RolRepository(BaseRepository[Rol]):

    def __init__(self, session: Optional[Any] = None):
        super().__init__(Rol, session)

    def buscar_por_nombre(self, nombre: str) -> Optional[Rol]:
        if not nombre:
            return None
        nombre_clean = nombre.strip().upper()

        if self.session is not None:
            return self.session.query(Rol).filter(Rol.nombre == nombre_clean).first()

        for r in self._memoria.values():
            if r.nombre and r.nombre.upper() == nombre_clean:
                return r
        return None
