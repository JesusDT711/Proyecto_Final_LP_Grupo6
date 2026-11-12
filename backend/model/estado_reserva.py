
from enum import Enum


class EstadoReserva(str, Enum):

    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    ATENDIDA = "ATENDIDA"

    def __str__(self) -> str:
        return self.value

