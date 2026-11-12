
from decimal import Decimal
from typing import Any, Dict, List, Optional, Union
try:
    from exception.api_exception import ApiException
    from model.atencion import Atencion
    from model.estado_reserva import EstadoReserva
    from repository.atencion_repository import AtencionRepository
    from repository.reserva_repository import ReservaRepository
    from repository.usuario_repository import UsuarioRepository
    from util.email_util import EmailUtil
except ImportError:
    from backend.exception.api_exception import ApiException
    from backend.model.atencion import Atencion
    from backend.model.estado_reserva import EstadoReserva
    from backend.repository.atencion_repository import AtencionRepository
    from backend.repository.reserva_repository import ReservaRepository
    from backend.repository.usuario_repository import UsuarioRepository
    from backend.util.email_util import EmailUtil


class AtencionService:

    def __init__(
        self,
        atencion_repository: AtencionRepository,
        reserva_repository: ReservaRepository,
        usuario_repository: UsuarioRepository,
    ):
        self.atencion_repository = atencion_repository
        self.reserva_repository = reserva_repository
        self.usuario_repository = usuario_repository

    def registrar_atencion(
        self,
        email_veterinario: str,
        reserva_id: int,
        diagnostico_o_detalle: str,
        tratamiento_o_indicaciones: Optional[str] = None,
        peso_kg: Optional[Union[Decimal, float, str]] = None,
    ) -> Dict[str, Any]:
        vet = self._buscar_veterinario(email_veterinario)

        reserva = self.reserva_repository.buscar_por_id(reserva_id)
        if reserva is None:
            raise ApiException(404, "La reserva no existe")

        if self.atencion_repository.existe_por_reserva_id(reserva_id):
            raise ApiException(409, "Ya existe un expediente clínico registrado para esta reserva")

        if not diagnostico_o_detalle or not diagnostico_o_detalle.strip():
            raise ApiException(400, "El diagnóstico o detalle de la atención es obligatorio")

        peso_dec = None
        if peso_kg is not None:
            try:
                peso_dec = Decimal(str(peso_kg))
                if peso_dec <= 0:
                    raise ValueError()
            except Exception:
                raise ApiException(400, "El peso debe ser un valor numérico positivo")

        atencion = Atencion(
            reserva_id=reserva.id,
            peso_kg=peso_dec,
            diagnostico_o_detalle=diagnostico_o_detalle.strip(),
            tratamiento_o_indicaciones=tratamiento_o_indicaciones.strip() if tratamiento_o_indicaciones else None,
            atendido_por_id=vet.id,
        )
        atencion.reserva = reserva
        atencion.atendido_por = vet

        guardada = self.atencion_repository.guardar(atencion)

        reserva.estado = EstadoReserva.ATENDIDA
        self.reserva_repository.guardar(reserva)

        return guardada.to_dict()

    def obtener_por_reserva(self, reserva_id: int) -> Dict[str, Any]:
        atencion = self.atencion_repository.buscar_por_reserva_id(reserva_id)
        if atencion is None:
            raise ApiException(404, "No existe un expediente clínico para esta reserva")
        return atencion.to_dict()

    def listar_por_veterinario(self, email_veterinario: str) -> List[Dict[str, Any]]:
        vet = self._buscar_veterinario(email_veterinario)
        return [a.to_dict() for a in self.atencion_repository.listar_por_veterinario(vet.id)]

    def _buscar_veterinario(self, email: str):
        email_clean = EmailUtil.normalizar(email)
        vet = self.usuario_repository.buscar_por_email(email_clean)
        if vet is None:
            raise ApiException(404, "Veterinario / usuario no encontrado")
        return vet
