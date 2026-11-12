
from typing import Any, List, Optional
try:
    from model.atencion import Atencion
except ImportError:
    from backend.model.atencion import Atencion
from .base_repository import BaseRepository


class AtencionRepository(BaseRepository[Atencion]):

    def __init__(self, session: Optional[Any] = None):
        super().__init__(Atencion, session)

    def buscar_por_reserva_id(self, reserva_id: int) -> Optional[Atencion]:
        if self.session is not None:
            return (
                self.session.query(Atencion)
                .filter(Atencion.reserva_id == reserva_id)
                .first()
            )

        for a in self._memoria.values():
            if a.reserva_id == reserva_id:
                return a
        return None

    def existe_por_reserva_id(self, reserva_id: int) -> bool:
        if self.session is not None:
            return (
                self.session.query(Atencion.id)
                .filter(Atencion.reserva_id == reserva_id)
                .first()
                is not None
            )

        return any(a.reserva_id == reserva_id for a in self._memoria.values())

    def listar_por_veterinario(self, atendido_por_id: int) -> List[Atencion]:
        if self.session is not None:
            return (
                self.session.query(Atencion)
                .filter(Atencion.atendido_por_id == atendido_por_id)
                .order_by(Atencion.fecha_atencion.desc())
                .all()
            )

        return sorted(
            [a for a in self._memoria.values() if a.atendido_por_id == atendido_por_id],
            key=lambda a: a.fecha_atencion,
            reverse=True,
        )
