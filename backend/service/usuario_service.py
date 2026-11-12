
from typing import Any, Dict, List, Optional
try:
    from exception.api_exception import ApiException
    from model.usuario import Usuario
    from repository.reserva_repository import ReservaRepository
    from repository.rol_repository import RolRepository
    from repository.usuario_repository import UsuarioRepository
    from util.email_util import EmailUtil
    from util.seguridad_util import SeguridadUtil
except ImportError:
    from backend.exception.api_exception import ApiException
    from backend.model.usuario import Usuario
    from backend.repository.reserva_repository import ReservaRepository
    from backend.repository.rol_repository import RolRepository
    from backend.repository.usuario_repository import UsuarioRepository
    from backend.util.email_util import EmailUtil
    from backend.util.seguridad_util import SeguridadUtil


class UsuarioService:

    def __init__(
        self,
        usuario_repository: UsuarioRepository,
        rol_repository: RolRepository,
        reserva_repository: ReservaRepository,
    ):
        self.usuario_repository = usuario_repository
        self.rol_repository = rol_repository
        self.reserva_repository = reserva_repository

    def listar(self) -> List[Dict[str, Any]]:   
        return [u.to_dict() for u in self.usuario_repository.listar_todos()]

    def obtener(self, id: int) -> Dict[str, Any]:
        usuario = self._buscar_por_id(id)
        return usuario.to_dict()

    def actualizar(
        self,
        id: int,
        nombre_completo: str,
        email: str,
        password: Optional[str] = None,
        rol_nombre: Optional[str] = None,
        telefono: Optional[str] = None,
        email_solicitante: Optional[str] = None,
    ) -> Dict[str, Any]:
        usuario = self._buscar_por_id(id)
        es_el_mismo_admin = (usuario.email == email_solicitante)

        nuevo_email = EmailUtil.normalizar(email)
        if self.usuario_repository.existe_por_email_y_distinto_id(nuevo_email, id):
            raise ApiException(409, "Ese correo ya pertenece a otro usuario")

        # Modificación de rol si se especifica
        if rol_nombre and rol_nombre.strip():
            nombre_rol_clean = rol_nombre.strip().upper()
            nuevo_rol = self.rol_repository.buscar_por_nombre(nombre_rol_clean)
            if nuevo_rol is None:
                raise ApiException(400, f"El rol '{rol_nombre}' no existe. Usa ADMIN o CLIENTE")

            # Evita que un administrador se retire a sí mismo sus permisos
            rol_actual = usuario.rol.nombre if usuario.rol else ""
            if es_el_mismo_admin and nuevo_rol.nombre != rol_actual:
                raise ApiException(400, "No puedes cambiar tu propio rol")

            usuario.rol = nuevo_rol
            usuario.rol_id = nuevo_rol.id

        usuario.nombre_completo = nombre_completo.strip()
        usuario.email = nuevo_email
        if telefono is not None:
            usuario.telefono = telefono.strip()

        # Contraseña opcional (solo se actualiza si se envía una nueva)
        if password and password.strip():
            if len(password.strip()) < 6:
                raise ApiException(400, "La contraseña debe tener al menos 6 caracteres")
            usuario.password = SeguridadUtil.encriptar_password(password.strip())

        usuario_guardado = self.usuario_repository.guardar(usuario)
        return usuario_guardado.to_dict()

    def eliminar(self, id: int, email_solicitante: Optional[str] = None) -> Dict[str, str]:
        usuario = self._buscar_por_id(id)

        if email_solicitante and usuario.email == email_solicitante:
            raise ApiException(400, "No puedes eliminar tu propia cuenta")

        if self.reserva_repository.existe_por_usuario(id):
            raise ApiException(409, "No se puede eliminar: el usuario tiene reservas registradas")

        self.usuario_repository.eliminar(usuario)
        return {"mensaje": "Usuario eliminado correctamente"}

    def _buscar_por_id(self, id: int) -> Usuario:
        usuario = self.usuario_repository.buscar_por_id(id)
        if usuario is None:
            raise ApiException(404, "El usuario no existe")
        return usuario
