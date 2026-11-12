
class ApiException(Exception):

    def __init__(self, status_code: int, mensaje: str):
        super().__init__(mensaje)
        self.status_code = status_code
        self.mensaje = mensaje

    def to_dict(self) -> dict:
        return {
            "mensaje": self.mensaje,
            "status": self.status_code,
        }

    def __repr__(self) -> str:
        return f"<ApiException(status_code={self.status_code}, mensaje='{self.mensaje}')>"

