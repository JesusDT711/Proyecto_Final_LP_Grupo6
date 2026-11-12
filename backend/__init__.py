"""
Paquete backend del sistema Veterinaria Huellitas.
Permite importar los módulos directamente (ej: from backend.model import Usuario).
"""

import os
import sys

# Agrega backend y su directorio contenedor a sys.path automáticamente
_backend_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_backend_dir)

for _ruta in [_backend_dir, _parent_dir]:
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)

from . import exception, model, repository, service, util

__all__ = ["model", "repository", "service", "exception", "util"]

