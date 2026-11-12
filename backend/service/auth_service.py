
from typing import Any, Dict, Optional
try:
    from exception.api_exception import ApiException
    from model.usuario import Usuario
    from repository.rol_repository import RolRepository
    from repository.usuario_repository import UsuarioRepository
    from util.email_util import EmailUtil
    from util.seguridad_util import SeguridadUtil
except ImportError:
    from backend.exception.api_exception import ApiException
    from backend.model.usuario import Usuario
    from backend.repository.rol_repository import RolRepository
    from backend.repository.usuario_repository import UsuarioRepository
    from backend.util.email_util import EmailUtil
    from backend.util.seguridad_util import SeguridadUtil


class AuthService:

    def __init__(
        self,
        usuario_repository: UsuarioRepository,
        rol_repository: RolRepository,
    ):
        self.usuario_repository = usuario_repository
        self.rol_repository = rol_repository

    def registrar(
        self,
        nombre_completo: str,
        email: str,
        password: str,
        telefono: Optional[str] = None,
    ) -> Dict[str, str]:
        if not nombre_completo or not nombre_completo.strip():
            raise ApiException(400, "El nombre completo es obligatorio")
        if not email or not email.strip():
            raise ApiException(400, "El correo es obligatorio")
        if not password or len(password) < 6:
            raise ApiException(400, "La contraseña debe tener al menos 6 caracteres")

        email_clean = EmailUtil.normalizar(email)
        if self.usuario_repository.existe_por_email(email_clean):
            raise ApiException(409, "El correo ya está registrado")

        rol_cliente = self.rol_repository.buscar_por_nombre("CLIENTE")
        if rol_cliente is None:
            rol_cliente = self.rol_repository.guardar(self.rol_repository.model_class(nombre="CLIENTE"))

        password_hash = SeguridadUtil.encriptar_password(password)

        usuario = Usuario(
            email=email_clean,
            password=password_hash,
            nombre_completo=nombre_completo.strip(),
            telefono=telefono.strip() if telefono else None,
            rol_id=rol_cliente.id,
        )
        usuario.rol = rol_cliente
        self.usuario_repository.guardar(usuario)

        return {"mensaje": "Usuario registrado correctamente"}

    def login(self, email: str, password: str) -> Dict[str, Any]:
        if not email or not password:
            raise ApiException(401, "Correo o contraseña incorrectos")

        email_clean = EmailUtil.normalizar(email)
        usuario = self.usuario_repository.buscar_por_email(email_clean)

        if usuario is None or not SeguridadUtil.verificar_password(password, usuario.password):
            raise ApiException(401, "Correo o contraseña incorrectos")

        rol_nombre = usuario.rol.nombre if usuario.rol else "CLIENTE"
        token = SeguridadUtil.generar_token(
            email=usuario.email,
            rol=rol_nombre,
            nombre_completo=usuario.nombre_completo,
        )

        return {
            "token": token,
            "email": usuario.email,
            "nombreCompleto": usuario.nombre_completo,
            "rol": rol_nombre,
        }
