
from datetime import datetime
from typing import Any, List, Optional
try:
    from model.estado_reserva import EstadoReserva
    from model.reserva import Reserva
except ImportError:
    from backend.model.estado_reserva import EstadoReserva
    from backend.model.reserva import Reserva
from .base_repository import BaseRepository


class ReservaRepository(BaseRepository[Reserva]):

    def __init__(self, session: Optional[Any] = None):
        super().__init__(Reserva, session)

    def historial_por_usuario(self, usuario_id: int) -> List[Reserva]:
        if self.session is not None:
            return (
                self.session.query(Reserva)
                .filter(Reserva.usuario_id == usuario_id)
                .order_by(Reserva.fecha_hora.desc())
                .all()
            )

        return sorted(
            [r for r in self._memoria.values() if r.usuario_id == usuario_id],
            key=lambda r: r.fecha_hora,
            reverse=True,
        )

    def listar_todas(self) -> List[Reserva]:
        if self.session is not None:
            return (
                self.session.query(Reserva)
                .order_by(Reserva.fecha_hora.desc())
                .all()
            )

        return sorted(
            list(self._memoria.values()),
            key=lambda r: r.fecha_hora,
            reverse=True,
        )

    def listar_por_estado(self, estado: EstadoReserva) -> List[Reserva]:
        estado_val = estado.value if hasattr(estado, "value") else str(estado)

        if self.session is not None:
            return (
                self.session.query(Reserva)
                .filter(Reserva.estado == estado)
                .order_by(Reserva.fecha_hora.desc())
                .all()
            )

        return sorted(
            [
                r
                for r in self._memoria.values()
                if (r.estado.value if hasattr(r.estado, "value") else str(r.estado)) == estado_val
            ],
            key=lambda r: r.fecha_hora,
            reverse=True,
        )

    def buscar_con_detalle(self, id: int) -> Optional[Reserva]:
        return self.buscar_por_id(id)

    def contar_cruces(
        self,
        servicio_id: int,
        estado: EstadoReserva,
        inicio: datetime,
        fin: datetime,
    ) -> int:
        if self.session is not None:
            return (
                self.session.query(Reserva.id)
                .filter(
                    Reserva.servicio_id == servicio_id,
                    Reserva.estado == estado,
                    Reserva.fecha_hora < fin,
                    Reserva.fecha_hora_fin > inicio,
                )
                .count()
            )

        estado_val = estado.value if hasattr(estado, "value") else str(estado)
        count = 0
        for r in self._memoria.values():
            r_estado = r.estado.value if hasattr(r.estado, "value") else str(r.estado)
            if r.servicio_id == servicio_id and r_estado == estado_val:
                if r.fecha_hora < fin and r.fecha_hora_fin > inicio:
                    count += 1
        return count

    def existe_por_usuario(self, usuario_id: int) -> bool:
        if self.session is not None:
            return (
                self.session.query(Reserva.id)
                .filter(Reserva.usuario_id == usuario_id)
                .first()
                is not None
            )

        return any(r.usuario_id == usuario_id for r in self._memoria.values())

    def existe_por_mascota(self, mascota_id: int) -> bool:
        if self.session is not None:
            return (
                self.session.query(Reserva.id)
                .filter(Reserva.mascota_id == mascota_id)
                .first()
                is not None
            )

        return any(r.mascota_id == mascota_id for r in self._memoria.values())

    def existe_por_servicio(self, servicio_id: int) -> bool:
        if self.session is not None:
            return (
                self.session.query(Reserva.id)
                .filter(Reserva.servicio_id == servicio_id)
                .first()
                is not None
            )

        return any(r.servicio_id == servicio_id for r in self._memoria.values())
