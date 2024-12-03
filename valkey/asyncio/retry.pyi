from collections.abc import Awaitable, Callable, Iterable
from typing import TypeVar

from valkey.backoff import AbstractBackoff
from valkey.exceptions import ValkeyError

_T = TypeVar("_T")

class Retry:
    def __init__(self, backoff: AbstractBackoff, retries: int, supported_errors: tuple[type[ValkeyError], ...] = ...) -> None: ...
    def update_supported_errors(self, specified_errors: Iterable[type[ValkeyError]]) -> None: ...
    async def call_with_retry(self, do: Callable[[], Awaitable[_T]], fail: Callable[[ValkeyError], Awaitable[object]]) -> _T: ...
