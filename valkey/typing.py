# from __future__ import annotations

from datetime import datetime, timedelta
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Iterable,
    Literal,
    Mapping,
    Protocol,
    Type,
    TypedDict,
    TypeVar,
    Union,
)

if TYPE_CHECKING:
    from valkey._parsers import Encoder
    from valkey.asyncio.connection import ConnectionPool as AsyncConnectionPool
    from valkey.connection import ConnectionPool


class AsyncClientProtocol(Protocol):
    _is_async_client: Literal[True]


class SyncClientProtocol(Protocol):
    _is_async_client: Literal[False]


Number = int | float
EncodedT = bytes | memoryview
StringTypeT = str | bytes
DecodedT = str | int | float
EncodableT = EncodedT | DecodedT
AbsExpiryT = int | datetime
ACLGetUserData = (
    dict[str, bool | list[str] | list[list[str]] | list[dict[str, str]]] | None
)
ACLLogEntry = dict[str, str | float | dict[str, str | int]]
ACLLogData = list[ACLLogEntry]
InfoData = dict[str, str | int | float | dict[str, str | int]]
MemoryStatsData = dict[str, str | int | float | dict[StringTypeT, int | str | float]]
LCSMatchEntry = list[list[int] | int]
LCSIdxData = (
    list[StringTypeT | list[LCSMatchEntry] | int]
    | dict[StringTypeT, list[LCSMatchEntry] | int]
)
BlockingPopResult = list[StringTypeT] | tuple[StringTypeT, StringTypeT]
ExpiryT = int | timedelta
ZScoreBoundT = float | str  # str allows for the [ or ( prefix
BitfieldOffsetT = int | str  # str allows for #x syntax
_StringLikeT = bytes | str | memoryview
KeyT = _StringLikeT  # Main valkey key space
PatternT = _StringLikeT  # Patterns matched against keys, fields etc
FieldT = EncodableT  # Fields within hash tables, streams and geo commands
KeysT = KeyT | Iterable[KeyT]
ResponseT = Awaitable[Any] | Any
ChannelT = _StringLikeT
GroupT = _StringLikeT  # Consumer group
ConsumerT = _StringLikeT  # Consumer name
StreamIdT = int | _StringLikeT
ScriptTextT = _StringLikeT
StreamEntryT = tuple[StringTypeT, dict[StringTypeT, StringTypeT]]
StreamReadResp2T = list[tuple[StringTypeT, list[StreamEntryT]]]
StreamReadResp3T = dict[StringTypeT, list[list[StreamEntryT]]]
TimeoutSecT = int | float | _StringLikeT
ZSetScorePairsT = list[tuple[StringTypeT, float]] | list[list[StringTypeT | float]]
ZSetWithScoresRawT = list[StringTypeT] | list[list[StringTypeT | float]]
ZPopResultT = (
    list[tuple[StringTypeT, float]]
    | list[StringTypeT | float]
    | list[list[StringTypeT | float]]
)
BZPopResultT = tuple[StringTypeT, StringTypeT, float] | list[StringTypeT | float]
ZMPopResultT = list[StringTypeT | list[list[StringTypeT | float]]]


class XPendingConsumer(TypedDict):
    name: StringTypeT
    pending: int


class XPendingResult(TypedDict):
    pending: int
    min: StringTypeT
    max: StringTypeT
    consumers: list[XPendingConsumer]


class XPendingRangeEntry(TypedDict):
    message_id: StringTypeT
    consumer: StringTypeT
    time_since_delivered: int
    times_delivered: int


# Mapping is not covariant in the key type, which prevents
# Mapping[_StringLikeT, X] from accepting arguments of type Dict[str, X]. Using
# a TypeVar instead of a Union allows mappings with any of the permitted types
# to be passed. Care is needed if there is more than one such mapping in a
# type signature because they will all be required to be the same key type.
AnyKeyT = TypeVar("AnyKeyT", bytes, str, memoryview)
AnyFieldT = TypeVar("AnyFieldT", bytes, str, memoryview)
AnyChannelT = TypeVar("AnyChannelT", bytes, str, memoryview)
AnyStreamIdT = TypeVar("AnyStreamIdT", int, bytes, str, memoryview)
AnyEncodableT = TypeVar("AnyEncodableT", int, float, bytes, str, memoryview)

ExceptionMappingT = Mapping[str, Union[Type[Exception], Mapping[str, Type[Exception]]]]


class CommandsProtocol(Protocol):
    connection_pool: Union["AsyncConnectionPool", "ConnectionPool"]

    def execute_command(self, *args, **options) -> ResponseT: ...


class ClusterCommandsProtocol(CommandsProtocol, Protocol):
    encoder: "Encoder"

    def execute_command(self, *args, **options) -> Any | Awaitable[Any]: ...
