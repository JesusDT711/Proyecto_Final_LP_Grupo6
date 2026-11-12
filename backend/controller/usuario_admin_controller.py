
from typing import Any, Dict, List, Union
try:
    from dto.auth_dto import MensajeResponse
    from dto.usuario_dto import UsuarioResponse, UsuarioUpdateRequest
    from service.usuario_service import UsuarioService
except ImportError:
    from backend.dto.auth_dto import MensajeResponse
    from backend.dto.usuario_dto import UsuarioResponse, UsuarioUpdateRequest
    from backend.service.usuario_service import UsuarioService

from .base_controller import ApiResponse


class UsuarioAdminController:

    def __init__(self, usuario_service: UsuarioService):
        self.usuario_service = usuario_service

    def listar(self) -> ApiResponse[List[UsuarioResponse]]:
        usuarios = self.usuario_service.listar()
        return ApiResponse.ok([UsuarioResponse(**u) for u in usuarios])

    def obtener(self, id: int) -> ApiResponse[UsuarioResponse]:
        usuario = self.usuario_service.obtener(id)
        return ApiResponse.ok(UsuarioResponse(**usuario))

    def actualizar(
        self,
        id: int,
        request: Union[UsuarioUpdateRequest, Dict[str, Any]],
        email_solicitante: str,
    ) -> ApiResponse[UsuarioResponse]:
        if isinstance(request, dict):
            req = UsuarioUpdateRequest(**request)
        else:
            req = request

        usuario = self.usuario_service.actualizar(
            id=id,
            nombre_completo=req.nombre_completo,
            email=req.email,
            password=req.password,
            rol_nombre=req.rol,
            telefono=req.telefono,
            email_solicitante=email_solicitante,
        )
        return ApiResponse.ok(UsuarioResponse(**usuario))

    def eliminar(self, id: int, email_solicitante: str) -> ApiResponse[MensajeResponse]:
        resultado = self.usuario_service.eliminar(id, email_solicitante)
        return ApiResponse.ok(MensajeResponse(**resultado))

