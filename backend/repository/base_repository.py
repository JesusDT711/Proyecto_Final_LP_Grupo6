"""
Repositorio base genérico para acceso a datos.
Soporta sesiones de SQLAlchemy con fallback en memoria para pruebas desacopladas.
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    Repositorio base que encapsula las operaciones comunes de persistencia.
    """

    def __init__(self, model_class: Type[T], session: Optional[Any] = None):
        self.model_class = model_class
        self.session = session
        # Almacenamiento en memoria como fallback para testing o ejecución sin BD activa
        self._memoria: Dict[int, T] = {}
        self._auto_id: int = 1

    def buscar_por_id(self, id: int) -> Optional[T]:
        if self.session is not None:
            return self.session.query(self.model_class).filter(self.model_class.id == id).first()
        return self._memoria.get(id)

    def listar_todos(self) -> List[T]:
        if self.session is not None:
            return self.session.query(self.model_class).all()
        return list(self._memoria.values())

    def guardar(self, entidad: T) -> T:
        if self.session is not None:
            self.session.add(entidad)
            self.session.commit()
            self.session.refresh(entidad)
            return entidad

        # Operación en memoria
        if getattr(entidad, "id", None) is None:
            setattr(entidad, "id", self._auto_id)
            self._auto_id += 1
        self._memoria[getattr(entidad, "id")] = entidad
        return entidad

    def eliminar(self, entidad: T) -> None:
        if self.session is not None:
            self.session.delete(entidad)
            self.session.commit()
            return

        entidad_id = getattr(entidad, "id", None)
        if entidad_id in self._memoria:
            del self._memoria[entidad_id]

