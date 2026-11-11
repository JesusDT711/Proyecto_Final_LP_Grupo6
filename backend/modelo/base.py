
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict

try:
    from sqlalchemy.orm import declarative_base, relationship
    from sqlalchemy import (
        Column,
        BigInteger,
        Integer,
        String,
        Numeric,
        DateTime,
        Date,
        Boolean,
        ForeignKey,
        Enum as SqlEnum,
        Index,
        func,
    )
    SQLALCHEMY_INSTALLED = True
    _DeclarativeBase = declarative_base()
except ImportError:
    # Capa de compatibilidad en caso de ejecutarse sin SQLAlchemy instalado previamente
    SQLALCHEMY_INSTALLED = False

    class _DeclarativeBase:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    def Column(*args, **kwargs):
        return None

    def relationship(*args, **kwargs):
        return None

    def BigInteger(*args, **kwargs):
        return None

    def Integer(*args, **kwargs):
        return None

    def String(*args, **kwargs):
        return None

    def Numeric(*args, **kwargs):
        return None

    def DateTime(*args, **kwargs):
        return None

    def Date(*args, **kwargs):
        return None

    def Boolean(*args, **kwargs):
        return None

    def ForeignKey(*args, **kwargs):
        return None

    def SqlEnum(*args, **kwargs):
        return None

    def Index(*args, **kwargs):
        return None

    class _FuncHelper:
        @staticmethod
        def now():
            return None

    func = _FuncHelper()


class Base(_DeclarativeBase):
    __abstract__ = True

    def __repr__(self) -> str:
        attrs = ", ".join(
            f"{k}={v!r}"
            for k, v in self.__dict__.items()
            if not k.startswith("_")
        )
        return f"<{self.__class__.__name__}({attrs})>"

    def to_dict(self) -> Dict[str, Any]:
   
        data: Dict[str, Any] = {}
        if hasattr(self, "__table__") and self.__table__ is not None:
            for column in self.__table__.columns:
                val = getattr(self, column.name, None)
                if isinstance(val, (datetime, date)):
                    data[column.name] = val.isoformat()
                elif isinstance(val, Decimal):
                    data[column.name] = float(val)
                elif hasattr(val, "value"):
                    data[column.name] = val.value
                else:
                    data[column.name] = val
        else:
            for k, v in self.__dict__.items():
                if not k.startswith("_"):
                    if isinstance(v, (datetime, date)):
                        data[k] = v.isoformat()
                    elif isinstance(v, Decimal):
                        data[k] = float(v)
                    elif hasattr(v, "value"):
                        data[k] = v.value
                    else:
                        data[k] = v
        return data


__all__ = [
    "Base",
    "Column",
    "BigInteger",
    "Integer",
    "String",
    "Numeric",
    "DateTime",
    "Date",
    "Boolean",
    "ForeignKey",
    "SqlEnum",
    "Index",
    "func",
    "relationship",
    "SQLALCHEMY_INSTALLED",
]

