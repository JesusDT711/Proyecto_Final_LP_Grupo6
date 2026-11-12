
from typing import Any, List, Optional
try:
    from model.mascota import Mascota
except ImportError:
    from backend.model.mascota import Mascota
from .base_repository import BaseRepository


class MascotaRepository(BaseRepository[Mascota]):
    def __init__(self, session: Optional[Any] = None):
        super().__init__(Mascota, session)

    def listar_por_usuario(self, usuario_id: int) -> List[Mascota]:
        if self.session is not None:
            return (
                self.session.query(Mascota)
                .filter(Mascota.usuario_id == usuario_id)
                .order_by(Mascota.nombre.asc())
                .all()
            )

        return sorted(
            [m for m in self._memoria.values() if m.usuario_id == usuario_id],
            key=lambda m: m.nombre.lower() if m.nombre else "",
        )

    def buscar_por_id_y_usuario(self, id: int, usuario_id: int) -> Optional[Mascota]:
        if self.session is not None:
            return (
                self.session.query(Mascota)
                .filter(Mascota.id == id, Mascota.usuario_id == usuario_id)
                .first()
            )

        for m in self._memoria.values():
            if m.id == id and m.usuario_id == usuario_id:
                return m
        return None

    def existe_por_usuario(self, usuario_id: int) -> bool:
        if self.session is not None:
            return (
                self.session.query(Mascota.id)
                .filter(Mascota.usuario_id == usuario_id)
                .first()
                is not None
            )

        return any(m.usuario_id == usuario_id for m in self._memoria.values())
