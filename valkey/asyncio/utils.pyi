from types import TracebackType
from typing import Any, Generic

from valkey.asyncio.client import Pipeline, Valkey
from valkey.client import _StrType

def from_url(url: str, **kwargs) -> Valkey[Any]: ...

class pipeline(Generic[_StrType]):
    p: Pipeline[_StrType]
    def __init__(self, valkey_obj: Valkey[_StrType]) -> None: ...
    async def __aenter__(self) -> Pipeline[_StrType]: ...
    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> None: ...
