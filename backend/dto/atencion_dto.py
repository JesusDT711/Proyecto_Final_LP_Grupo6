
from typing import Optional
from .base_dto import BaseDto


class AtencionRequest(BaseDto):
    reserva_id: int
    diagnostico_o_detalle: str
    tratamiento_o_indicaciones: Optional[str] = None
    peso_kg: Optional[float] = None

    def __init__(
        self,
        reserva_id: int = 0,
        diagnostico_o_detalle: str = "",
        tratamiento_o_indicaciones: Optional[str] = None,
        peso_kg: Optional[float] = None,
        reservaId: Optional[int] = None,
        diagnosticoODetalle: Optional[str] = None,
        tratamientoOIndicaciones: Optional[str] = None,
        pesoKg: Optional[float] = None,
        **kwargs,
    ):
        r_id = reservaId if reservaId is not None else reserva_id
        diag = diagnosticoODetalle or diagnostico_o_detalle
        trat = tratamientoOIndicaciones or tratamiento_o_indicaciones
        p_kg = pesoKg if pesoKg is not None else peso_kg

        super().__init__(
            reserva_id=r_id,
            diagnostico_o_detalle=diag,
            tratamiento_o_indicaciones=trat,
            peso_kg=p_kg,
            **kwargs,
        )
        self.reserva_id = r_id
        self.reservaId = r_id
        self.diagnostico_o_detalle = diag
        self.diagnosticoODetalle = diag
        self.tratamiento_o_indicaciones = trat
        self.tratamientoOIndicaciones = trat
        self.peso_kg = p_kg
        self.pesoKg = p_kg


class AtencionResponse(BaseDto):
    id: int
    reserva_id: int
    peso_kg: Optional[float] = None
    diagnostico_o_detalle: str
    tratamiento_o_indicaciones: Optional[str] = None
    fecha_atencion: Optional[str] = None
    atendido_por_id: Optional[int] = None
    atendido_por_nombre: Optional[str] = None

    def __init__(
        self,
        id: int = 0,
        reserva_id: int = 0,
        diagnostico_o_detalle: str = "",
        peso_kg: Optional[float] = None,
        tratamiento_o_indicaciones: Optional[str] = None,
        fecha_atencion: Optional[str] = None,
        atendido_por_id: Optional[int] = None,
        atendido_por_nombre: Optional[str] = None,
        reservaId: Optional[int] = None,
        diagnosticoODetalle: Optional[str] = None,
        tratamientoOIndicaciones: Optional[str] = None,
        pesoKg: Optional[float] = None,
        fechaAtencion: Optional[str] = None,
        atendidoPorId: Optional[int] = None,
        atendidoPorNombre: Optional[str] = None,
        **kwargs,
    ):
        r_id = reservaId if reservaId is not None else reserva_id
        diag = diagnosticoODetalle or diagnostico_o_detalle
        trat = tratamientoOIndicaciones or tratamiento_o_indicaciones
        p_kg = pesoKg if pesoKg is not None else peso_kg
        f_aten = fechaAtencion or fecha_atencion
        at_id = atendidoPorId if atendidoPorId is not None else atendido_por_id
        at_nom = atendidoPorNombre or atendido_por_nombre

        super().__init__(
            id=id,
            reserva_id=r_id,
            peso_kg=p_kg,
            diagnostico_o_detalle=diag,
            tratamiento_o_indicaciones=trat,
            fecha_atencion=f_aten,
            atendido_por_id=at_id,
            atendido_por_nombre=at_nom,
            **kwargs,
        )
        self.id = id
        self.reserva_id = r_id
        self.reservaId = r_id
        self.peso_kg = p_kg
        self.pesoKg = p_kg
        self.diagnostico_o_detalle = diag
        self.diagnosticoODetalle = diag
        self.tratamiento_o_indicaciones = trat
        self.tratamientoOIndicaciones = trat
        self.fecha_atencion = f_aten
        self.fechaAtencion = f_aten
        self.atendido_por_id = at_id
        self.atendidoPorId = at_id
        self.atendido_por_nombre = at_nom
        self.atendidoPorNombre = at_nom

    def to_dict(self):
        return {
            "id": self.id,
            "reservaId": self.reserva_id,
            "pesoKg": self.peso_kg,
            "diagnosticoODetalle": self.diagnostico_o_detalle,
            "tratamientoOIndicaciones": self.tratamiento_o_indicaciones,
            "fechaAtencion": self.fecha_atencion,
            "atendidoPorId": self.atendido_por_id,
            "atendidoPorNombre": self.atendido_por_nombre,
        }

