
from typing import Any, Dict, List, Union
try:
    from dto.auth_dto import MensajeResponse
    from dto.servicio_dto import ServicioRequest, ServicioResponse
    from service.servicio_service import ServicioService
except ImportError:
    from backend.dto.auth_dto import MensajeResponse
    from backend.dto.servicio_dto import ServicioRequest, ServicioResponse
    from backend.service.servicio_service import ServicioService

from .base_controller import ApiResponse


class ServicioController:

    def __init__(self, servicio_service: ServicioService):
        self.servicio_service = servicio_service

    def listar(self) -> ApiResponse[List[ServicioResponse]]:
        servicios = self.servicio_service.listar_activos()
        return ApiResponse.ok([ServicioResponse(**s) for s in servicios])

    def buscar(self, nombre: str) -> ApiResponse[List[ServicioResponse]]:
        servicios = self.servicio_service.buscar(nombre)
        return ApiResponse.ok([ServicioResponse(**s) for s in servicios])

    def obtener(self, id: int) -> ApiResponse[ServicioResponse]:
        servicio = self.servicio_service.obtener(id)
        return ApiResponse.ok(ServicioResponse(**servicio))

    def crear(self, request: Union[ServicioRequest, Dict[str, Any]]) -> ApiResponse[ServicioResponse]:
        if isinstance(request, dict):
            req = ServicioRequest(**request)
        else:
            req = request

        servicio = self.servicio_service.crear(
            nombre=req.nombre,
            precio=req.precio,
            duracion_minutos=req.duracion_minutos,
            descripcion=req.descripcion,
            activo=req.activo if req.activo is not None else True,
        )
        return ApiResponse.created(ServicioResponse(**servicio))

    def actualizar(self, id: int, request: Union[ServicioRequest, Dict[str, Any]]) -> ApiResponse[ServicioResponse]:
        if isinstance(request, dict):
            req = ServicioRequest(**request)
        else:
            req = request

        servicio = self.servicio_service.actualizar(
            id=id,
            nombre=req.nombre,
            precio=req.precio,
            duracion_minutos=req.duracion_minutos,
            descripcion=req.descripcion,
            activo=req.activo,
        )
        return ApiResponse.ok(ServicioResponse(**servicio))

    def eliminar(self, id: int) -> ApiResponse[MensajeResponse]:
        resultado = self.servicio_service.desactivar(id)
        return ApiResponse.ok(MensajeResponse(**resultado))

