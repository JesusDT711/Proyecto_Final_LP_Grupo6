
from typing import Any, Dict

try:
    from pydantic import BaseModel, ConfigDict
    PYDANTIC_AVAILABLE = True

    class BaseDto(BaseModel):
        model_config = ConfigDict(
            populate_by_name=True,
            from_attributes=True,
            extra="ignore",
        )

        def to_dict(self) -> Dict[str, Any]:
            return self.model_dump(by_alias=True)

except ImportError:
    PYDANTIC_AVAILABLE = False

    class BaseDto:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

        def to_dict(self) -> Dict[str, Any]:
            data = {}
            for k, v in self.__dict__.items():
                if not k.startswith("_"):
                    data[k] = v
            return data

        def __repr__(self) -> str:
            attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items() if not k.startswith("_"))
            return f"<{self.__class__.__name__}({attrs})>"

