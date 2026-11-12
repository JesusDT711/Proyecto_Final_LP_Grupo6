
from typing import Any, Dict, List, Union
try:
    from dto.atencion_dto import AtencionRequest, AtencionResponse
    from service.atencion_service import AtencionService
except ImportError:
    from backend.dto.atencion_dto import AtencionRequest, AtencionResponse
    from backend.service.atencion_service import AtencionService

from .base_controller import ApiResponse


class AtencionController:

    def __init__(self, atencion_service: AtencionService):
        self.atencion_service = atencion_service

    def registrar(
        self,
        request: Union[AtencionRequest, Dict[str, Any]],
        email_veterinario: str,
    ) -> ApiResponse[AtencionResponse]:
        if isinstance(request, dict):
            req = AtencionRequest(**request)
        else:
            req = request

        atencion = self.atencion_service.registrar_atencion(
            email_veterinario=email_veterinario,
            reserva_id=req.reserva_id,
            diagnostico_o_detalle=req.diagnostico_o_detalle,
            tratamiento_o_indicaciones=req.tratamiento_o_indicaciones,
            peso_kg=req.peso_kg,
        )
        return ApiResponse.created(AtencionResponse(**atencion))

    def obtener_por_reserva(self, reserva_id: int) -> ApiResponse[AtencionResponse]:
        atencion = self.atencion_service.obtener_por_reserva(reserva_id)
        return ApiResponse.ok(AtencionResponse(**atencion))

    def mis_atenciones(self, email_veterinario: str) -> ApiResponse[List[AtencionResponse]]:
        atenciones = self.atencion_service.listar_por_veterinario(email_veterinario)
        return ApiResponse.ok([AtencionResponse(**a) for a in atenciones])

