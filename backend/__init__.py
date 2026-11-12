
import os
import sys

_backend_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_backend_dir)

for _ruta in [_backend_dir, _parent_dir]:
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)

from . import config, controller, dto, exception, model, repository, security, service, util

__all__ = [
    "config",
    "model",
    "repository",
    "service",
    "dto",
    "controller",
    "security",
    "exception",
    "util",
]

