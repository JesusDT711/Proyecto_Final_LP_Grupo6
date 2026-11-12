"""
Utilidades para normalización y tratamiento de correos electrónicos.
Equivalente a EmailUtil.java del proyecto modelo de referencia.
"""

from typing import Optional


class EmailUtil:
    """
    Tratamiento uniforme de correos electrónicos en el sistema:
    sin espacios en los extremos y siempre en minúsculas.
    Garantiza que 'Usuario@Mail.com ' y 'usuario@mail.com' correspondan a la misma cuenta.
    """

    @staticmethod
    def normalizar(email: Optional[str]) -> Optional[str]:
        if email is None:
            return None
        return email.strip().lower()

