
from datetime import datetime
from typing import Any, Dict, List, Union
try:
    from dto.reserva_dto import ReservaRequest, ReservaResponse
    from service.reserva_service import ReservaService
except ImportError:
    from backend.dto.reserva_dto import ReservaRequest, ReservaResponse
    from backend.service.reserva_service import ReservaService

from .base_controller import ApiResponse


class ReservaController:
    def __init__(self, reserva_service: ReservaService):
        self.reserva_service = reserva_service

    def crear(
        self,
        request: Union[ReservaRequest, Dict[str, Any]],
        email_cliente: str,
    ) -> ApiResponse[ReservaResponse]:
        if isinstance(request, dict):
            req = ReservaRequest(**request)
        else:
            req = request

        fecha_dt = req.fecha_hora
        if isinstance(fecha_dt, str):
            fecha_dt = datetime.fromisoformat(fecha_dt.replace("Z", ""))

        reserva = self.reserva_service.crear(
            email_cliente=email_cliente,
            servicio_id=req.servicio_id,
            fecha_hora=fecha_dt,
            mascota_id=req.mascota_id,
            nombre_mascota=req.nombre_mascota,
            observaciones=req.observaciones,
        )
        return ApiResponse.created(ReservaResponse(**reserva))

    def mis_reservas(self, email_cliente: str) -> ApiResponse[List[ReservaResponse]]:
        reservas = self.reserva_service.historial(email_cliente)
        return ApiResponse.ok([ReservaResponse(**r) for r in reservas])

    def cancelar(self, id: int, email_cliente: str) -> ApiResponse[ReservaResponse]:
        reserva = self.reserva_service.cancelar(id, email_cliente)
        return ApiResponse.ok(ReservaResponse(**reserva))

