
from typing import List, Optional
try:
    from dto.reserva_dto import ReservaResponse
    from model.estado_reserva import EstadoReserva
    from service.reserva_service import ReservaService
except ImportError:
    from backend.dto.reserva_dto import ReservaResponse
    from backend.model.estado_reserva import EstadoReserva
    from backend.service.reserva_service import ReservaService

from .base_controller import ApiResponse


class ReservaAdminController:

    def __init__(self, reserva_service: ReservaService):
        self.reserva_service = reserva_service

    def listar(self, estado: Optional[str] = None) -> ApiResponse[List[ReservaResponse]]:
        estado_enum = None
        if estado:
            estado_enum = EstadoReserva(estado.strip().upper())

        reservas = self.reserva_service.listar_todas(estado_enum)
        return ApiResponse.ok([ReservaResponse(**r) for r in reservas])

    def marcar_atendida(self, id: int) -> ApiResponse[ReservaResponse]:
        reserva = self.reserva_service.marcar_atendida(id)
        return ApiResponse.ok(ReservaResponse(**reserva))

