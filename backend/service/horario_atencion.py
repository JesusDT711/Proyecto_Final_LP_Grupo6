
from datetime import datetime, time
from typing import Optional

class HorarioAtencion:

    def __init__(self, apertura: time = time(9, 0), cierre: time = time(21, 0)):
        self.apertura = apertura
        self.cierre = cierre

    def validar(self, inicio: datetime, fin: datetime) -> Optional[str]:
        if inicio.weekday() == 6:
            return "No atendemos los domingos. Atendemos de lunes a sábado"

        termina_otro_dia = fin.date() != inicio.date()
        empieza_antes_de_abrir = inicio.time() < self.apertura
        termina_despues_de_cerrar = fin.time() > self.cierre

        if termina_otro_dia or empieza_antes_de_abrir or termina_despues_de_cerrar:
            hora_apertura = self.apertura.strftime("%H:%M")
            hora_cierre = self.cierre.strftime("%H:%M")
            return (
                f"El horario de atención es de lunes a sábado de {hora_apertura} a {hora_cierre}, "
                f"y el servicio debe terminar antes del cierre"
            )

        return None

