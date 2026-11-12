
from typing import Any, List, Optional
try:
    from model.servicio import Servicio
except ImportError:
    from backend.model.servicio import Servicio
from .base_repository import BaseRepository


class ServicioRepository(BaseRepository[Servicio]):

    def __init__(self, session: Optional[Any] = None):
        super().__init__(Servicio, session)

    def listar_activos(self) -> List[Servicio]:
        if self.session is not None:
            return (
                self.session.query(Servicio)
                .filter(Servicio.activo == True)  # noqa: E712
                .order_by(Servicio.nombre.asc())
                .all()
            )

        return sorted(
            [s for s in self._memoria.values() if s.activo],
            key=lambda s: s.nombre.lower() if s.nombre else "",
        )

    def buscar_por_nombre(self, nombre: str) -> List[Servicio]:
        if not nombre:
            return self.listar_activos()
        term = nombre.strip().lower()

        if self.session is not None:
            return (
                self.session.query(Servicio)
                .filter(Servicio.activo == True, Servicio.nombre.ilike(f"%{term}%"))  # noqa: E712
                .order_by(Servicio.nombre.asc())
                .all()
            )

        return sorted(
            [s for s in self._memoria.values() if s.activo and term in (s.nombre or "").lower()],
            key=lambda s: s.nombre.lower() if s.nombre else "",
        )

    def existe_por_nombre_ignore_case(self, nombre: str) -> bool:
        if not nombre:
            return False
        clean = nombre.strip().lower()

        if self.session is not None:
            return (
                self.session.query(Servicio.id)
                .filter(Servicio.nombre.ilike(clean))
                .first()
                is not None
            )

        return any((s.nombre or "").strip().lower() == clean for s in self._memoria.values())

    def existe_por_nombre_ignore_case_y_distinto_id(self, nombre: str, id: int) -> bool:
        if not nombre:
            return False
        clean = nombre.strip().lower()

        if self.session is not None:
            return (
                self.session.query(Servicio.id)
                .filter(Servicio.nombre.ilike(clean), Servicio.id != id)
                .first()
                is not None
            )

        return any(
            (s.nombre or "").strip().lower() == clean and s.id != id
            for s in self._memoria.values()
        )
