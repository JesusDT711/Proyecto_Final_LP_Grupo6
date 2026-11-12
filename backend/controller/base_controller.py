
from typing import Any, Dict, Generic, Optional, TypeVar, Union

T = TypeVar("T")


class ApiResponse(Generic[T]):

    def __init__(self, data: T, status_code: int = 200, headers: Optional[Dict[str, str]] = None):
        self.data = data
        self.status_code = status_code
        self.headers = headers or {}

    def __iter__(self):
        yield self.data
        yield self.status_code

    def __repr__(self) -> str:
        return f"<ApiResponse(status_code={self.status_code}, data={self.data!r})>"

    @property
    def body(self) -> T:
        return self.data

    @classmethod
    def ok(cls, data: Any = None) -> "ApiResponse":
        return cls(data=data, status_code=200)

    @classmethod
    def created(cls, data: Any = None) -> "ApiResponse":
        return cls(data=data, status_code=201)

    @classmethod
    def no_content(cls) -> "ApiResponse":
        return cls(data=None, status_code=204)

