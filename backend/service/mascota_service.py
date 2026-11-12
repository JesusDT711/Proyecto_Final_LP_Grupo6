
from datetime import date
from typing import Any, Dict, List, Optional
try:
    from exception.api_exception import ApiException
    from model.mascota import Mascota
    from repository.mascota_repository import MascotaRepository
    from repository.reserva_repository import ReservaRepository
    from repository.usuario_repository import UsuarioRepository
    from util.email_util import EmailUtil
except ImportError:
    from backend.exception.api_exception import ApiException
    from backend.model.mascota import Mascota
    from backend.repository.mascota_repository import MascotaRepository
    from backend.repository.reserva_repository import ReservaRepository
    from backend.repository.usuario_repository import UsuarioRepository
    from backend.util.email_util import EmailUtil


class MascotaService:

    def __init__(
        self,
        mascota_repository: MascotaRepository,
        usuario_repository: UsuarioRepository,
        reserva_repository: ReservaRepository,
    ):
        self.mascota_repository = mascota_repository
        self.usuario_repository = usuario_repository
        self.reserva_repository = reserva_repository

    def registrar(
        self,
        email_cliente: str,
        nombre: str,
        especie: str,
        raza: Optional[str] = None,
        sexo: Optional[str] = None,
        fecha_nacimiento: Optional[date] = None,
    ) -> Dict[str, Any]:
        cliente = self._buscar_usuario(email_cliente)

        if not nombre or not nombre.strip():
            raise ApiException(400, "El nombre de la mascota es obligatorio")
        if not especie or not especie.strip():
            raise ApiException(400, "La especie es obligatoria (ej. Canino, Felino)")

        mascota = Mascota(
            nombre=nombre.strip(),
            especie=especie.strip(),
            raza=raza.strip() if raza else None,
            sexo=sexo.strip() if sexo else None,
            fecha_nacimiento=fecha_nacimiento,
            usuario_id=cliente.id,
        )
        mascota.usuario = cliente
        guardada = self.mascota_repository.guardar(mascota)
        return guardada.to_dict()

    def listar_por_dueno(self, email_cliente: str) -> List[Dict[str, Any]]:
        cliente = self._buscar_usuario(email_cliente)
        return [m.to_dict() for m in self.mascota_repository.listar_por_usuario(cliente.id)]

    def obtener(
        self,
        id: int,
        email_solicitante: Optional[str] = None,
        es_admin: bool = False,
    ) -> Dict[str, Any]:
        mascota = self._buscar_mascota(id)

        if not es_admin and email_solicitante:
            cliente = self._buscar_usuario(email_solicitante)
            if mascota.usuario_id != cliente.id:
                raise ApiException(403, "No tienes permiso para ver esta mascota")

        return mascota.to_dict()

    def actualizar(
        self,
        id: int,
        nombre: str,
        especie: str,
        raza: Optional[str] = None,
        sexo: Optional[str] = None,
        fecha_nacimiento: Optional[date] = None,
        email_solicitante: Optional[str] = None,
        es_admin: bool = False,
    ) -> Dict[str, Any]:
        mascota = self._buscar_mascota(id)

        if not es_admin and email_solicitante:
            cliente = self._buscar_usuario(email_solicitante)
            if mascota.usuario_id != cliente.id:
                raise ApiException(403, "No tienes permiso para modificar esta mascota")

        if not nombre or not nombre.strip():
            raise ApiException(400, "El nombre de la mascota es obligatorio")
        if not especie or not especie.strip():
            raise ApiException(400, "La especie es obligatoria")

        mascota.nombre = nombre.strip()
        mascota.especie = especie.strip()
        mascota.raza = raza.strip() if raza else None
        mascota.sexo = sexo.strip() if sexo else None
        if fecha_nacimiento is not None:
            mascota.fecha_nacimiento = fecha_nacimiento

        guardada = self.mascota_repository.guardar(mascota)
        return guardada.to_dict()

    def eliminar(
        self,
        id: int,
        email_solicitante: Optional[str] = None,
        es_admin: bool = False,
    ) -> Dict[str, str]:
        mascota = self._buscar_mascota(id)

        if not es_admin and email_solicitante:
            cliente = self._buscar_usuario(email_solicitante)
            if mascota.usuario_id != cliente.id:
                raise ApiException(403, "No tienes permiso para eliminar esta mascota")

        if self.reserva_repository.existe_por_mascota(id):
            raise ApiException(409, "No se puede eliminar: la mascota tiene citas registradas en el historial")

        self.mascota_repository.eliminar(mascota)
        return {"mensaje": "Mascota eliminada correctamente"}

    def _buscar_mascota(self, id: int) -> Mascota:
        mascota = self.mascota_repository.buscar_por_id(id)
        if mascota is None:
            raise ApiException(404, "La mascota no existe")
        return mascota

    def _buscar_usuario(self, email: str):
        email_clean = EmailUtil.normalizar(email)
        usuario = self.usuario_repository.buscar_por_email(email_clean)
        if usuario is None:
            raise ApiException(404, "Usuario no encontrado")
        return usuario
