
from typing import Any, Dict, Union
try:
    from dto.auth_dto import AuthResponse, LoginRequest, MensajeResponse, RegistroRequest
    from service.auth_service import AuthService
except ImportError:
    from backend.dto.auth_dto import AuthResponse, LoginRequest, MensajeResponse, RegistroRequest
    from backend.service.auth_service import AuthService

from .base_controller import ApiResponse


class AuthController:

    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def registrar(self, request: Union[RegistroRequest, Dict[str, Any]]) -> ApiResponse[MensajeResponse]:
        if isinstance(request, dict):
            req = RegistroRequest(**request)
        else:
            req = request

        resultado = self.auth_service.registrar(
            nombre_completo=req.nombre_completo,
            email=req.email,
            password=req.password,
            telefono=req.telefono,
        )
        return ApiResponse.created(MensajeResponse(**resultado))

    def login(self, request: Union[LoginRequest, Dict[str, Any]]) -> ApiResponse[AuthResponse]:
        if isinstance(request, dict):
            req = LoginRequest(**request)
        else:
            req = request

        resultado = self.auth_service.login(
            email=req.email,
            password=req.password,
        )
        return ApiResponse.ok(AuthResponse(**resultado))

