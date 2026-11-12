
from datetime import date
from typing import Any, Dict, List, Optional, Union
try:
    from dto.auth_dto import MensajeResponse
    from dto.mascota_dto import MascotaRequest, MascotaResponse
    from service.mascota_service import MascotaService
except ImportError:
    from backend.dto.auth_dto import MensajeResponse
    from backend.dto.mascota_dto import MascotaRequest, MascotaResponse
    from backend.service.mascota_service import MascotaService

from .base_controller import ApiResponse


class MascotaController:

    def __init__(self, mascota_service: MascotaService):
        self.mascota_service = mascota_service

    def registrar(
        self,
        request: Union[MascotaRequest, Dict[str, Any]],
        email_cliente: str,
    ) -> ApiResponse[MascotaResponse]:
        if isinstance(request, dict):
            req = MascotaRequest(**request)
        else:
            req = request

        fecha_nac = None
        if req.fecha_nacimiento:
            if isinstance(req.fecha_nacimiento, str):
                fecha_nac = date.fromisoformat(req.fecha_nacimiento)
            else:
                fecha_nac = req.fecha_nacimiento

        mascota = self.mascota_service.registrar(
            email_cliente=email_cliente,
            nombre=req.nombre,
            especie=req.especie,
            raza=req.raza,
            sexo=req.sexo,
            fecha_nacimiento=fecha_nac,
        )
        return ApiResponse.created(MascotaResponse(**mascota))

    def mis_mascotas(self, email_cliente: str) -> ApiResponse[List[MascotaResponse]]:
        mascotas = self.mascota_service.listar_por_dueno(email_cliente)
        return ApiResponse.ok([MascotaResponse(**m) for m in mascotas])

    def obtener(
        self,
        id: int,
        email_solicitante: Optional[str] = None,
        es_admin: bool = False,
    ) -> ApiResponse[MascotaResponse]:
        mascota = self.mascota_service.obtener(id, email_solicitante, es_admin)
        return ApiResponse.ok(MascotaResponse(**mascota))

    def actualizar(
        self,
        id: int,
        request: Union[MascotaRequest, Dict[str, Any]],
        email_solicitante: Optional[str] = None,
        es_admin: bool = False,
    ) -> ApiResponse[MascotaResponse]:
        if isinstance(request, dict):
            req = MascotaRequest(**request)
        else:
            req = request

        fecha_nac = None
        if req.fecha_nacimiento:
            if isinstance(req.fecha_nacimiento, str):
                fecha_nac = date.fromisoformat(req.fecha_nacimiento)
            else:
                fecha_nac = req.fecha_nacimiento

        mascota = self.mascota_service.actualizar(
            id=id,
            nombre=req.nombre,
            especie=req.especie,
            raza=req.raza,
            sexo=req.sexo,
            fecha_nacimiento=fecha_nac,
            email_solicitante=email_solicitante,
            es_admin=es_admin,
        )
        return ApiResponse.ok(MascotaResponse(**mascota))

    def eliminar(
        self,
        id: int,
        email_solicitante: Optional[str] = None,
        es_admin: bool = False,
    ) -> ApiResponse[MensajeResponse]:
        resultado = self.mascota_service.eliminar(id, email_solicitante, es_admin)
        return ApiResponse.ok(MensajeResponse(**resultado))

