
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
try:
    from exception.api_exception import ApiException
    from model.estado_reserva import EstadoReserva
    from model.reserva import Reserva
    from model.servicio import Servicio
    from model.usuario import Usuario
    from repository.mascota_repository import MascotaRepository
    from repository.reserva_repository import ReservaRepository
    from repository.servicio_repository import ServicioRepository
    from repository.usuario_repository import UsuarioRepository
    from service.horario_atencion import HorarioAtencion
    from util.email_util import EmailUtil
except ImportError:
    from backend.exception.api_exception import ApiException
    from backend.model.estado_reserva import EstadoReserva
    from backend.model.reserva import Reserva
    from backend.model.servicio import Servicio
    from backend.model.usuario import Usuario
    from backend.repository.mascota_repository import MascotaRepository
    from backend.repository.reserva_repository import ReservaRepository
    from backend.repository.servicio_repository import ServicioRepository
    from backend.repository.usuario_repository import UsuarioRepository
    from backend.service.horario_atencion import HorarioAtencion
    from backend.util.email_util import EmailUtil


class ReservaService:

    HORAS_MINIMAS_PARA_CANCELAR: int = 24

    def __init__(
        self,
        reserva_repository: ReservaRepository,
        servicio_repository: ServicioRepository,
        usuario_repository: UsuarioRepository,
        mascota_repository: MascotaRepository,
        horario_atencion: Optional[HorarioAtencion] = None,
    ):
        self.reserva_repository = reserva_repository
        self.servicio_repository = servicio_repository
        self.usuario_repository = usuario_repository
        self.mascota_repository = mascota_repository
        self.horario_atencion = horario_atencion or HorarioAtencion()

    def crear(
        self,
        email_cliente: str,
        servicio_id: int,
        fecha_hora: datetime,
        mascota_id: Optional[int] = None,
        nombre_mascota: Optional[str] = None,
        observaciones: Optional[str] = None,
    ) -> Dict[str, Any]:
        cliente = self._buscar_usuario(email_cliente)

        servicio = self.servicio_repository.buscar_por_id(servicio_id)
        if servicio is None:
            raise ApiException(404, "El servicio no existe")
        if not servicio.activo:
            raise ApiException(400, "El servicio no está disponible")

        inicio = fecha_hora
        fin = inicio + timedelta(minutes=servicio.duracion_minutos)

        if inicio <= datetime.now():
            raise ApiException(400, "La fecha y hora de la reserva deben ser futuras")

        error_horario = self.horario_atencion.validar(inicio, fin)
        if error_horario:
            raise ApiException(400, error_horario)

        cruces = self.reserva_repository.contar_cruces(
            servicio_id=servicio.id,
            estado=EstadoReserva.CONFIRMADA,
            inicio=inicio,
            fin=fin,
        )
        if cruces > 0:
            raise ApiException(409, "Ese horario ya está ocupado para este servicio. Elige otra hora")

        mascota = None
        if mascota_id:
            mascota = self.mascota_repository.buscar_por_id(mascota_id)
        elif nombre_mascota and nombre_mascota.strip():
            mascotas_cliente = self.mascota_repository.listar_por_usuario(cliente.id)
            for m in mascotas_cliente:
                if m.nombre.lower() == nombre_mascota.strip().lower():
                    mascota = m
                    break
            if mascota is None:
                # Si no existe, crear la mascota asociada
                try:
                    from model.mascota import Mascota
                except ImportError:
                    from backend.model.mascota import Mascota
                mascota = self.mascota_repository.guardar(
                    Mascota(
                        nombre=nombre_mascota.strip(),
                        especie="Mascota",
                        usuario_id=cliente.id,
                    )
                )

        if mascota is None:
            raise ApiException(400, "Debes especificar la mascota para la cita")

        reserva = Reserva(
            fecha_hora=inicio,
            fecha_hora_fin=fin,
            mascota_id=mascota.id,
            usuario_id=cliente.id,
            servicio_id=servicio.id,
            observaciones=observaciones.strip() if observaciones else None,
            estado=EstadoReserva.CONFIRMADA,
            creada_en=datetime.now(),
        )
        reserva.usuario = cliente
        reserva.servicio = servicio
        reserva.mascota = mascota

        guardada = self.reserva_repository.guardar(reserva)
        return guardada.to_dict()

    def historial(self, email_cliente: str) -> List[Dict[str, Any]]:
        cliente = self._buscar_usuario(email_cliente)
        return [r.to_dict() for r in self.reserva_repository.historial_por_usuario(cliente.id)]

    def cancelar(self, id: int, email_solicitante: str) -> Dict[str, Any]:
        reserva = self._buscar_reserva(id)

        email_cliente = reserva.usuario.email if reserva.usuario else None
        if not email_cliente:
            u = self.usuario_repository.buscar_por_id(reserva.usuario_id)
            email_cliente = u.email if u else None

        if EmailUtil.normalizar(email_cliente) != EmailUtil.normalizar(email_solicitante):
            raise ApiException(403, "No puedes cancelar la reserva de otro cliente")

        estado_actual = reserva.estado.value if hasattr(reserva.estado, "value") else str(reserva.estado)
        if estado_actual != EstadoReserva.CONFIRMADA.value:
            raise ApiException(409, "Solo se pueden cancelar reservas confirmadas")

        limite_cancelacion = reserva.fecha_hora - timedelta(hours=self.HORAS_MINIMAS_PARA_CANCELAR)
        if datetime.now() > limite_cancelacion:
            raise ApiException(
                400,
                f"Solo puedes cancelar una reserva con al menos {self.HORAS_MINIMAS_PARA_CANCELAR} horas de anticipación",
            )

        reserva.estado = EstadoReserva.CANCELADA
        guardada = self.reserva_repository.guardar(reserva)
        return guardada.to_dict()

    def listar_todas(self, estado: Optional[EstadoReserva] = None) -> List[Dict[str, Any]]:
        if estado is None:
            reservas = self.reserva_repository.listar_todas()
        else:
            reservas = self.reserva_repository.listar_por_estado(estado)

        return [r.to_dict() for r in reservas]

    def marcar_atendida(self, id: int) -> Dict[str, Any]:
        reserva = self._buscar_reserva(id)

        estado_actual = reserva.estado.value if hasattr(reserva.estado, "value") else str(reserva.estado)
        if estado_actual != EstadoReserva.CONFIRMADA.value:
            raise ApiException(409, "Solo se pueden marcar como atendidas las reservas confirmadas")

        reserva.estado = EstadoReserva.ATENDIDA
        guardada = self.reserva_repository.guardar(reserva)
        return guardada.to_dict()

    def _buscar_usuario(self, email: str) -> Usuario:
        email_clean = EmailUtil.normalizar(email)
        usuario = self.usuario_repository.buscar_por_email(email_clean)
        if usuario is None:
            raise ApiException(404, "Usuario no encontrado")
        return usuario

    def _buscar_reserva(self, id: int) -> Reserva:
        reserva = self.reserva_repository.buscar_con_detalle(id)
        if reserva is None:
            raise ApiException(404, "La reserva no existe")
        return reserva
