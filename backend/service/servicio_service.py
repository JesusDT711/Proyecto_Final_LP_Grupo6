
from decimal import Decimal
from typing import Any, Dict, List, Optional, Union
try:
    from exception.api_exception import ApiException
    from model.servicio import Servicio
    from repository.servicio_repository import ServicioRepository
except ImportError:
    from backend.exception.api_exception import ApiException
    from backend.model.servicio import Servicio
    from backend.repository.servicio_repository import ServicioRepository


class ServicioService:

    def __init__(self, servicio_repository: ServicioRepository):
        self.servicio_repository = servicio_repository

    def listar_activos(self) -> List[Dict[str, Any]]:   
        return [s.to_dict() for s in self.servicio_repository.listar_activos()]

    def listar_todos(self) -> List[Dict[str, Any]]:
        return [s.to_dict() for s in self.servicio_repository.listar_todos()]

    def obtener(self, id: int) -> Dict[str, Any]:
        servicio = self._buscar_por_id(id)
        return servicio.to_dict()

    def buscar(self, nombre: str) -> List[Dict[str, Any]]:
        return [s.to_dict() for s in self.servicio_repository.buscar_por_nombre(nombre)]

    def crear(
        self,
        nombre: str,
        precio: Union[Decimal, float, str],
        duracion_minutos: int,
        descripcion: Optional[str] = None,
        activo: bool = True,
    ) -> Dict[str, Any]:
        if not nombre or not nombre.strip():
            raise ApiException(400, "El nombre del servicio es obligatorio")

        nombre_clean = nombre.strip()
        if self.servicio_repository.existe_por_nombre_ignore_case(nombre_clean):
            raise ApiException(409, "Ya existe un servicio con ese nombre")

        try:
            precio_dec = Decimal(str(precio))
            if precio_dec <= 0:
                raise ValueError()
        except Exception:
            raise ApiException(400, "El precio debe ser un número mayor a 0")

        if not duracion_minutos or duracion_minutos < 5 or duracion_minutos > 480:
            raise ApiException(400, "La duración debe estar entre 5 y 480 minutos")

        servicio = Servicio(
            nombre=nombre_clean,
            descripcion=descripcion.strip() if descripcion else None,
            precio=precio_dec,
            duracion_minutos=duracion_minutos,
            activo=activo,
        )
        guardado = self.servicio_repository.guardar(servicio)
        return guardado.to_dict()

    def actualizar(
        self,
        id: int,
        nombre: str,
        precio: Union[Decimal, float, str],
        duracion_minutos: int,
        descripcion: Optional[str] = None,
        activo: Optional[bool] = None,
    ) -> Dict[str, Any]:
        servicio = self._buscar_por_id(id)

        if not nombre or not nombre.strip():
            raise ApiException(400, "El nombre del servicio es obligatorio")

        nombre_clean = nombre.strip()
        if self.servicio_repository.existe_por_nombre_ignore_case_y_distinto_id(nombre_clean, id):
            raise ApiException(409, "Ya existe otro servicio con ese nombre")

        try:
            precio_dec = Decimal(str(precio))
            if precio_dec <= 0:
                raise ValueError()
        except Exception:
            raise ApiException(400, "El precio debe ser un número mayor a 0")

        if not duracion_minutos or duracion_minutos < 5 or duracion_minutos > 480:
            raise ApiException(400, "La duración debe estar entre 5 y 480 minutos")

        servicio.nombre = nombre_clean
        servicio.descripcion = descripcion.strip() if descripcion else None
        servicio.precio = precio_dec
        servicio.duracion_minutos = duracion_minutos
        if activo is not None:
            servicio.activo = activo

        guardado = self.servicio_repository.guardar(servicio)
        return guardado.to_dict()

    def desactivar(self, id: int) -> Dict[str, str]:
        servicio = self._buscar_por_id(id)
        servicio.activo = False
        self.servicio_repository.guardar(servicio)
        return {"mensaje": "Servicio desactivado correctamente"}

    def _buscar_por_id(self, id: int) -> Servicio:
        servicio = self.servicio_repository.buscar_por_id(id)
        if servicio is None:
            raise ApiException(404, "El servicio no existe")
        return servicio
