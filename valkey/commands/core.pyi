from datetime import datetime
from collections.abc import AsyncIterator

from typing import (
    Any,
    Awaitable,
    Callable,
    Generic,
    Iterable,
    Iterator,
    Literal,
    Mapping,
    NoReturn,
    Sequence,
    TypeVar,
    overload,
)

from _typeshed import Incomplete

from valkey.asyncio.client import Valkey as AsyncValkey
from valkey.client import Valkey
from valkey.typing import (
    AbsExpiryT,
    AnyEncodableT,
    AnyFieldT,
    AnyKeyT,
    AnyStreamIdT,
    BitfieldOffsetT,
    ChannelT,
    CommandsProtocol,
    ConsumerT,
    EncodableT,
    ExpiryT,
    FieldT,
    GroupT,
    KeysT,
    KeyT,
    PatternT,
    ResponseT,
    ScriptTextT,
    StreamIdT,
    TimeoutSecT,
    ZScoreBoundT,
)

_ScoreCastFuncReturn = TypeVar("_ScoreCastFuncReturn")
_StrType = TypeVar("_StrType", bound=str | bytes)

_StreamEntryT = tuple[_StrType, dict[_StrType, _StrType]]
_StreamReadResp2T = list[tuple[_StrType, list[_StreamEntryT]]]
_StreamReadResp3T = dict[_StrType, list[list[_StreamEntryT]]]
_ZSetScorePairT = tuple[_StrType, float] | list[_StrType | float]
_GeoSearchEntryT = list[_StrType | float | int | tuple[float, float]]
_GeoSearchReplyT = list[_StrType] | list[_GeoSearchEntryT]

# Internal helper aliases used by legacy signatures in this stub.
_CommandOptions = Any
_Key = KeyT
_Value = EncodableT

class ACLCommands(CommandsProtocol, Generic[_StrType]):
    def acl_cat(self, category: str | None = None, **kwargs) -> list[_StrType]: ...
    def acl_deluser(self, *username: str, **kwargs) -> int: ...
    def acl_dryrun(self, username, *args, **kwargs) -> _StrType: ...
    def acl_genpass(self, bits: int | None = None, **kwargs) -> _StrType: ...
    def acl_getuser(self, username: str, **kwargs) -> dict[str, Any] | None: ...
    def acl_help(self, **kwargs) -> list[_StrType]: ...
    def acl_list(self, **kwargs) -> list[_StrType]: ...
    def acl_log(
        self, count: int | None = None, **kwargs
    ) -> list[dict[str, Any]] | None: ...
    def acl_log_reset(self, **kwargs) -> Literal[True]: ...
    def acl_load(self, **kwargs) -> Literal[True]: ...
    def acl_save(self, **kwargs) -> Literal[True]: ...
    def acl_setuser(
        self,
        username: str,
        enabled: bool = False,
        nopass: bool = False,
        passwords: str | Iterable[str] | None = None,
        hashed_passwords: str | Iterable[str] | None = None,
        categories: Iterable[str] | None = None,
        commands: Iterable[str] | None = None,
        keys: Iterable[KeyT] | None = None,
        channels: Iterable[ChannelT] | None = None,
        selectors: Iterable[tuple[str, KeyT]] | None = None,
        reset: bool = False,
        reset_keys: bool = False,
        reset_channels: bool = False,
        reset_passwords: bool = False,
        **kwargs,
    ) -> Literal[True]: ...
    def acl_users(self, **kwargs) -> list[_StrType]: ...
    def acl_whoami(self, **kwargs) -> _StrType: ...

class AsyncACLCommands(CommandsProtocol, Generic[_StrType]):
    async def acl_cat(
        self, category: str | None = None, **kwargs
    ) -> list[_StrType]: ...
    async def acl_deluser(self, *username: str, **kwargs) -> int: ...
    async def acl_dryrun(self, username, *args, **kwargs) -> _StrType: ...
    async def acl_genpass(self, bits: int | None = None, **kwargs) -> _StrType: ...
    async def acl_getuser(self, username: str, **kwargs) -> dict[str, Any] | None: ...
    async def acl_help(self, **kwargs) -> list[_StrType]: ...
    async def acl_list(self, **kwargs) -> list[_StrType]: ...
    async def acl_log(
        self, count: int | None = None, **kwargs
    ) -> list[dict[str, Any]] | None: ...
    async def acl_log_reset(self, **kwargs) -> Literal[True]: ...
    async def acl_load(self, **kwargs) -> Literal[True]: ...
    async def acl_save(self, **kwargs) -> Literal[True]: ...
    async def acl_setuser(
        self,
        username: str,
        enabled: bool = False,
        nopass: bool = False,
        passwords: str | Iterable[str] | None = None,
        hashed_passwords: str | Iterable[str] | None = None,
        categories: Iterable[str] | None = None,
        commands: Iterable[str] | None = None,
        keys: Iterable[KeyT] | None = None,
        channels: Iterable[ChannelT] | None = None,
        selectors: Iterable[tuple[str, KeyT]] | None = None,
        reset: bool = False,
        reset_keys: bool = False,
        reset_channels: bool = False,
        reset_passwords: bool = False,
        **kwargs,
    ) -> Literal[True]: ...
    async def acl_users(self, **kwargs) -> list[_StrType]: ...
    async def acl_whoami(self, **kwargs) -> _StrType: ...

class ManagementCommands(CommandsProtocol, Generic[_StrType]):
    def auth(self, password: str, username: str | None = None, **kwargs) -> bool: ...
    def bgrewriteaof(self, **kwargs) -> Literal[True]: ...
    def bgsave(self, schedule: bool = True, **kwargs) -> Literal[True]: ...
    def role(self) -> list[Any]: ...
    def client_kill(self, address: str, **kwargs) -> int | bool: ...
    def client_kill_filter(
        self,
        _id: str | None = None,
        _type: str | None = None,
        addr: str | None = None,
        skipme: bool | None = None,
        laddr: bool | None = None,
        user: str | None = None,
        maxage: int | None = None,
        **kwargs,
    ) -> int | bool: ...
    def client_info(self, **kwargs) -> dict[str, str | int]: ...
    def client_list(
        self, _type: str | None = None, client_id: list[EncodableT] = [], **kwargs
    ) -> list[dict[str, str]]: ...
    def client_getname(self, **kwargs) -> _StrType | None: ...
    def client_getredir(self, **kwargs) -> int: ...
    def client_reply(
        self, reply: Literal["ON"] | Literal["OFF"] | Literal["SKIP"], **kwargs
    ): ...
    def client_id(self, **kwargs) -> int: ...
    def client_tracking_on(
        self,
        clientid: int | None = None,
        prefix: Sequence[KeyT] = [],
        bcast: bool = False,
        optin: bool = False,
        optout: bool = False,
        noloop: bool = False,
    ): ...
    def client_tracking_off(
        self,
        clientid: int | None = None,
        prefix: Sequence[KeyT] = [],
        bcast: bool = False,
        optin: bool = False,
        optout: bool = False,
        noloop: bool = False,
    ): ...
    def client_tracking(
        self,
        on: bool = True,
        clientid: int | None = None,
        prefix: Sequence[KeyT] = [],
        bcast: bool = False,
        optin: bool = False,
        optout: bool = False,
        noloop: bool = False,
        **kwargs,
    ): ...
    def client_trackinginfo(self, **kwargs) -> list[Any] | dict[_StrType, Any]: ...
    def client_setname(self, name: str, **kwargs) -> Literal[True]: ...
    def client_setinfo(self, attr: str, value: str, **kwargs) -> Literal[True]: ...
    def client_unblock(self, client_id: int, error: bool = False, **kwargs) -> bool: ...
    def client_pause(
        self, timeout: int, all: bool = True, **kwargs
    ) -> Literal[True]: ...
    def client_unpause(self, **kwargs) -> _StrType: ...
    def client_no_evict(self, mode: str) -> str: ...
    def client_no_touch(self, mode: str) -> str: ...
    def command(self, **kwargs) -> dict[str, dict[str, Any]]: ...
    def command_info(self, **kwargs) -> NoReturn: ...
    def command_count(self, **kwargs) -> int: ...
    def command_list(
        self,
        module: str | None = None,
        category: str | None = None,
        pattern: str | None = None,
    ) -> list[bytes]: ...
    def command_getkeysandflags(self, *args: list[str]) -> list[str | list[str]]: ...
    def command_docs(self, *args) -> None: ...
    def config_get(
        self, pattern: PatternT = "*", *args: list[PatternT], **kwargs
    ) -> dict[str, str]: ...
    def config_set(
        self, name: KeyT, value: EncodableT, *args: list[KeyT | EncodableT], **kwargs
    ) -> Literal[True]: ...
    def config_resetstat(self, **kwargs) -> Literal[True]: ...
    def config_rewrite(self, **kwargs) -> _StrType: ...
    def dbsize(self, **kwargs) -> int: ...
    def debug_object(self, key: KeyT, **kwargs) -> dict[str, str | int]: ...
    def debug_segfault(self, **kwargs) -> None: ...
    def echo(self, value: EncodableT, **kwargs) -> _StrType: ...
    def flushall(self, asynchronous: bool = False, **kwargs) -> Literal[True]: ...
    def flushdb(self, asynchronous: bool = False, **kwargs) -> Literal[True]: ...
    def sync(self): ...
    def psync(self, replicationid: str, offset: int): ...
    def swapdb(self, first: int, second: int, **kwargs) -> Literal[True]: ...
    def select(self, index: int, **kwargs) -> Literal[True]: ...
    def info(
        self, section: str | None = None, *args: list[str], **kwargs
    ) -> dict[str, Any]: ...
    def lastsave(self, **kwargs) -> datetime | None: ...
    def latency_doctor(self) -> None: ...
    def latency_graph(self) -> None: ...
    def lolwut(self, *version_numbers: str | float, **kwargs) -> bytes: ...
    def reset(self) -> _StrType: ...
    def migrate(
        self,
        host: str,
        port: int,
        keys: KeysT,
        destination_db: int,
        timeout: int,
        copy: bool = False,
        replace: bool = False,
        auth: str | None = None,
        **kwargs,
    ): ...
    def object(self, infotype: str, key: KeyT, **kwargs): ...
    def memory_doctor(self, **kwargs) -> None: ...
    def memory_help(self, **kwargs) -> None: ...
    def memory_stats(self, **kwargs) -> dict[str, Any]: ...
    # TODO: parse the output of memory_malloc_stats at least to a str
    def memory_malloc_stats(self, **kwargs) -> bytes: ...
    def memory_usage(
        self, key: KeyT, samples: int | None = None, **kwargs
    ) -> int | None: ...
    def memory_purge(self, **kwargs) -> Literal[True]: ...
    def latency_histogram(self, *args) -> None: ...
    def latency_history(self, event: str): ...
    def latency_latest(self): ...
    def latency_reset(self, *events: str): ...
    def ping(self, **kwargs) -> bool: ...
    def quit(self, **kwargs) -> Literal[True]: ...
    def replicaof(self, *args, **kwargs): ...
    def save(self, **kwargs) -> Literal[True]: ...
    def shutdown(
        self,
        save: bool = False,
        nosave: bool = False,
        now: bool = False,
        force: bool = False,
        abort: bool = False,
        **kwargs,
    ) -> None: ...
    def slaveof(self, host: str | None = None, port: int | None = None, **kwargs): ...
    def slowlog_get(self, num: int | None = None, **kwargs) -> list[dict[str, Any]]: ...
    def slowlog_len(self, **kwargs) -> int: ...
    def slowlog_reset(self, **kwargs) -> Literal[True]: ...
    def time(self, **kwargs) -> tuple[int, int]: ...
    def wait(self, num_replicas: int, timeout: int, **kwargs) -> int: ...
    def waitaof(self, num_local: int, num_replicas: int, timeout: int, **kwargs): ...
    def hello(self) -> None: ...
    def failover(self) -> None: ...

class AsyncManagementCommands(CommandsProtocol, Generic[_StrType]):
    async def auth(
        self, password: str, username: str | None = None, **kwargs
    ) -> bool: ...
    async def bgrewriteaof(self, **kwargs) -> Literal[True]: ...
    async def bgsave(self, schedule: bool = True, **kwargs) -> Literal[True]: ...
    async def role(self) -> list[Any]: ...
    async def client_kill(self, address: str, **kwargs) -> int | bool: ...
    async def client_kill_filter(
        self,
        _id: str | None = None,
        _type: str | None = None,
        addr: str | None = None,
        skipme: bool | None = None,
        laddr: bool | None = None,
        user: str | None = None,
        maxage: int | None = None,
        **kwargs,
    ) -> int | bool: ...
    async def client_info(self, **kwargs) -> dict[str, str | int]: ...
    async def client_list(
        self, _type: str | None = None, client_id: list[EncodableT] = [], **kwargs
    ) -> list[dict[str, str]]: ...
    async def client_getname(self, **kwargs) -> _StrType | None: ...
    async def client_getredir(self, **kwargs) -> int: ...
    async def client_reply(
        self, reply: Literal["ON"] | Literal["OFF"] | Literal["SKIP"], **kwargs
    ): ...
    async def client_id(self, **kwargs) -> int: ...
    async def client_tracking_on(
        self,
        clientid: int | None = None,
        prefix: Sequence[KeyT] = [],
        bcast: bool = False,
        optin: bool = False,
        optout: bool = False,
        noloop: bool = False,
    ): ...
    async def client_tracking_off(
        self,
        clientid: int | None = None,
        prefix: Sequence[KeyT] = [],
        bcast: bool = False,
        optin: bool = False,
        optout: bool = False,
        noloop: bool = False,
    ): ...
    async def client_tracking(
        self,
        on: bool = True,
        clientid: int | None = None,
        prefix: Sequence[KeyT] = [],
        bcast: bool = False,
        optin: bool = False,
        optout: bool = False,
        noloop: bool = False,
        **kwargs,
    ): ...
    async def client_trackinginfo(
        self, **kwargs
    ) -> list[Any] | dict[_StrType, Any]: ...
    async def client_setname(self, name: str, **kwargs) -> Literal[True]: ...
    async def client_setinfo(
        self, attr: str, value: str, **kwargs
    ) -> Literal[True]: ...
    async def client_unblock(
        self, client_id: int, error: bool = False, **kwargs
    ) -> bool: ...
    async def client_pause(
        self, timeout: int, all: bool = True, **kwargs
    ) -> Literal[True]: ...
    async def client_unpause(self, **kwargs) -> _StrType: ...
    async def client_no_evict(self, mode: str) -> str: ...
    async def client_no_touch(self, mode: str) -> str: ...
    async def command(self, **kwargs) -> dict[str, dict[str, Any]]: ...
    async def command_info(self, **kwargs) -> NoReturn: ...
    async def command_count(self, **kwargs) -> int: ...
    async def command_list(
        self,
        module: str | None = None,
        category: str | None = None,
        pattern: str | None = None,
    ) -> list[bytes]: ...
    async def command_getkeysandflags(
        self, *args: list[str]
    ) -> list[str | list[str]]: ...
    async def command_docs(self, *args) -> None: ...
    async def config_get(
        self, pattern: PatternT = "*", *args: list[PatternT], **kwargs
    ) -> dict[str, str]: ...
    async def config_set(
        self, name: KeyT, value: EncodableT, *args: list[KeyT | EncodableT], **kwargs
    ) -> Literal[True]: ...
    async def config_resetstat(self, **kwargs) -> Literal[True]: ...
    async def config_rewrite(self, **kwargs) -> _StrType: ...
    async def dbsize(self, **kwargs) -> int: ...
    async def debug_object(self, key: KeyT, **kwargs) -> dict[str, str | int]: ...
    async def debug_segfault(self, **kwargs) -> None: ...
    async def echo(self, value: EncodableT, **kwargs) -> _StrType: ...
    async def flushall(self, asynchronous: bool = False, **kwargs) -> Literal[True]: ...
    async def flushdb(self, asynchronous: bool = False, **kwargs) -> Literal[True]: ...
    async def sync(self): ...
    async def psync(self, replicationid: str, offset: int): ...
    async def swapdb(self, first: int, second: int, **kwargs) -> Literal[True]: ...
    async def select(self, index: int, **kwargs) -> Literal[True]: ...
    async def info(
        self, section: str | None = None, *args: list[str], **kwargs
    ) -> dict[str, Any]: ...
    async def lastsave(self, **kwargs) -> datetime | None: ...
    async def latency_doctor(self) -> None: ...
    async def latency_graph(self) -> None: ...
    async def lolwut(self, *version_numbers: str | float, **kwargs) -> bytes: ...
    async def reset(self) -> _StrType: ...
    async def migrate(
        self,
        host: str,
        port: int,
        keys: KeysT,
        destination_db: int,
        timeout: int,
        copy: bool = False,
        replace: bool = False,
        auth: str | None = None,
        **kwargs,
    ): ...
    async def object(self, infotype: str, key: KeyT, **kwargs): ...
    async def memory_doctor(self, **kwargs) -> None: ...
    async def memory_help(self, **kwargs) -> None: ...
    async def memory_stats(self, **kwargs) -> dict[str, Any]: ...
    # TODO: parse the output of memory_malloc_stats at least to a str
    async def memory_malloc_stats(self, **kwargs) -> bytes: ...
    async def memory_usage(
        self, key: KeyT, samples: int | None = None, **kwargs
    ) -> int | None: ...
    async def memory_purge(self, **kwargs) -> Literal[True]: ...
    async def latency_histogram(self, *args) -> None: ...
    async def latency_history(self, event: str): ...
    async def latency_latest(self): ...
    async def latency_reset(self, *events: str): ...
    async def ping(self, **kwargs) -> bool: ...
    async def quit(self, **kwargs) -> Literal[True]: ...
    async def replicaof(self, *args, **kwargs): ...
    async def save(self, **kwargs) -> Literal[True]: ...
    async def shutdown(
        self,
        save: bool = False,
        nosave: bool = False,
        now: bool = False,
        force: bool = False,
        abort: bool = False,
        **kwargs,
    ) -> None: ...
    async def slaveof(
        self, host: str | None = None, port: int | None = None, **kwargs
    ): ...
    async def slowlog_get(
        self, num: int | None = None, **kwargs
    ) -> list[dict[str, Any]]: ...
    async def slowlog_len(self, **kwargs) -> int: ...
    async def slowlog_reset(self, **kwargs) -> Literal[True]: ...
    async def time(self, **kwargs) -> tuple[int, int]: ...
    async def wait(self, num_replicas: int, timeout: int, **kwargs) -> int: ...
    async def waitaof(
        self, num_local: int, num_replicas: int, timeout: int, **kwargs
    ): ...
    async def hello(self) -> None: ...
    async def failover(self) -> None: ...

class BitFieldOperation:
    client: Incomplete
    key: Incomplete
    operations: list[tuple[EncodableT, ...]]
    def __init__(
        self,
        client: Valkey,
        key: KeyT,
        default_overflow: str | None = None,
    ) -> None: ...
    def reset(self) -> None: ...
    def overflow(self, overflow: str) -> BitFieldOperation: ...
    def incrby(
        self,
        fmt: str,
        offset: BitfieldOffsetT,
        increment: int,
        overflow: str | None = None,
    ) -> BitFieldOperation: ...
    def get(self, fmt: str, offset: BitfieldOffsetT) -> BitFieldOperation: ...
    def set(
        self, fmt: str, offset: BitfieldOffsetT, value: int
    ) -> BitFieldOperation: ...
    @property
    def command(self) -> list[EncodableT]: ...
    def execute(self) -> list[int | None]: ...

class AsyncBitFieldOperation:
    client: Incomplete
    key: Incomplete
    operations: list[tuple[EncodableT, ...]]
    def __init__(
        self,
        client: AsyncValkey,
        key: KeyT,
        default_overflow: str | None = None,
    ) -> None: ...
    def reset(self) -> None: ...
    def overflow(self, overflow: str) -> AsyncBitFieldOperation: ...
    def incrby(
        self,
        fmt: str,
        offset: BitfieldOffsetT,
        increment: int,
        overflow: str | None = None,
    ) -> AsyncBitFieldOperation: ...
    def get(self, fmt: str, offset: BitfieldOffsetT) -> AsyncBitFieldOperation: ...
    def set(
        self, fmt: str, offset: BitfieldOffsetT, value: int
    ) -> AsyncBitFieldOperation: ...
    @property
    def command(self) -> list[EncodableT]: ...
    async def execute(self) -> list[int | None]: ...

class BasicKeyCommands(CommandsProtocol, Generic[_StrType]):
    def append(self, key: KeyT, value: EncodableT) -> int: ...
    def bitcount(
        self,
        key: KeyT,
        start: int | None = None,
        end: int | None = None,
        mode: str | None = None,
    ) -> int: ...
    def bitfield(
        self, key: KeyT, default_overflow: str | None = None
    ) -> BitFieldOperation: ...
    def bitfield_ro(
        self,
        key: KeyT,
        encoding: str,
        offset: BitfieldOffsetT,
        items: list[tuple[str, BitfieldOffsetT]] | None = None,
    ) -> list[int]: ...
    def bitop(self, operation: str, dest: KeyT, *keys: KeyT) -> int: ...
    def bitpos(
        self,
        key: KeyT,
        bit: int,
        start: int | None = None,
        end: int | None = None,
        mode: str | None = None,
    ) -> int: ...
    def copy(
        self,
        source: KeyT,
        destination: KeyT,
        destination_db: int | str | None = None,
        replace: bool = False,
    ) -> bool: ...
    def decr(self, name: KeyT, amount: int = 1) -> int: ...
    def decrby(self, name: KeyT, amount: int = 1) -> int: ...
    def delete(self, *names: KeyT) -> int: ...
    def __delitem__(self, name: KeyT) -> None: ...
    def dump(self, name: KeyT) -> _StrType | None: ...
    def exists(self, *names: KeyT) -> int: ...
    __contains__ = exists
    def expire(
        self,
        name: KeyT,
        time: ExpiryT,
        nx: bool = False,
        xx: bool = False,
        gt: bool = False,
        lt: bool = False,
    ) -> bool: ...
    def expireat(
        self,
        name: KeyT,
        when: AbsExpiryT,
        nx: bool = False,
        xx: bool = False,
        gt: bool = False,
        lt: bool = False,
    ) -> bool: ...
    def expiretime(self, key: KeyT) -> int: ...
    def get(self, name: KeyT) -> _StrType | None: ...
    def getdel(self, name: KeyT) -> _StrType | None: ...
    def getex(
        self,
        name: KeyT,
        ex: ExpiryT | None = None,
        px: ExpiryT | None = None,
        exat: AbsExpiryT | None = None,
        pxat: AbsExpiryT | None = None,
        persist: bool = False,
    ) -> _StrType | None: ...
    def __getitem__(self, name: KeyT) -> _StrType: ...
    def getbit(self, name: KeyT, offset: int) -> int: ...
    def getrange(self, key: KeyT, start: int, end: int) -> _StrType: ...
    def getset(self, name: KeyT, value: EncodableT) -> _StrType | None: ...
    def incr(self, name: KeyT, amount: int = 1) -> int: ...
    def incrby(self, name: KeyT, amount: int = 1) -> int: ...
    def incrbyfloat(self, name: KeyT, amount: float = 1.0) -> float: ...
    def keys(self, pattern: PatternT = "*", **kwargs) -> list[_StrType]: ...
    def lmove(
        self,
        first_list: KeyT,
        second_list: KeyT,
        src: str = "LEFT",
        dest: str = "RIGHT",
    ) -> _StrType | None: ...
    def blmove(
        self,
        first_list: KeyT,
        second_list: KeyT,
        timeout: int,
        src: str = "LEFT",
        dest: str = "RIGHT",
    ) -> _StrType | None: ...
    def mget(self, keys: KeysT, *args: EncodableT) -> list[_StrType | None]: ...
    def mset(self, mapping: Mapping[AnyKeyT, EncodableT]) -> Literal[True]: ...
    def msetnx(self, mapping: Mapping[AnyKeyT, EncodableT]) -> bool: ...
    def move(self, name: KeyT, db: str | int) -> bool: ...
    def persist(self, name: KeyT) -> bool: ...
    def pexpire(
        self,
        name: KeyT,
        time: ExpiryT,
        nx: bool = False,
        xx: bool = False,
        gt: bool = False,
        lt: bool = False,
    ) -> bool: ...
    def pexpireat(
        self,
        name: KeyT,
        when: AbsExpiryT,
        nx: bool = False,
        xx: bool = False,
        gt: bool = False,
        lt: bool = False,
    ) -> bool: ...
    def pexpiretime(self, key: KeyT) -> int: ...
    def psetex(
        self, name: KeyT, time_ms: ExpiryT, value: EncodableT
    ) -> Literal[True]: ...
    def pttl(self, name: KeyT) -> int: ...
    @overload
    def hrandfield(
        self, key: KeyT, count: None = None, withvalues: Literal[False] = False
    ) -> _StrType | None: ...
    @overload
    def hrandfield(
        self, key: KeyT, count: int, withvalues: bool = False
    ) -> list[_StrType]: ...
    def randomkey(self, **kwargs) -> _StrType | None: ...
    def rename(self, src: KeyT, dst: KeyT) -> Literal[True]: ...
    def renamenx(self, src: KeyT, dst: KeyT) -> bool: ...
    def restore(
        self,
        name: KeyT,
        ttl: float,
        value: EncodableT,
        replace: bool = False,
        absttl: bool = False,
        idletime: int | None = None,
        frequency: int | None = None,
    ) -> _StrType: ...
    def set(
        self,
        name: KeyT,
        value: EncodableT,
        ex: ExpiryT | None = None,
        px: ExpiryT | None = None,
        nx: bool = False,
        xx: bool = False,
        keepttl: bool = False,
        get: bool = False,
        exat: AbsExpiryT | None = None,
        pxat: AbsExpiryT | None = None,
    ) -> bool | _StrType | None: ...
    def __setitem__(self, name: KeyT, value: EncodableT) -> None: ...
    def setbit(self, name: KeyT, offset: int, value: int) -> int: ...
    def setex(self, name: KeyT, time: ExpiryT, value: EncodableT) -> Literal[True]: ...
    def setnx(self, name: KeyT, value: EncodableT) -> bool: ...
    def setrange(self, name: KeyT, offset: int, value: EncodableT) -> int: ...
    def stralgo(
        self,
        algo: Literal["LCS"],
        value1: KeyT,
        value2: KeyT,
        specific_argument: Literal["strings"] | Literal["keys"] = "strings",
        len: bool = False,
        idx: bool = False,
        minmatchlen: int | None = None,
        withmatchlen: bool = False,
        **kwargs,
    ) -> str | dict[str, Any]: ...
    def strlen(self, name: KeyT) -> int: ...
    def substr(self, name: KeyT, start: int, end: int = -1) -> _StrType: ...
    def touch(self, *args: KeyT) -> int: ...
    def ttl(self, name: KeyT) -> int: ...
    def type(self, name: KeyT) -> _StrType: ...
    def watch(self, *names: KeyT) -> None: ...
    def unwatch(self) -> None: ...
    def unlink(self, *names: KeyT) -> int: ...
    def lcs(
        self,
        key1: str,
        key2: str,
        len: bool | None = False,
        idx: bool | None = False,
        minmatchlen: int | None = 0,
        withmatchlen: bool | None = False,
    ) -> str | int | list: ...

class AsyncBasicKeyCommands(CommandsProtocol, Generic[_StrType]):
    async def append(self, key: KeyT, value: EncodableT) -> int: ...
    async def bitcount(
        self,
        key: KeyT,
        start: int | None = None,
        end: int | None = None,
        mode: str | None = None,
    ) -> int: ...
    async def bitfield(
        self, key: KeyT, default_overflow: str | None = None
    ) -> AsyncBitFieldOperation: ...
    async def bitfield_ro(
        self,
        key: KeyT,
        encoding: str,
        offset: BitfieldOffsetT,
        items: list[tuple[str, BitfieldOffsetT]] | None = None,
    ) -> list[int]: ...
    async def bitop(self, operation: str, dest: KeyT, *keys: KeyT) -> int: ...
    async def bitpos(
        self,
        key: KeyT,
        bit: int,
        start: int | None = None,
        end: int | None = None,
        mode: str | None = None,
    ) -> int: ...
    async def copy(
        self,
        source: KeyT,
        destination: KeyT,
        destination_db: int | str | None = None,
        replace: bool = False,
    ) -> bool: ...
    async def decr(self, name: KeyT, amount: int = 1) -> int: ...
    async def decrby(self, name: KeyT, amount: int = 1) -> int: ...
    async def delete(self, *names: KeyT) -> int: ...
    async def __delitem__(self, name: KeyT) -> None: ...
    async def dump(self, name: KeyT) -> _StrType | None: ...
    async def exists(self, *names: KeyT) -> int: ...
    __contains__ = exists
    async def expire(
        self,
        name: KeyT,
        time: ExpiryT,
        nx: bool = False,
        xx: bool = False,
        gt: bool = False,
        lt: bool = False,
    ) -> bool: ...
    async def expireat(
        self,
        name: KeyT,
        when: AbsExpiryT,
        nx: bool = False,
        xx: bool = False,
        gt: bool = False,
        lt: bool = False,
    ) -> bool: ...
    async def expiretime(self, key: KeyT) -> int: ...
    async def get(self, name: KeyT) -> _StrType | None: ...
    async def getdel(self, name: KeyT) -> _StrType | None: ...
    async def getex(
        self,
        name: KeyT,
        ex: ExpiryT | None = None,
        px: ExpiryT | None = None,
        exat: AbsExpiryT | None = None,
        pxat: AbsExpiryT | None = None,
        persist: bool = False,
    ) -> _StrType | None: ...
    async def __getitem__(self, name: KeyT) -> _StrType: ...
    async def getbit(self, name: KeyT, offset: int) -> int: ...
    async def getrange(self, key: KeyT, start: int, end: int) -> _StrType: ...
    async def getset(self, name: KeyT, value: EncodableT) -> _StrType | None: ...
    async def incr(self, name: KeyT, amount: int = 1) -> int: ...
    async def incrby(self, name: KeyT, amount: int = 1) -> int: ...
    async def incrbyfloat(self, name: KeyT, amount: float = 1.0) -> float: ...
    async def keys(self, pattern: PatternT = "*", **kwargs) -> list[_StrType]: ...
    async def lmove(
        self,
        first_list: KeyT,
        second_list: KeyT,
        src: str = "LEFT",
        dest: str = "RIGHT",
    ) -> _StrType | None: ...
    async def blmove(
        self,
        first_list: KeyT,
        second_list: KeyT,
        timeout: int,
        src: str = "LEFT",
        dest: str = "RIGHT",
    ) -> _StrType | None: ...
    async def mget(self, keys: KeysT, *args: EncodableT) -> list[_StrType | None]: ...
    async def mset(self, mapping: Mapping[AnyKeyT, EncodableT]) -> Literal[True]: ...
    async def msetnx(self, mapping: Mapping[AnyKeyT, EncodableT]) -> bool: ...
    async def move(self, name: KeyT, db: str | int) -> bool: ...
    async def persist(self, name: KeyT) -> bool: ...
    async def pexpire(
        self,
        name: KeyT,
        time: ExpiryT,
        nx: bool = False,
        xx: bool = False,
        gt: bool = False,
        lt: bool = False,
    ) -> bool: ...
    async def pexpireat(
        self,
        name: KeyT,
        when: AbsExpiryT,
        nx: bool = False,
        xx: bool = False,
        gt: bool = False,
        lt: bool = False,
    ) -> bool: ...
    async def pexpiretime(self, key: KeyT) -> int: ...
    async def psetex(
        self, name: KeyT, time_ms: ExpiryT, value: EncodableT
    ) -> Literal[True]: ...
    async def pttl(self, name: KeyT) -> int: ...
    @overload
    async def hrandfield(
        self, key: KeyT, count: None = None, withvalues: Literal[False] = False
    ) -> _StrType | None: ...
    @overload
    async def hrandfield(
        self, key: KeyT, count: int, withvalues: bool = False
    ) -> list[_StrType]: ...
    async def randomkey(self, **kwargs) -> _StrType | None: ...
    async def rename(self, src: KeyT, dst: KeyT) -> Literal[True]: ...
    async def renamenx(self, src: KeyT, dst: KeyT) -> bool: ...
    async def restore(
        self,
        name: KeyT,
        ttl: float,
        value: EncodableT,
        replace: bool = False,
        absttl: bool = False,
        idletime: int | None = None,
        frequency: int | None = None,
    ) -> _StrType: ...
    async def set(
        self,
        name: KeyT,
        value: EncodableT,
        ex: ExpiryT | None = None,
        px: ExpiryT | None = None,
        nx: bool = False,
        xx: bool = False,
        keepttl: bool = False,
        get: bool = False,
        exat: AbsExpiryT | None = None,
        pxat: AbsExpiryT | None = None,
    ) -> bool | _StrType | None: ...
    async def __setitem__(self, name: KeyT, value: EncodableT) -> None: ...
    async def setbit(self, name: KeyT, offset: int, value: int) -> int: ...
    async def setex(
        self, name: KeyT, time: ExpiryT, value: EncodableT
    ) -> Literal[True]: ...
    async def setnx(self, name: KeyT, value: EncodableT) -> bool: ...
    async def setrange(self, name: KeyT, offset: int, value: EncodableT) -> int: ...
    async def stralgo(
        self,
        algo: Literal["LCS"],
        value1: KeyT,
        value2: KeyT,
        specific_argument: Literal["strings"] | Literal["keys"] = "strings",
        len: bool = False,
        idx: bool = False,
        minmatchlen: int | None = None,
        withmatchlen: bool = False,
        **kwargs,
    ) -> str | dict[str, Any]: ...
    async def strlen(self, name: KeyT) -> int: ...
    async def substr(self, name: KeyT, start: int, end: int = -1) -> _StrType: ...
    async def touch(self, *args: KeyT) -> int: ...
    async def ttl(self, name: KeyT) -> int: ...
    async def type(self, name: KeyT) -> _StrType: ...
    async def watch(self, *names: KeyT) -> None: ...
    async def unwatch(self) -> None: ...
    async def unlink(self, *names: KeyT) -> int: ...
    async def lcs(
        self,
        key1: str,
        key2: str,
        len: bool | None = False,
        idx: bool | None = False,
        minmatchlen: int | None = 0,
        withmatchlen: bool | None = False,
    ) -> str | int | list: ...

class ListCommands(CommandsProtocol, Generic[_StrType]):
    @overload
    def blpop(
        self, keys: _Key | Iterable[_Key], timeout: Literal[0]
    ) -> tuple[_StrType, _StrType]: ...
    @overload
    def blpop(
        self, keys: _Key | Iterable[_Key], timeout: float
    ) -> tuple[_StrType, _StrType] | None: ...
    @overload
    def brpop(
        self, keys: _Key | Iterable[_Key], timeout: Literal[0]
    ) -> tuple[_StrType, _StrType]: ...
    @overload
    def brpop(
        self, keys: _Key | Iterable[_Key], timeout: float
    ) -> tuple[_StrType, _StrType] | None: ...
    @overload
    def brpoplpush(self, src: _Key, dst: _Key, timeout: Literal[0]) -> _StrType: ...
    @overload
    def brpoplpush(self, src: _Key, dst: _Key, timeout: float) -> _StrType | None: ...
    @overload
    def blmpop(
        self,
        timeout: Literal[0],
        numkeys: int,
        *keys: _Key,
        direction: Literal["LEFT"] | Literal["RIGHT"],
        count: int = 1,
    ) -> tuple[_StrType, list[_StrType]]: ...
    @overload
    def blmpop(
        self,
        timeout: float,
        numkeys: int,
        *keys: _Key,
        direction: Literal["LEFT"] | Literal["RIGHT"],
        count: int = 1,
    ) -> tuple[_StrType, list[_StrType]] | None: ...
    def lmpop(
        self,
        numkeys: int,
        *keys: _Key,
        direction: Literal["LEFT"] | Literal["RIGHT"],
        count: int = 1,
    ) -> tuple[_StrType, list[_StrType]] | None: ...
    def lindex(self, name: _Key, index: int) -> _StrType | None: ...
    def linsert(
        self,
        name: _Key,
        where: Literal["BEFORE"] | Literal["AFTER"],
        refvalue: _Value,
        value: _Value,
    ) -> int: ...
    def llen(self, name: _Key) -> int: ...
    @overload
    def lpop(self, name: _Key) -> _StrType | None: ...
    @overload
    def lpop(self, name: _Key, count: int) -> list[_StrType] | None: ...
    def lpush(self, name: _Key, *values: _Value) -> int: ...
    def lpushx(self, name: _Key, *values: _Value) -> int: ...
    def lrange(self, name: _Key, start: int, end: int) -> list[_StrType]: ...
    def lrem(self, name: _Key, count: int, value: _Value) -> int: ...
    def lset(self, name: _Key, index: int, value: _Value) -> Literal[True]: ...
    def ltrim(self, name: _Key, start: int, end: int) -> Literal[True]: ...
    @overload
    def rpop(self, name: _Key) -> _StrType | None: ...
    @overload
    def rpop(self, name: _Key, count: int) -> list[_StrType] | None: ...
    def rpoplpush(self, src: _Key, dst: _Key) -> _StrType | None: ...
    def rpush(self, name: _Key, *values: _Value) -> int: ...
    def rpushx(self, name: _Key, *values: _Value) -> int: ...
    @overload
    def lpos(
        self,
        name: _Key,
        value: _Value,
        rank: int | None = None,
        count: None = None,
        maxlen: int | None = None,
    ) -> int | None: ...
    @overload
    def lpos(
        self,
        name: _Key,
        value: _Value,
        rank: int | None = None,
        *,
        count: int,
        maxlen: int | None = None,
    ) -> list[int]: ...
    @overload
    def lpos(
        self,
        name: _Key,
        value: _Value,
        rank: int | None,
        count: int,
        maxlen: int | None = None,
    ) -> list[int]: ...
    @overload
    def sort(
        self,
        name: _Key,
        start: int | None = None,
        num: int | None = None,
        by: _Key | None = None,
        get: _Key | Sequence[_Key] | None = None,
        desc: bool = False,
        alpha: bool = False,
        store: None = None,
        groups: bool | None = False,
    ) -> list[_StrType]: ...
    @overload
    def sort(
        self,
        name: _Key,
        start: int | None = None,
        num: int | None = None,
        by: _Key | None = None,
        get: _Key | Sequence[_Key] | None = None,
        desc: bool = False,
        alpha: bool = False,
        *,
        store: _Key,
        groups: bool = False,
    ) -> int: ...
    @overload
    def sort(
        self,
        name: _Key,
        start: int | None,
        num: int | None,
        by: _Key | None,
        get: _Key | Sequence[_Key] | None,
        desc: bool,
        alpha: bool,
        store: _Key,
        groups: bool = False,
    ) -> int: ...
    def sort_ro(
        self,
        key: _Key,
        start: int | None = None,
        num: int | None = None,
        by: _Key | None = None,
        get: _Key | Sequence[_Key] | None = None,
        desc: bool = False,
        alpha: bool = False,
    ) -> list[_StrType]: ...

class AsyncListCommands(CommandsProtocol, Generic[_StrType]):
    @overload
    async def blpop(
        self, keys: _Key | Iterable[_Key], timeout: Literal[0]
    ) -> tuple[_StrType, _StrType]: ...
    @overload
    async def blpop(
        self, keys: _Key | Iterable[_Key], timeout: float
    ) -> tuple[_StrType, _StrType] | None: ...
    @overload
    async def brpop(
        self, keys: _Key | Iterable[_Key], timeout: Literal[0]
    ) -> tuple[_StrType, _StrType]: ...
    @overload
    async def brpop(
        self, keys: _Key | Iterable[_Key], timeout: float
    ) -> tuple[_StrType, _StrType] | None: ...
    @overload
    async def brpoplpush(
        self, src: _Key, dst: _Key, timeout: Literal[0]
    ) -> _StrType: ...
    @overload
    async def brpoplpush(
        self, src: _Key, dst: _Key, timeout: float
    ) -> _StrType | None: ...
    @overload
    async def blmpop(
        self,
        timeout: Literal[0],
        numkeys: int,
        *keys: _Key,
        direction: Literal["LEFT"] | Literal["RIGHT"],
        count: int = 1,
    ) -> tuple[_StrType, list[_StrType]]: ...
    @overload
    async def blmpop(
        self,
        timeout: float,
        numkeys: int,
        *keys: _Key,
        direction: Literal["LEFT"] | Literal["RIGHT"],
        count: int = 1,
    ) -> tuple[_StrType, list[_StrType]] | None: ...
    async def lmpop(
        self,
        numkeys: int,
        *keys: _Key,
        direction: Literal["LEFT"] | Literal["RIGHT"],
        count: int = 1,
    ) -> tuple[_StrType, list[_StrType]] | None: ...
    async def lindex(self, name: _Key, index: int) -> _StrType | None: ...
    async def linsert(
        self,
        name: _Key,
        where: Literal["BEFORE"] | Literal["AFTER"],
        refvalue: _Value,
        value: _Value,
    ) -> int: ...
    async def llen(self, name: _Key) -> int: ...
    @overload
    async def lpop(self, name: _Key) -> _StrType | None: ...
    @overload
    async def lpop(self, name: _Key, count: int) -> list[_StrType] | None: ...
    async def lpush(self, name: _Key, *values: _Value) -> int: ...
    async def lpushx(self, name: _Key, *values: _Value) -> int: ...
    async def lrange(self, name: _Key, start: int, end: int) -> list[_StrType]: ...
    async def lrem(self, name: _Key, count: int, value: _Value) -> int: ...
    async def lset(self, name: _Key, index: int, value: _Value) -> Literal[True]: ...
    async def ltrim(self, name: _Key, start: int, end: int) -> Literal[True]: ...
    @overload
    async def rpop(self, name: _Key) -> _StrType | None: ...
    @overload
    async def rpop(self, name: _Key, count: int) -> list[_StrType] | None: ...
    async def rpoplpush(self, src: _Key, dst: _Key) -> _StrType | None: ...
    async def rpush(self, name: _Key, *values: _Value) -> int: ...
    async def rpushx(self, name: _Key, *values: _Value) -> int: ...
    @overload
    async def lpos(
        self,
        name: _Key,
        value: _Value,
        rank: int | None = None,
        count: None = None,
        maxlen: int | None = None,
    ) -> int | None: ...
    @overload
    async def lpos(
        self,
        name: _Key,
        value: _Value,
        rank: int | None = None,
        *,
        count: int,
        maxlen: int | None = None,
    ) -> list[int]: ...
    @overload
    async def lpos(
        self,
        name: _Key,
        value: _Value,
        rank: int | None,
        count: int,
        maxlen: int | None = None,
    ) -> list[int]: ...
    @overload
    async def sort(
        self,
        name: _Key,
        start: int | None = None,
        num: int | None = None,
        by: _Key | None = None,
        get: _Key | Sequence[_Key] | None = None,
        desc: bool = False,
        alpha: bool = False,
        store: None = None,
        groups: bool | None = False,
    ) -> list[_StrType]: ...
    @overload
    async def sort(
        self,
        name: _Key,
        start: int | None = None,
        num: int | None = None,
        by: _Key | None = None,
        get: _Key | Sequence[_Key] | None = None,
        desc: bool = False,
        alpha: bool = False,
        *,
        store: _Key,
        groups: bool = False,
    ) -> int: ...
    @overload
    async def sort(
        self,
        name: _Key,
        start: int | None,
        num: int | None,
        by: _Key | None,
        get: _Key | Sequence[_Key] | None,
        desc: bool,
        alpha: bool,
        store: _Key,
        groups: bool = False,
    ) -> int: ...
    async def sort_ro(
        self,
        key: _Key,
        start: int | None = None,
        num: int | None = None,
        by: _Key | None = None,
        get: _Key | Sequence[_Key] | None = None,
        desc: bool = False,
        alpha: bool = False,
    ) -> list[_StrType]: ...

class ScanCommands(CommandsProtocol, Generic[_StrType]):
    def scan(
        self,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
        _type: str | None = None,
        **kwargs: _CommandOptions,
    ) -> tuple[int, list[_StrType]]: ...
    def scan_iter(
        self,
        match: _Key | None = None,
        count: int | None = None,
        _type: str | None = None,
        **kwargs: _CommandOptions,
    ) -> Iterator[_StrType]: ...
    def sscan(
        self,
        name: _Key,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
    ) -> tuple[int, list[_StrType]]: ...
    def sscan_iter(
        self, name: _Key, match: _Key | None = None, count: int | None = None
    ) -> Iterator[_StrType]: ...
    @overload
    def hscan(
        self,
        name: _Key,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
        no_values: Literal[False] | None = None,
    ) -> tuple[int, dict[_StrType, _StrType]]: ...
    @overload
    def hscan(
        self,
        name: _Key,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
        *,
        no_values: Literal[True],
    ) -> tuple[int, list[_StrType]]: ...
    @overload
    def hscan(
        self,
        name: _Key,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
        no_values: bool | None = None,
    ) -> tuple[int, dict[_StrType, _StrType] | list[_StrType]]: ...
    @overload
    def hscan_iter(
        self,
        name: _Key,
        match: _Key | None = None,
        count: int | None = None,
        no_values: Literal[False] | None = None,
    ) -> Iterator[tuple[_StrType, _StrType]]: ...
    @overload
    def hscan_iter(
        self,
        name: _Key,
        match: _Key | None = None,
        count: int | None = None,
        *,
        no_values: Literal[True],
    ) -> Iterator[_StrType]: ...
    @overload
    def hscan_iter(
        self,
        name: _Key,
        match: _Key | None = None,
        count: int | None = None,
        no_values: bool | None = None,
    ) -> Iterator[_StrType] | Iterator[tuple[_StrType, _StrType]]: ...
    @overload
    def zscan(
        self,
        name: _Key,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
    ) -> tuple[int, list[tuple[_StrType, float]]]: ...
    @overload
    def zscan(
        self,
        name: _Key,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
        *,
        score_cast_func: Callable[[_StrType], _ScoreCastFuncReturn],
    ) -> tuple[int, list[tuple[_StrType, _ScoreCastFuncReturn]]]: ...
    @overload
    def zscan(
        self,
        name: _Key,
        cursor: int,
        match: _Key | None,
        count: int | None,
        score_cast_func: Callable[[_StrType], _ScoreCastFuncReturn],
    ) -> tuple[int, list[tuple[_StrType, _ScoreCastFuncReturn]]]: ...
    @overload
    def zscan_iter(
        self, name: _Key, match: _Key | None = None, count: int | None = None
    ) -> Iterator[tuple[_StrType, float]]: ...
    @overload
    def zscan_iter(
        self,
        name: _Key,
        match: _Key | None = None,
        count: int | None = None,
        *,
        score_cast_func: Callable[[_StrType], _ScoreCastFuncReturn],
    ) -> Iterator[tuple[_StrType, _ScoreCastFuncReturn]]: ...
    @overload
    def zscan_iter(
        self,
        name: KeyT,
        match: PatternT | None,
        count: int | None,
        score_cast_func: Callable[[_StrType], _ScoreCastFuncReturn],
    ) -> Iterator[tuple[_StrType, _ScoreCastFuncReturn]]: ...

class AsyncScanCommands(CommandsProtocol, Generic[_StrType]):
    async def scan(
        self,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
        _type: str | None = None,
        **kwargs: _CommandOptions,
    ) -> tuple[int, list[_StrType]]: ...
    async def scan_iter(
        self,
        match: _Key | None = None,
        count: int | None = None,
        _type: str | None = None,
        **kwargs: _CommandOptions,
    ) -> AsyncIterator[_StrType]: ...
    async def sscan(
        self,
        name: _Key,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
    ) -> tuple[int, list[_StrType]]: ...
    async def sscan_iter(
        self, name: _Key, match: _Key | None = None, count: int | None = None
    ) -> AsyncIterator[_StrType]: ...
    @overload
    async def hscan(
        self,
        name: _Key,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
        no_values: Literal[False] | None = None,
    ) -> tuple[int, dict[_StrType, _StrType]]: ...
    @overload
    async def hscan(
        self,
        name: _Key,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
        *,
        no_values: Literal[True],
    ) -> tuple[int, list[_StrType]]: ...
    @overload
    async def hscan(
        self,
        name: _Key,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
        no_values: bool | None = None,
    ) -> tuple[int, dict[_StrType, _StrType] | list[_StrType]]: ...
    @overload
    async def hscan_iter(
        self,
        name: _Key,
        match: _Key | None = None,
        count: int | None = None,
        no_values: Literal[False] | None = None,
    ) -> AsyncIterator[tuple[_StrType, _StrType]]: ...
    @overload
    async def hscan_iter(
        self,
        name: _Key,
        match: _Key | None = None,
        count: int | None = None,
        *,
        no_values: Literal[True],
    ) -> AsyncIterator[_StrType]: ...
    @overload
    async def hscan_iter(
        self,
        name: _Key,
        match: _Key | None = None,
        count: int | None = None,
        no_values: bool | None = None,
    ) -> AsyncIterator[_StrType] | AsyncIterator[tuple[_StrType, _StrType]]: ...
    @overload
    async def zscan(
        self,
        name: _Key,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
    ) -> tuple[int, list[tuple[_StrType, float]]]: ...
    @overload
    async def zscan(
        self,
        name: _Key,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
        *,
        score_cast_func: Callable[[_StrType], _ScoreCastFuncReturn],
    ) -> tuple[int, list[tuple[_StrType, _ScoreCastFuncReturn]]]: ...
    @overload
    async def zscan(
        self,
        name: _Key,
        cursor: int,
        match: _Key | None,
        count: int | None,
        score_cast_func: Callable[[_StrType], _ScoreCastFuncReturn],
    ) -> tuple[int, list[tuple[_StrType, _ScoreCastFuncReturn]]]: ...
    @overload
    async def zscan_iter(
        self, name: _Key, match: _Key | None = None, count: int | None = None
    ) -> AsyncIterator[tuple[_StrType, float]]: ...
    @overload
    async def zscan_iter(
        self,
        name: _Key,
        match: _Key | None = None,
        count: int | None = None,
        *,
        score_cast_func: Callable[[_StrType], _ScoreCastFuncReturn],
    ) -> AsyncIterator[tuple[_StrType, _ScoreCastFuncReturn]]: ...
    @overload
    async def zscan_iter(
        self,
        name: KeyT,
        match: PatternT | None,
        count: int | None,
        score_cast_func: Callable[[_StrType], _ScoreCastFuncReturn],
    ) -> AsyncIterator[tuple[_StrType, _ScoreCastFuncReturn]]: ...

class SetCommands(CommandsProtocol, Generic[_StrType]):
    def sadd(self, name: _Key, *values: _Value) -> int: ...
    def scard(self, name: _Key) -> int: ...
    def sdiff(self, keys: _Key | Iterable[_Key], *args: _Key) -> list[_StrType]: ...
    def sdiffstore(
        self, dest: _Key, keys: _Key | Iterable[_Key], *args: _Key
    ) -> int: ...
    def sinter(self, keys: _Key | Iterable[_Key], *args: _Key) -> list[_StrType]: ...
    def sintercard(self, numkeys: int, keys: Iterable[_Key], limit: int = 0) -> int: ...
    def sinterstore(
        self, dest: _Key, keys: _Key | Iterable[_Key], *args: _Key
    ) -> int: ...
    def sismember(self, name: _Key, value: _Value) -> Literal[0] | Literal[1]: ...
    def smembers(self, name: _Key) -> list[_StrType]: ...
    def smismember(
        self, name: _Key, values: _Value | Iterable[_Value], *args: _Value
    ) -> list[Literal[0] | Literal[1]]: ...
    def smove(self, src: _Key, dst: _Key, value: _Value) -> bool: ...
    @overload
    def spop(self, name: _Key, count: None = None) -> _StrType | None: ...
    @overload
    def spop(self, name: _Key, count: int) -> list[_StrType]: ...
    @overload
    def srandmember(self, name: _Key, number: None = None) -> _StrType | None: ...
    @overload
    def srandmember(self, name: _Key, number: int) -> list[_StrType]: ...
    def srem(self, name: _Key, *values: _Value) -> int: ...
    def sunion(self, keys: _Key | Iterable[_Key], *args: _Key) -> list[_StrType]: ...
    def sunionstore(
        self, dest: _Key, keys: _Key | Iterable[_Key], *args: _Key
    ) -> int: ...

class AsyncSetCommands(CommandsProtocol, Generic[_StrType]):
    async def sadd(self, name: _Key, *values: _Value) -> int: ...
    async def scard(self, name: _Key) -> int: ...
    async def sdiff(
        self, keys: _Key | Iterable[_Key], *args: _Key
    ) -> list[_StrType]: ...
    async def sdiffstore(
        self, dest: _Key, keys: _Key | Iterable[_Key], *args: _Key
    ) -> int: ...
    async def sinter(
        self, keys: _Key | Iterable[_Key], *args: _Key
    ) -> list[_StrType]: ...
    async def sintercard(
        self, numkeys: int, keys: Iterable[_Key], limit: int = 0
    ) -> int: ...
    async def sinterstore(
        self, dest: _Key, keys: _Key | Iterable[_Key], *args: _Key
    ) -> int: ...
    async def sismember(self, name: _Key, value: _Value) -> Literal[0] | Literal[1]: ...
    async def smembers(self, name: _Key) -> list[_StrType]: ...
    async def smismember(
        self, name: _Key, values: _Value | Iterable[_Value], *args: _Value
    ) -> list[Literal[0] | Literal[1]]: ...
    async def smove(self, src: _Key, dst: _Key, value: _Value) -> bool: ...
    @overload
    async def spop(self, name: _Key, count: None = None) -> _StrType | None: ...
    @overload
    async def spop(self, name: _Key, count: int) -> list[_StrType]: ...
    @overload
    async def srandmember(self, name: _Key, number: None = None) -> _StrType | None: ...
    @overload
    async def srandmember(self, name: _Key, number: int) -> list[_StrType]: ...
    async def srem(self, name: _Key, *values: _Value) -> int: ...
    async def sunion(
        self, keys: _Key | Iterable[_Key], *args: _Key
    ) -> list[_StrType]: ...
    async def sunionstore(
        self, dest: _Key, keys: _Key | Iterable[_Key], *args: _Key
    ) -> int: ...

class StreamCommands(CommandsProtocol, Generic[_StrType]):
    def xack(self, name: _Key, groupname: GroupT, *ids: StreamIdT) -> int: ...
    def xadd(
        self,
        name: _Key,
        fields: Mapping[AnyFieldT, AnyEncodableT],
        id: StreamIdT = "*",
        maxlen: int | None = None,
        approximate: bool = True,
        nomkstream: bool = False,
        minid: StreamIdT | None = None,
        limit: int | None = None,
    ) -> _StrType | None: ...
    @overload
    def xautoclaim(
        self,
        name: _Key,
        groupname: GroupT,
        consumername: ConsumerT,
        min_idle_time: int,
        start_id: StreamIdT = "0-0",
        count: int | None = None,
        justid: Literal[False] = False,
    ) -> list[_StrType | list[_StreamEntryT] | list[_StrType]]: ...
    @overload
    def xautoclaim(
        self,
        name: _Key,
        groupname: GroupT,
        consumername: ConsumerT,
        min_idle_time: int,
        start_id: StreamIdT = "0-0",
        count: int | None = None,
        *,
        justid: Literal[True],
    ) -> list[_StrType]: ...
    @overload
    def xautoclaim(
        self,
        name: _Key,
        groupname: GroupT,
        consumername: ConsumerT,
        min_idle_time: int,
        start_id: StreamIdT = "0-0",
        count: int | None = None,
        justid: bool = False,
    ) -> list[_StrType] | list[_StrType | list[_StreamEntryT] | list[_StrType]]: ...
    @overload
    def xclaim(
        self,
        name: _Key,
        groupname: GroupT,
        consumername: ConsumerT,
        min_idle_time: int,
        message_ids: list[StreamIdT] | tuple[StreamIdT],
        idle: int | None = None,
        time: int | None = None,
        retrycount: int | None = None,
        force: bool = False,
        justid: Literal[False] = False,
    ) -> list[_StreamEntryT]: ...
    @overload
    def xclaim(
        self,
        name: _Key,
        groupname: GroupT,
        consumername: ConsumerT,
        min_idle_time: int,
        message_ids: list[StreamIdT] | tuple[StreamIdT],
        idle: int | None = None,
        time: int | None = None,
        retrycount: int | None = None,
        force: bool = False,
        *,
        justid: Literal[True],
    ) -> list[_StrType]: ...
    @overload
    def xclaim(
        self,
        name: _Key,
        groupname: GroupT,
        consumername: ConsumerT,
        min_idle_time: int,
        message_ids: list[StreamIdT] | tuple[StreamIdT],
        idle: int | None = None,
        time: int | None = None,
        retrycount: int | None = None,
        force: bool = False,
        justid: bool = False,
    ) -> list[_StreamEntryT] | list[_StrType]: ...
    def xdel(self, name: _Key, *ids: StreamIdT) -> int: ...
    def xgroup_create(
        self,
        name: _Key,
        groupname: GroupT,
        id: StreamIdT = "$",
        mkstream: bool = False,
        entries_read: int | None = None,
    ) -> Literal[True]: ...
    def xgroup_delconsumer(
        self, name: _Key, groupname: GroupT, consumername: ConsumerT
    ) -> int: ...
    def xgroup_destroy(self, name: _Key, groupname: GroupT) -> bool: ...
    def xgroup_createconsumer(
        self, name: _Key, groupname: GroupT, consumername: ConsumerT
    ) -> Literal[1] | Literal[0]: ...
    def xgroup_setid(
        self,
        name: _Key,
        groupname: GroupT,
        id: StreamIdT,
        entries_read: int | None = None,
    ) -> Literal[True]: ...
    def xinfo_consumers(
        self, name: _Key, groupname: GroupT
    ) -> list[dict[str, Any]]: ...
    def xinfo_groups(self, name: _Key) -> list[dict[str, Any]]: ...
    def xinfo_stream(self, name: _Key, full: bool = False) -> dict[str, Any]: ...
    def xlen(self, name: _Key) -> int: ...
    def xpending(self, name: _Key, groupname: GroupT) -> dict[str, Any]: ...
    def xpending_range(
        self,
        name: _Key,
        groupname: GroupT,
        min: StreamIdT,
        max: StreamIdT,
        count: int,
        consumername: ConsumerT | None = None,
        idle: int | None = None,
    ) -> list[dict[str, Any]]: ...
    def xrange(
        self,
        name: _Key,
        min: StreamIdT = "-",
        max: StreamIdT = "+",
        count: int | None = None,
    ) -> list[_StreamEntryT]: ...
    def xread(
        self,
        streams: Mapping[AnyKeyT, AnyStreamIdT],
        count: int | None = None,
        block: int | None = None,
    ) -> _StreamReadResp2T | _StreamReadResp3T: ...
    def xreadgroup(
        self,
        groupname: GroupT,
        consumername: ConsumerT,
        streams: Mapping[AnyKeyT, AnyStreamIdT],
        count: int | None = None,
        block: int | None = None,
        noack: bool = False,
    ) -> _StreamReadResp2T | _StreamReadResp3T: ...
    def xrevrange(
        self,
        name: _Key,
        max: StreamIdT = "+",
        min: StreamIdT = "-",
        count: int | None = None,
    ) -> list[_StreamEntryT]: ...
    def xtrim(
        self,
        name: _Key,
        maxlen: int | None = None,
        approximate: bool = True,
        minid: StreamIdT | None = None,
        limit: int | None = None,
    ) -> int: ...

class AsyncStreamCommands(CommandsProtocol, Generic[_StrType]):
    async def xack(self, name: _Key, groupname: GroupT, *ids: StreamIdT) -> int: ...
    async def xadd(
        self,
        name: _Key,
        fields: Mapping[AnyFieldT, AnyEncodableT],
        id: StreamIdT = "*",
        maxlen: int | None = None,
        approximate: bool = True,
        nomkstream: bool = False,
        minid: StreamIdT | None = None,
        limit: int | None = None,
    ) -> _StrType | None: ...
    @overload
    async def xautoclaim(
        self,
        name: _Key,
        groupname: GroupT,
        consumername: ConsumerT,
        min_idle_time: int,
        start_id: StreamIdT = "0-0",
        count: int | None = None,
        justid: Literal[False] = False,
    ) -> list[_StrType | list[_StreamEntryT] | list[_StrType]]: ...
    @overload
    async def xautoclaim(
        self,
        name: _Key,
        groupname: GroupT,
        consumername: ConsumerT,
        min_idle_time: int,
        start_id: StreamIdT = "0-0",
        count: int | None = None,
        *,
        justid: Literal[True],
    ) -> list[_StrType]: ...
    @overload
    async def xautoclaim(
        self,
        name: _Key,
        groupname: GroupT,
        consumername: ConsumerT,
        min_idle_time: int,
        start_id: StreamIdT = "0-0",
        count: int | None = None,
        justid: bool = False,
    ) -> list[_StrType] | list[_StrType | list[_StreamEntryT] | list[_StrType]]: ...
    @overload
    async def xclaim(
        self,
        name: _Key,
        groupname: GroupT,
        consumername: ConsumerT,
        min_idle_time: int,
        message_ids: list[StreamIdT] | tuple[StreamIdT],
        idle: int | None = None,
        time: int | None = None,
        retrycount: int | None = None,
        force: bool = False,
        justid: Literal[False] = False,
    ) -> list[_StreamEntryT]: ...
    @overload
    async def xclaim(
        self,
        name: _Key,
        groupname: GroupT,
        consumername: ConsumerT,
        min_idle_time: int,
        message_ids: list[StreamIdT] | tuple[StreamIdT],
        idle: int | None = None,
        time: int | None = None,
        retrycount: int | None = None,
        force: bool = False,
        *,
        justid: Literal[True],
    ) -> list[_StrType]: ...
    @overload
    async def xclaim(
        self,
        name: _Key,
        groupname: GroupT,
        consumername: ConsumerT,
        min_idle_time: int,
        message_ids: list[StreamIdT] | tuple[StreamIdT],
        idle: int | None = None,
        time: int | None = None,
        retrycount: int | None = None,
        force: bool = False,
        justid: bool = False,
    ) -> list[_StreamEntryT] | list[_StrType]: ...
    async def xdel(self, name: _Key, *ids: StreamIdT) -> int: ...
    async def xgroup_create(
        self,
        name: _Key,
        groupname: GroupT,
        id: StreamIdT = "$",
        mkstream: bool = False,
        entries_read: int | None = None,
    ) -> Literal[True]: ...
    async def xgroup_delconsumer(
        self, name: _Key, groupname: GroupT, consumername: ConsumerT
    ) -> int: ...
    async def xgroup_destroy(self, name: _Key, groupname: GroupT) -> bool: ...
    async def xgroup_createconsumer(
        self, name: _Key, groupname: GroupT, consumername: ConsumerT
    ) -> Literal[1] | Literal[0]: ...
    async def xgroup_setid(
        self,
        name: _Key,
        groupname: GroupT,
        id: StreamIdT,
        entries_read: int | None = None,
    ) -> Literal[True]: ...
    async def xinfo_consumers(
        self, name: _Key, groupname: GroupT
    ) -> list[dict[str, Any]]: ...
    async def xinfo_groups(self, name: _Key) -> list[dict[str, Any]]: ...
    async def xinfo_stream(self, name: _Key, full: bool = False) -> dict[str, Any]: ...
    async def xlen(self, name: _Key) -> int: ...
    async def xpending(self, name: _Key, groupname: GroupT) -> dict[str, Any]: ...
    async def xpending_range(
        self,
        name: _Key,
        groupname: GroupT,
        min: StreamIdT,
        max: StreamIdT,
        count: int,
        consumername: ConsumerT | None = None,
        idle: int | None = None,
    ) -> list[dict[str, Any]]: ...
    async def xrange(
        self,
        name: _Key,
        min: StreamIdT = "-",
        max: StreamIdT = "+",
        count: int | None = None,
    ) -> list[_StreamEntryT]: ...
    async def xread(
        self,
        streams: Mapping[AnyKeyT, AnyStreamIdT],
        count: int | None = None,
        block: int | None = None,
    ) -> _StreamReadResp2T | _StreamReadResp3T: ...
    async def xreadgroup(
        self,
        groupname: GroupT,
        consumername: ConsumerT,
        streams: Mapping[AnyKeyT, AnyStreamIdT],
        count: int | None = None,
        block: int | None = None,
        noack: bool = False,
    ) -> _StreamReadResp2T | _StreamReadResp3T: ...
    async def xrevrange(
        self,
        name: _Key,
        max: StreamIdT = "+",
        min: StreamIdT = "-",
        count: int | None = None,
    ) -> list[_StreamEntryT]: ...
    async def xtrim(
        self,
        name: _Key,
        maxlen: int | None = None,
        approximate: bool = True,
        minid: StreamIdT | None = None,
        limit: int | None = None,
    ) -> int: ...

class SortedSetCommands(CommandsProtocol, Generic[_StrType]):
    @overload
    def zadd(
        self,
        name: _Key,
        mapping: Mapping[AnyKeyT, EncodableT],
        nx: bool = False,
        xx: bool = False,
        ch: bool = False,
        incr: Literal[False] = False,
        gt: bool = False,
        lt: bool = False,
    ) -> int: ...
    @overload
    def zadd(
        self,
        name: _Key,
        mapping: Mapping[AnyKeyT, EncodableT],
        nx: bool = False,
        xx: bool = False,
        ch: bool = False,
        incr: Literal[True] = True,
        gt: bool = False,
        lt: bool = False,
    ) -> float | None: ...
    @overload
    def zadd(
        self,
        name: _Key,
        mapping: Mapping[AnyKeyT, EncodableT],
        nx: bool = False,
        xx: bool = False,
        ch: bool = False,
        incr: bool = False,
        gt: bool = False,
        lt: bool = False,
    ) -> int | float | None: ...
    def zcard(self, name: _Key) -> int: ...
    def zcount(self, name: _Key, min: ZScoreBoundT, max: ZScoreBoundT) -> int: ...
    @overload
    def zdiff(
        self, keys: Sequence[_Key], withscores: Literal[False] = False
    ) -> list[_StrType]: ...
    @overload
    def zdiff(
        self, keys: Sequence[_Key], withscores: Literal[True]
    ) -> list[_StrType] | list[_ZSetScorePairT]: ...
    @overload
    def zdiff(
        self, keys: Sequence[_Key], withscores: bool = False
    ) -> list[_StrType] | list[_ZSetScorePairT]: ...
    def zdiffstore(self, dest: _Key, keys: Sequence[_Key]) -> int: ...
    def zincrby(self, name: _Key, amount: float, value: _Value) -> float: ...
    @overload
    def zinter(
        self, keys: Sequence[_Key], aggregate: str | None = None
    ) -> list[_StrType]: ...
    @overload
    def zinter(
        self,
        keys: Sequence[_Key],
        aggregate: str | None = None,
        withscores: Literal[False] = False,
    ) -> list[_StrType]: ...
    @overload
    def zinter(
        self, keys: Sequence[_Key], aggregate: str | None, withscores: Literal[True]
    ) -> list[_ZSetScorePairT]: ...
    @overload
    def zinter(
        self,
        keys: Sequence[_Key],
        aggregate: str | None = None,
        withscores: bool = False,
    ) -> list[_StrType] | list[_ZSetScorePairT]: ...
    def zinterstore(
        self,
        dest: _Key,
        keys: Sequence[_Key],
        aggregate: str | None = None,
    ) -> int: ...
    def zintercard(self, numkeys: int, keys: Sequence[_Key], limit: int = 0) -> int: ...
    def zlexcount(self, name: _Key, min: _Value, max: _Value) -> int: ...
    def zpopmax(
        self, name: _Key, count: int | None = None
    ) -> list[_ZSetScorePairT]: ...
    def zpopmin(
        self, name: _Key, count: int | None = None
    ) -> list[_ZSetScorePairT]: ...
    @overload
    def zrandmember(self, key: _Key, count: None = None) -> _StrType | None: ...
    @overload
    def zrandmember(
        self, key: _Key, count: int, withscores: Literal[False] = False
    ) -> list[_StrType]: ...
    # With RESP2, scores are always returned as strings, so withscores=True
    # doesn't change the return type
    @overload
    def zrandmember(
        self, key: _Key, count: int, withscores: Literal[True]
    ) -> list[_StrType] | list[_ZSetScorePairT]: ...
    @overload
    def zrandmember(
        self, key: _Key, count: int, withscores: bool = False
    ) -> list[_StrType] | list[_ZSetScorePairT]: ...
    # tuples are returned for RESP2, list for RESP3
    def bzpopmax(
        self, keys: KeysT, timeout: TimeoutSecT = 0
    ) -> tuple[_StrType, _StrType, float] | list[_StrType | float] | None: ...
    def bzpopmin(
        self, keys: KeysT, timeout: TimeoutSecT = 0
    ) -> tuple[_StrType, _StrType, float] | list[_StrType | float] | None: ...
    def zmpop(
        self,
        num_keys: int,
        keys: Sequence[_Key],
        min: bool | None = False,
        max: bool | None = False,
        count: int = 1,
    ) -> list[Any] | None: ...
    def bzmpop(
        self,
        timeout: float,
        numkeys: int,
        keys: Sequence[_Key],
        min: bool | None = False,
        max: bool | None = False,
        count: int = 1,
    ) -> list[Any] | None: ...
    def zrange(
        self,
        name: _Key,
        start: int,
        end: int,
        desc: bool = False,
        withscores: bool = False,
        score_cast_func: type | Callable = ...,
        byscore: bool = False,
        bylex: bool = False,
        offset: int | None = None,
        num: int | None = None,
    ) -> list[_StrType] | list[_ZSetScorePairT]: ...
    @overload
    def zrevrange(
        self,
        name: _Key,
        start: int,
        end: int,
        withscores: Literal[False] = False,
        score_cast_func: type | Callable = ...,
    ) -> list[_StrType]: ...
    @overload
    def zrevrange(
        self,
        name: _Key,
        start: int,
        end: int,
        withscores: Literal[True],
        score_cast_func: type | Callable = ...,
    ) -> list[_ZSetScorePairT]: ...
    @overload
    def zrevrange(
        self,
        name: _Key,
        start: int,
        end: int,
        withscores: bool = False,
        score_cast_func: type | Callable = ...,
    ) -> list[_StrType] | list[_ZSetScorePairT]: ...
    def zrangestore(
        self,
        dest: _Key,
        name: _Key,
        start: int,
        end: int,
        byscore: bool = False,
        bylex: bool = False,
        desc: bool = False,
        offset: int | None = None,
        num: int | None = None,
    ) -> int: ...
    def zrangebylex(
        self,
        name: _Key,
        min: _Value,
        max: _Value,
        start: int | None = None,
        num: int | None = None,
    ) -> list[_StrType]: ...
    def zrevrangebylex(
        self,
        name: _Key,
        max: _Value,
        min: _Value,
        start: int | None = None,
        num: int | None = None,
    ) -> list[_StrType]: ...
    def zrangebyscore(
        self,
        name: _Key,
        min: ZScoreBoundT,
        max: ZScoreBoundT,
        start: int | None = None,
        num: int | None = None,
        withscores: bool = False,
        score_cast_func: type | Callable = ...,
    ) -> list[_StrType] | list[_ZSetScorePairT]: ...
    def zrevrangebyscore(
        self,
        name: _Key,
        max: ZScoreBoundT,
        min: ZScoreBoundT,
        start: int | None = None,
        num: int | None = None,
        withscores: bool = False,
        score_cast_func: type | Callable = ...,
    ) -> list[_StrType] | list[_ZSetScorePairT]: ...
    @overload
    def zrank(
        self, name: _Key, value: _Value, withscore: Literal[False] = False
    ) -> int | None: ...
    @overload
    def zrank(
        self, name: _Key, value: _Value, withscore: Literal[True]
    ) -> list[int | float | _StrType] | None: ...
    @overload
    def zrank(
        self, name: _Key, value: _Value, withscore: bool = False
    ) -> int | list[int | float | _StrType] | None: ...
    def zrem(self, name: _Key, *values: FieldT) -> int: ...
    def zremrangebylex(self, name: _Key, min: _Value, max: _Value) -> int: ...
    def zremrangebyrank(self, name: _Key, min: int, max: int) -> int: ...
    def zremrangebyscore(
        self, name: _Key, min: ZScoreBoundT, max: ZScoreBoundT
    ) -> int: ...
    @overload
    def zrevrank(
        self, name: _Key, value: _Value, withscore: Literal[False] = False
    ) -> int | None: ...
    @overload
    def zrevrank(
        self, name: _Key, value: _Value, withscore: Literal[True]
    ) -> list[int | float | _StrType] | None: ...
    @overload
    def zrevrank(
        self, name: _Key, value: _Value, withscore: bool = False
    ) -> int | list[int | float | _StrType] | None: ...
    def zscore(self, name: _Key, value: _Value) -> float | None: ...
    @overload
    def zunion(
        self,
        keys: Sequence[_Key] | Mapping[AnyKeyT, float],
        aggregate: str | None = None,
    ) -> list[_StrType]: ...
    @overload
    def zunion(
        self,
        keys: Sequence[_Key] | Mapping[AnyKeyT, float],
        aggregate: str | None = None,
        withscores: Literal[False] = False,
    ) -> list[_StrType]: ...
    @overload
    def zunion(
        self,
        keys: Sequence[_Key] | Mapping[AnyKeyT, float],
        aggregate: str | None,
        withscores: Literal[True],
    ) -> list[_ZSetScorePairT]: ...
    @overload
    def zunion(
        self,
        keys: Sequence[_Key] | Mapping[AnyKeyT, float],
        aggregate: str | None = None,
        withscores: bool = False,
    ) -> list[_StrType] | list[_ZSetScorePairT]: ...
    def zunionstore(
        self,
        dest: _Key,
        keys: Sequence[_Key] | Mapping[AnyKeyT, float],
        aggregate: str | None = None,
    ) -> int: ...
    def zmscore(self, key: _Key, members: Sequence[_Value]) -> list[float | None]: ...

class AsyncSortedSetCommands(CommandsProtocol, Generic[_StrType]):
    @overload
    async def zadd(
        self,
        name: _Key,
        mapping: Mapping[AnyKeyT, EncodableT],
        nx: bool = False,
        xx: bool = False,
        ch: bool = False,
        incr: Literal[False] = False,
        gt: bool = False,
        lt: bool = False,
    ) -> int: ...
    @overload
    async def zadd(
        self,
        name: _Key,
        mapping: Mapping[AnyKeyT, EncodableT],
        nx: bool = False,
        xx: bool = False,
        ch: bool = False,
        incr: Literal[True] = True,
        gt: bool = False,
        lt: bool = False,
    ) -> float | None: ...
    @overload
    async def zadd(
        self,
        name: _Key,
        mapping: Mapping[AnyKeyT, EncodableT],
        nx: bool = False,
        xx: bool = False,
        ch: bool = False,
        incr: bool = False,
        gt: bool = False,
        lt: bool = False,
    ) -> int | float | None: ...
    async def zcard(self, name: _Key) -> int: ...
    async def zcount(self, name: _Key, min: ZScoreBoundT, max: ZScoreBoundT) -> int: ...
    @overload
    async def zdiff(
        self, keys: Sequence[_Key], withscores: Literal[False] = False
    ) -> list[_StrType]: ...
    @overload
    async def zdiff(
        self, keys: Sequence[_Key], withscores: Literal[True]
    ) -> list[_StrType] | list[_ZSetScorePairT]: ...
    @overload
    async def zdiff(
        self, keys: Sequence[_Key], withscores: bool = False
    ) -> list[_StrType] | list[_ZSetScorePairT]: ...
    async def zdiffstore(self, dest: _Key, keys: Sequence[_Key]) -> int: ...
    async def zincrby(self, name: _Key, amount: float, value: _Value) -> float: ...
    @overload
    async def zinter(
        self, keys: Sequence[_Key], aggregate: str | None = None
    ) -> list[_StrType]: ...
    @overload
    async def zinter(
        self,
        keys: Sequence[_Key],
        aggregate: str | None = None,
        withscores: Literal[False] = False,
    ) -> list[_StrType]: ...
    @overload
    async def zinter(
        self, keys: Sequence[_Key], aggregate: str | None, withscores: Literal[True]
    ) -> list[_ZSetScorePairT]: ...
    @overload
    async def zinter(
        self,
        keys: Sequence[_Key],
        aggregate: str | None = None,
        withscores: bool = False,
    ) -> list[_StrType] | list[_ZSetScorePairT]: ...
    async def zinterstore(
        self,
        dest: _Key,
        keys: Sequence[_Key],
        aggregate: str | None = None,
    ) -> int: ...
    async def zintercard(
        self, numkeys: int, keys: Sequence[_Key], limit: int = 0
    ) -> int: ...
    async def zlexcount(self, name: _Key, min: _Value, max: _Value) -> int: ...
    async def zpopmax(
        self, name: _Key, count: int | None = None
    ) -> list[_ZSetScorePairT]: ...
    async def zpopmin(
        self, name: _Key, count: int | None = None
    ) -> list[_ZSetScorePairT]: ...
    @overload
    async def zrandmember(self, key: _Key, count: None = None) -> _StrType | None: ...
    @overload
    async def zrandmember(
        self, key: _Key, count: int, withscores: Literal[False] = False
    ) -> list[_StrType]: ...
    # With RESP2, scores are always returned as strings, so withscores=True
    # doesn't change the return type
    @overload
    async def zrandmember(
        self, key: _Key, count: int, withscores: Literal[True]
    ) -> list[_StrType] | list[_ZSetScorePairT]: ...
    @overload
    async def zrandmember(
        self, key: _Key, count: int, withscores: bool = False
    ) -> list[_StrType] | list[_ZSetScorePairT]: ...
    # tuples are returned for RESP2, list for RESP3
    async def bzpopmax(
        self, keys: KeysT, timeout: TimeoutSecT = 0
    ) -> tuple[_StrType, _StrType, float] | list[_StrType | float] | None: ...
    async def bzpopmin(
        self, keys: KeysT, timeout: TimeoutSecT = 0
    ) -> tuple[_StrType, _StrType, float] | list[_StrType | float] | None: ...
    async def zmpop(
        self,
        num_keys: int,
        keys: Sequence[_Key],
        min: bool | None = False,
        max: bool | None = False,
        count: int = 1,
    ) -> list[Any] | None: ...
    async def bzmpop(
        self,
        timeout: float,
        numkeys: int,
        keys: Sequence[_Key],
        min: bool | None = False,
        max: bool | None = False,
        count: int = 1,
    ) -> list[Any] | None: ...
    async def zrange(
        self,
        name: _Key,
        start: int,
        end: int,
        desc: bool = False,
        withscores: bool = False,
        score_cast_func: type | Callable = ...,
        byscore: bool = False,
        bylex: bool = False,
        offset: int | None = None,
        num: int | None = None,
    ) -> list[_StrType] | list[_ZSetScorePairT]: ...
    @overload
    async def zrevrange(
        self,
        name: _Key,
        start: int,
        end: int,
        withscores: Literal[False] = False,
        score_cast_func: type | Callable = ...,
    ) -> list[_StrType]: ...
    @overload
    async def zrevrange(
        self,
        name: _Key,
        start: int,
        end: int,
        withscores: Literal[True],
        score_cast_func: type | Callable = ...,
    ) -> list[_ZSetScorePairT]: ...
    @overload
    async def zrevrange(
        self,
        name: _Key,
        start: int,
        end: int,
        withscores: bool = False,
        score_cast_func: type | Callable = ...,
    ) -> list[_StrType] | list[_ZSetScorePairT]: ...
    async def zrangestore(
        self,
        dest: _Key,
        name: _Key,
        start: int,
        end: int,
        byscore: bool = False,
        bylex: bool = False,
        desc: bool = False,
        offset: int | None = None,
        num: int | None = None,
    ) -> int: ...
    async def zrangebylex(
        self,
        name: _Key,
        min: _Value,
        max: _Value,
        start: int | None = None,
        num: int | None = None,
    ) -> list[_StrType]: ...
    async def zrevrangebylex(
        self,
        name: _Key,
        max: _Value,
        min: _Value,
        start: int | None = None,
        num: int | None = None,
    ) -> list[_StrType]: ...
    async def zrangebyscore(
        self,
        name: _Key,
        min: ZScoreBoundT,
        max: ZScoreBoundT,
        start: int | None = None,
        num: int | None = None,
        withscores: bool = False,
        score_cast_func: type | Callable = ...,
    ) -> list[_StrType] | list[_ZSetScorePairT]: ...
    async def zrevrangebyscore(
        self,
        name: _Key,
        max: ZScoreBoundT,
        min: ZScoreBoundT,
        start: int | None = None,
        num: int | None = None,
        withscores: bool = False,
        score_cast_func: type | Callable = ...,
    ) -> list[_StrType] | list[_ZSetScorePairT]: ...
    @overload
    async def zrank(
        self, name: _Key, value: _Value, withscore: Literal[False] = False
    ) -> int | None: ...
    @overload
    async def zrank(
        self, name: _Key, value: _Value, withscore: Literal[True]
    ) -> list[int | float | _StrType] | None: ...
    @overload
    async def zrank(
        self, name: _Key, value: _Value, withscore: bool = False
    ) -> int | list[int | float | _StrType] | None: ...
    async def zrem(self, name: _Key, *values: FieldT) -> int: ...
    async def zremrangebylex(self, name: _Key, min: _Value, max: _Value) -> int: ...
    async def zremrangebyrank(self, name: _Key, min: int, max: int) -> int: ...
    async def zremrangebyscore(
        self, name: _Key, min: ZScoreBoundT, max: ZScoreBoundT
    ) -> int: ...
    @overload
    async def zrevrank(
        self, name: _Key, value: _Value, withscore: Literal[False] = False
    ) -> int | None: ...
    @overload
    async def zrevrank(
        self, name: _Key, value: _Value, withscore: Literal[True]
    ) -> list[int | float | _StrType] | None: ...
    @overload
    async def zrevrank(
        self, name: _Key, value: _Value, withscore: bool = False
    ) -> int | list[int | float | _StrType] | None: ...
    async def zscore(self, name: _Key, value: _Value) -> float | None: ...
    @overload
    async def zunion(
        self,
        keys: Sequence[_Key] | Mapping[AnyKeyT, float],
        aggregate: str | None = None,
    ) -> list[_StrType]: ...
    @overload
    async def zunion(
        self,
        keys: Sequence[_Key] | Mapping[AnyKeyT, float],
        aggregate: str | None = None,
        withscores: Literal[False] = False,
    ) -> list[_StrType]: ...
    @overload
    async def zunion(
        self,
        keys: Sequence[_Key] | Mapping[AnyKeyT, float],
        aggregate: str | None,
        withscores: Literal[True],
    ) -> list[_ZSetScorePairT]: ...
    @overload
    async def zunion(
        self,
        keys: Sequence[_Key] | Mapping[AnyKeyT, float],
        aggregate: str | None = None,
        withscores: bool = False,
    ) -> list[_StrType] | list[_ZSetScorePairT]: ...
    async def zunionstore(
        self,
        dest: _Key,
        keys: Sequence[_Key] | Mapping[AnyKeyT, float],
        aggregate: str | None = None,
    ) -> int: ...
    async def zmscore(
        self, key: _Key, members: Sequence[_Value]
    ) -> list[float | None]: ...

class HyperlogCommands(CommandsProtocol):
    def pfadd(self, name: _Key, *values: _Value) -> int: ...
    def pfcount(self, *sources: _Key) -> int: ...
    def pfmerge(self, dest: _Key, *sources: _Key) -> Literal[True]: ...

class AsyncHyperlogCommands(CommandsProtocol):
    async def pfadd(self, name: _Key, *values: _Value) -> int: ...
    async def pfcount(self, *sources: _Key) -> int: ...
    async def pfmerge(self, dest: _Key, *sources: _Key) -> Literal[True]: ...

class HashCommands(CommandsProtocol, Generic[_StrType]):
    def hdel(self, name: _Key, *keys: _Value) -> int: ...
    def hexists(self, name: _Key, key: _Value) -> bool: ...
    def hget(self, name: _Key, key: _Value) -> _StrType | None: ...
    def hgetall(self, name: _Key) -> dict[_StrType, _StrType]: ...
    def hincrby(self, name: _Key, key: _Value, amount: int = 1) -> int: ...
    def hincrbyfloat(self, name: _Key, key: _Value, amount: float = 1.0) -> float: ...
    def hkeys(self, name: _Key) -> list[_StrType]: ...
    def hlen(self, name: _Key) -> int: ...
    def hset(
        self,
        name: _Key,
        key: _Value | None = None,
        value: _Value | None = None,
        mapping: Mapping[_Value, _Value] | None = None,
        items: Sequence[_Value] | None = None,
    ) -> int: ...
    def hsetnx(self, name: _Key, key: _Value, value: _Value) -> int: ...
    def hsetex(
        self,
        name: _Key,
        key: _Value | None = None,
        value: _Value | None = None,
        mapping: Mapping[_Value, _Value] | None = None,
        items: Sequence[_Value] | None = None,
        ex: ExpiryT | None = None,
        px: ExpiryT | None = None,
        exat: AbsExpiryT | None = None,
        pxat: AbsExpiryT | None = None,
        keepttl: bool = False,
        nx: bool = False,
        xx: bool = False,
        fnx: bool = False,
        fxx: bool = False,
    ) -> int: ...
    def hmset(self, name: _Key, mapping: Mapping[_Value, _Value]) -> Literal[True]: ...
    def hmget(
        self, name: _Key, keys: Sequence[_Value], *args: _Value
    ) -> list[_StrType | None]: ...
    def hvals(self, name: _Key) -> list[_StrType]: ...
    def hstrlen(self, name: _Key, key: _Value) -> int: ...

class AsyncHashCommands(CommandsProtocol, Generic[_StrType]):
    async def hdel(self, name: _Key, *keys: _Value) -> int: ...
    async def hexists(self, name: _Key, key: _Value) -> bool: ...
    async def hget(self, name: _Key, key: _Value) -> _StrType | None: ...
    async def hgetall(self, name: _Key) -> dict[_StrType, _StrType]: ...
    async def hincrby(self, name: _Key, key: _Value, amount: int = 1) -> int: ...
    async def hincrbyfloat(
        self, name: _Key, key: _Value, amount: float = 1.0
    ) -> float: ...
    async def hkeys(self, name: _Key) -> list[_StrType]: ...
    async def hlen(self, name: _Key) -> int: ...
    async def hset(
        self,
        name: _Key,
        key: _Value | None = None,
        value: _Value | None = None,
        mapping: Mapping[_Value, _Value] | None = None,
        items: Sequence[_Value] | None = None,
    ) -> int: ...
    async def hsetnx(self, name: _Key, key: _Value, value: _Value) -> int: ...
    async def hsetex(
        self,
        name: _Key,
        key: _Value | None = None,
        value: _Value | None = None,
        mapping: Mapping[_Value, _Value] | None = None,
        items: Sequence[_Value] | None = None,
        ex: ExpiryT | None = None,
        px: ExpiryT | None = None,
        exat: AbsExpiryT | None = None,
        pxat: AbsExpiryT | None = None,
        keepttl: bool = False,
        nx: bool = False,
        xx: bool = False,
        fnx: bool = False,
        fxx: bool = False,
    ) -> int: ...
    async def hmset(
        self, name: _Key, mapping: Mapping[_Value, _Value]
    ) -> Literal[True]: ...
    async def hmget(
        self, name: _Key, keys: Sequence[_Value], *args: _Value
    ) -> list[_StrType | None]: ...
    async def hvals(self, name: _Key) -> list[_StrType]: ...
    async def hstrlen(self, name: _Key, key: _Value) -> int: ...

class Script:
    registered_client: Valkey
    script: ScriptTextT
    sha: str
    def __init__(self, registered_client: Valkey, script: ScriptTextT) -> None: ...
    def __call__(
        self,
        keys: Sequence[KeyT] | None = None,
        args: Iterable[EncodableT] | None = None,
        client: Valkey | None = None,
    ) -> Any: ...
    def get_encoder(self) -> Any: ...

class AsyncScript:
    registered_client: AsyncValkey
    script: ScriptTextT
    sha: str
    def __init__(self, registered_client: AsyncValkey, script: ScriptTextT) -> None: ...
    async def __call__(
        self,
        keys: Sequence[KeyT] | None = None,
        args: Iterable[EncodableT] | None = None,
        client: AsyncValkey | None = None,
    ) -> Any: ...
    # NOTE: AsyncScript doesn't have get_encoder. Add it if someone asks for it.

class PubSubCommands(CommandsProtocol, Generic[_StrType]):
    def publish(self, channel: ChannelT, message: EncodableT, **kwargs) -> int: ...
    def spublish(self, shard_channel: ChannelT, message: EncodableT) -> int: ...
    def pubsub_channels(self, pattern: PatternT = "*", **kwargs) -> list[_StrType]: ...
    def pubsub_shardchannels(
        self, pattern: PatternT = "*", **kwargs
    ) -> list[_StrType]: ...
    def pubsub_numpat(self, **kwargs) -> int: ...
    def pubsub_numsub(
        self, *args: ChannelT, **kwargs
    ) -> list[tuple[_StrType, int]]: ...
    def pubsub_shardnumsub(
        self, *args: ChannelT, **kwargs
    ) -> list[tuple[_StrType, int]]: ...

class AsyncPubSubCommands(CommandsProtocol, Generic[_StrType]):
    async def publish(
        self, channel: ChannelT, message: EncodableT, **kwargs
    ) -> int: ...
    async def spublish(self, shard_channel: ChannelT, message: EncodableT) -> int: ...
    async def pubsub_channels(
        self, pattern: PatternT = "*", **kwargs
    ) -> list[_StrType]: ...
    async def pubsub_shardchannels(
        self, pattern: PatternT = "*", **kwargs
    ) -> list[_StrType]: ...
    async def pubsub_numpat(self, **kwargs) -> int: ...
    async def pubsub_numsub(
        self, *args: ChannelT, **kwargs
    ) -> list[tuple[_StrType, int]]: ...
    async def pubsub_shardnumsub(
        self, *args: ChannelT, **kwargs
    ) -> list[tuple[_StrType, int]]: ...

class ScriptCommands(CommandsProtocol):
    def eval(
        self, script: ScriptTextT, numkeys: int, *keys_and_args: _Value
    ) -> Any: ...
    def eval_ro(
        self, script: ScriptTextT, numkeys: int, *keys_and_args: _Value
    ) -> Any: ...
    def evalsha(self, sha: str, numkeys: int, *keys_and_args: _Value) -> Any: ...
    def evalsha_ro(self, sha: str, numkeys: int, *keys_and_args: _Value) -> Any: ...
    def script_exists(self, *args: str) -> list[bool]: ...
    def script_debug(self, *args) -> NoReturn: ...
    def script_flush(
        self, sync_type: Literal["SYNC"] | Literal["ASYNC"] | None = None
    ) -> Literal[True]: ...
    def script_kill(self) -> Literal[True]: ...
    def script_load(self, script: ScriptTextT) -> str: ...
    def register_script(self, script: ScriptTextT) -> Script: ...

class AsyncScriptCommands(CommandsProtocol):
    async def eval(
        self, script: ScriptTextT, numkeys: int, *keys_and_args: _Value
    ) -> Any: ...
    async def eval_ro(
        self, script: ScriptTextT, numkeys: int, *keys_and_args: _Value
    ) -> Any: ...
    async def evalsha(self, sha: str, numkeys: int, *keys_and_args: _Value) -> Any: ...
    async def evalsha_ro(
        self, sha: str, numkeys: int, *keys_and_args: _Value
    ) -> Any: ...
    async def script_exists(self, *args: str) -> list[bool]: ...
    async def script_debug(self, *args) -> NoReturn: ...
    async def script_flush(
        self, sync_type: Literal["SYNC"] | Literal["ASYNC"] | None = None
    ) -> Literal[True]: ...
    async def script_kill(self) -> Literal[True]: ...
    async def script_load(self, script: ScriptTextT) -> str: ...
    # register_script is not async because it doesn't actually do any IO
    def register_script(self, script: ScriptTextT) -> AsyncScript: ...

class GeoCommands(CommandsProtocol, Generic[_StrType]):
    def geoadd(
        self,
        name: _Key,
        values: Sequence[_Value],
        nx: bool = False,
        xx: bool = False,
        ch: bool = False,
    ) -> int: ...
    def geodist(
        self, name: _Key, place1: _Value, place2: _Value, unit: str | None = None
    ) -> float | None: ...
    def geohash(self, name: _Key, *values: _Value) -> list[str | _StrType | None]: ...
    def geopos(
        self, name: _Key, *values: _Value
    ) -> list[tuple[float, float] | list[float] | None]: ...
    @overload
    def georadius(
        self,
        name: _Key,
        longitude: float,
        latitude: float,
        radius: float,
        unit: str | None = None,
        withdist: bool = False,
        withcoord: bool = False,
        withhash: bool = False,
        count: int | None = None,
        sort: str | None = None,
        store: _Key = ...,
        store_dist: None = None,
        any: bool = False,
    ) -> int: ...
    @overload
    def georadius(
        self,
        name: _Key,
        longitude: float,
        latitude: float,
        radius: float,
        unit: str | None = None,
        withdist: bool = False,
        withcoord: bool = False,
        withhash: bool = False,
        count: int | None = None,
        sort: str | None = None,
        store: None = None,
        store_dist: _Key = ...,
        any: bool = False,
    ) -> int: ...
    def georadius(
        self,
        name: _Key,
        longitude: float,
        latitude: float,
        radius: float,
        unit: str | None = None,
        withdist: bool = False,
        withcoord: bool = False,
        withhash: bool = False,
        count: int | None = None,
        sort: str | None = None,
        store: _Key | None = None,
        store_dist: _Key | None = None,
        any: bool = False,
    ) -> _GeoSearchReplyT | int: ...
    @overload
    def georadiusbymember(
        self,
        name: _Key,
        member: _Value,
        radius: float,
        unit: str | None = None,
        withdist: bool = False,
        withcoord: bool = False,
        withhash: bool = False,
        count: int | None = None,
        sort: str | None = None,
        store: _Key = ...,
        store_dist: None = None,
        any: bool = False,
    ) -> int: ...
    @overload
    def georadiusbymember(
        self,
        name: _Key,
        member: _Value,
        radius: float,
        unit: str | None = None,
        withdist: bool = False,
        withcoord: bool = False,
        withhash: bool = False,
        count: int | None = None,
        sort: str | None = None,
        store: None = None,
        store_dist: _Key = ...,
        any: bool = False,
    ) -> int: ...
    def georadiusbymember(
        self,
        name: _Key,
        member: _Value,
        radius: float,
        unit: str | None = None,
        withdist: bool = False,
        withcoord: bool = False,
        withhash: bool = False,
        count: int | None = None,
        sort: str | None = None,
        store: _Key | None = None,
        store_dist: _Key | None = None,
        any: bool = False,
    ) -> _GeoSearchReplyT | int: ...
    def geosearch(
        self,
        name: _Key,
        member: _Value | None = None,
        longitude: float | None = None,
        latitude: float | None = None,
        unit: str = "m",
        radius: float | None = None,
        width: float | None = None,
        height: float | None = None,
        sort: str | None = None,
        count: int | None = None,
        any: bool = False,
        withcoord: bool = False,
        withdist: bool = False,
        withhash: bool = False,
    ) -> _GeoSearchReplyT: ...
    def geosearchstore(
        self,
        dest: _Key,
        name: _Key,
        member: _Value | None = None,
        longitude: float | None = None,
        latitude: float | None = None,
        unit: str = "m",
        radius: float | None = None,
        width: float | None = None,
        height: float | None = None,
        sort: str | None = None,
        count: int | None = None,
        any: bool = False,
        storedist: bool = False,
    ) -> int: ...

class AsyncGeoCommands(CommandsProtocol, Generic[_StrType]):
    async def geoadd(
        self,
        name: _Key,
        values: Sequence[_Value],
        nx: bool = False,
        xx: bool = False,
        ch: bool = False,
    ) -> int: ...
    async def geodist(
        self, name: _Key, place1: _Value, place2: _Value, unit: str | None = None
    ) -> float | None: ...
    async def geohash(
        self, name: _Key, *values: _Value
    ) -> list[str | _StrType | None]: ...
    async def geopos(
        self, name: _Key, *values: _Value
    ) -> list[tuple[float, float] | list[float] | None]: ...
    @overload
    async def georadius(
        self,
        name: _Key,
        longitude: float,
        latitude: float,
        radius: float,
        unit: str | None = None,
        withdist: bool = False,
        withcoord: bool = False,
        withhash: bool = False,
        count: int | None = None,
        sort: str | None = None,
        store: _Key = ...,
        store_dist: None = None,
        any: bool = False,
    ) -> int: ...
    @overload
    async def georadius(
        self,
        name: _Key,
        longitude: float,
        latitude: float,
        radius: float,
        unit: str | None = None,
        withdist: bool = False,
        withcoord: bool = False,
        withhash: bool = False,
        count: int | None = None,
        sort: str | None = None,
        store: None = None,
        store_dist: _Key = ...,
        any: bool = False,
    ) -> int: ...
    async def georadius(
        self,
        name: _Key,
        longitude: float,
        latitude: float,
        radius: float,
        unit: str | None = None,
        withdist: bool = False,
        withcoord: bool = False,
        withhash: bool = False,
        count: int | None = None,
        sort: str | None = None,
        store: _Key | None = None,
        store_dist: _Key | None = None,
        any: bool = False,
    ) -> _GeoSearchReplyT | int: ...
    @overload
    async def georadiusbymember(
        self,
        name: _Key,
        member: _Value,
        radius: float,
        unit: str | None = None,
        withdist: bool = False,
        withcoord: bool = False,
        withhash: bool = False,
        count: int | None = None,
        sort: str | None = None,
        store: _Key = ...,
        store_dist: None = None,
        any: bool = False,
    ) -> int: ...
    @overload
    async def georadiusbymember(
        self,
        name: _Key,
        member: _Value,
        radius: float,
        unit: str | None = None,
        withdist: bool = False,
        withcoord: bool = False,
        withhash: bool = False,
        count: int | None = None,
        sort: str | None = None,
        store: None = None,
        store_dist: _Key = ...,
        any: bool = False,
    ) -> int: ...
    async def georadiusbymember(
        self,
        name: _Key,
        member: _Value,
        radius: float,
        unit: str | None = None,
        withdist: bool = False,
        withcoord: bool = False,
        withhash: bool = False,
        count: int | None = None,
        sort: str | None = None,
        store: _Key | None = None,
        store_dist: _Key | None = None,
        any: bool = False,
    ) -> _GeoSearchReplyT | int: ...
    async def geosearch(
        self,
        name: _Key,
        member: _Value | None = None,
        longitude: float | None = None,
        latitude: float | None = None,
        unit: str = "m",
        radius: float | None = None,
        width: float | None = None,
        height: float | None = None,
        sort: str | None = None,
        count: int | None = None,
        any: bool = False,
        withcoord: bool = False,
        withdist: bool = False,
        withhash: bool = False,
    ) -> _GeoSearchReplyT: ...
    async def geosearchstore(
        self,
        dest: _Key,
        name: _Key,
        member: _Value | None = None,
        longitude: float | None = None,
        latitude: float | None = None,
        unit: str = "m",
        radius: float | None = None,
        width: float | None = None,
        height: float | None = None,
        sort: str | None = None,
        count: int | None = None,
        any: bool = False,
        storedist: bool = False,
    ) -> int: ...

class ModuleCommands(CommandsProtocol, Generic[_StrType]):
    def module_load(self, path: str, *args: str) -> Literal[True]: ...
    # NOTE: module_loadex misses the parsing callback in the implementation,
    # so the return type is a string. This seems to be an oversight in the
    # implementation. It needs to be handled the same way as module_load
    def module_loadex(
        self, path: str, options: list[str] | None = None, args: list[str] | None = None
    ) -> _StrType: ...
    def module_unload(self, name: str) -> Literal[True]: ...
    def module_list(self) -> list[dict[Any, Any]]: ...
    def command_info(self) -> NoReturn: ...
    def command_count(self) -> int: ...
    def command_getkeys(self, *args: str) -> list[str | _StrType]: ...
    def command(self) -> dict[str, dict[str, Any]]: ...

class AsyncModuleCommands(CommandsProtocol, Generic[_StrType]):
    async def module_load(self, path: str, *args: str) -> Literal[True]: ...
    # NOTE: module_loadex misses the parsing callback in the implementation,
    # so the return type is a string. This seems to be an oversight in the
    # implementation. It needs to be handled the same way as module_load
    async def module_loadex(
        self, path: str, options: list[str] | None = None, args: list[str] | None = None
    ) -> _StrType: ...
    async def module_unload(self, name: str) -> Literal[True]: ...
    async def module_list(self) -> list[dict[Any, Any]]: ...
    async def command_info(self) -> NoReturn: ...
    async def command_count(self) -> int: ...
    async def command_getkeys(self, *args: str) -> list[str | _StrType]: ...
    async def command(self) -> dict[str, dict[str, Any]]: ...

class ClusterCommands(CommandsProtocol):
    def cluster(self, cluster_arg: str, *args: _Value, **kwargs: Any) -> Any: ...
    def readwrite(self, **kwargs: Any) -> Literal[True]: ...
    def readonly(self, **kwargs: Any) -> Literal[True]: ...

class AsyncClusterCommands(CommandsProtocol):
    async def cluster(self, cluster_arg: str, *args: _Value, **kwargs: Any) -> Any: ...
    async def readwrite(self, **kwargs: Any) -> Literal[True]: ...
    async def readonly(self, **kwargs: Any) -> Literal[True]: ...

class FunctionCommands(CommandsProtocol, Generic[_StrType]):
    def function_load(self, code: str, replace: bool | None = False) -> _StrType: ...
    def function_delete(self, library: str) -> Literal[True]: ...
    def function_flush(self, mode: str = "SYNC") -> Literal[True]: ...
    def function_list(
        self, library: str | None = "*", withcode: bool | None = False
    ) -> list[Any]: ...
    def fcall(self, function: str, numkeys: int, *keys_and_args: _Value) -> Any: ...
    def fcall_ro(self, function: str, numkeys: int, *keys_and_args: _Value) -> Any: ...
    def function_dump(self) -> bytes: ...
    def function_restore(
        self, payload: EncodableT, policy: str | None = "APPEND"
    ) -> Literal[True]: ...
    def function_kill(self) -> _StrType: ...
    def function_stats(self) -> list[Any] | dict[_StrType, Any]: ...

class AsyncFunctionCommands(CommandsProtocol, Generic[_StrType]):
    async def function_load(
        self, code: str, replace: bool | None = False
    ) -> _StrType: ...
    async def function_delete(self, library: str) -> Literal[True]: ...
    async def function_flush(self, mode: str = "SYNC") -> Literal[True]: ...
    async def function_list(
        self, library: str | None = "*", withcode: bool | None = False
    ) -> list[Any]: ...
    async def fcall(
        self, function: str, numkeys: int, *keys_and_args: _Value
    ) -> Any: ...
    async def fcall_ro(
        self, function: str, numkeys: int, *keys_and_args: _Value
    ) -> Any: ...
    async def function_dump(self) -> bytes: ...
    async def function_restore(
        self, payload: EncodableT, policy: str | None = "APPEND"
    ) -> Literal[True]: ...
    async def function_kill(self) -> _StrType: ...
    async def function_stats(self) -> list[Any] | dict[_StrType, Any]: ...

class GearsCommands(CommandsProtocol, Generic[_StrType]):
    def tfunction_load(
        self, lib_code: str, replace: bool = False, config: str | None = None
    ) -> _StrType: ...
    def tfunction_delete(self, lib_name: str) -> _StrType: ...
    def tfunction_list(
        self, with_code: bool = False, verbose: int = 0, lib_name: str | None = None
    ) -> Any: ...
    def tfcall(
        self,
        lib_name: str,
        func_name: str,
        keys: Sequence[_Key] | None = None,
        *args: _Value,
    ) -> Any: ...
    def tfcall_async(
        self,
        lib_name: str,
        func_name: str,
        keys: Sequence[_Key] | None = None,
        *args: _Value,
    ) -> Any: ...

class AsyncGearsCommands(CommandsProtocol, Generic[_StrType]):
    async def tfunction_load(
        self, lib_code: str, replace: bool = False, config: str | None = None
    ) -> _StrType: ...
    async def tfunction_delete(self, lib_name: str) -> _StrType: ...
    async def tfunction_list(
        self, with_code: bool = False, verbose: int = 0, lib_name: str | None = None
    ) -> Any: ...
    async def tfcall(
        self,
        lib_name: str,
        func_name: str,
        keys: Sequence[_Key] | None = None,
        *args: _Value,
    ) -> Any: ...
    async def tfcall_async(
        self,
        lib_name: str,
        func_name: str,
        keys: Sequence[_Key] | None = None,
        *args: _Value,
    ) -> Any: ...

class DataAccessCommands(
    BasicKeyCommands[_StrType],
    HyperlogCommands,
    HashCommands[_StrType],
    GeoCommands[_StrType],
    ListCommands[_StrType],
    ScanCommands[_StrType],
    SetCommands[_StrType],
    StreamCommands[_StrType],
    SortedSetCommands[_StrType],
    Generic[_StrType],
): ...
class AsyncDataAccessCommands(
    AsyncBasicKeyCommands[_StrType],
    AsyncHyperlogCommands,
    AsyncHashCommands[_StrType],
    AsyncGeoCommands[_StrType],
    AsyncListCommands[_StrType],
    AsyncScanCommands[_StrType],
    AsyncSetCommands[_StrType],
    AsyncStreamCommands[_StrType],
    AsyncSortedSetCommands[_StrType],
    Generic[_StrType],
): ...
class CoreCommands(
    ACLCommands[_StrType],
    ClusterCommands,
    DataAccessCommands[_StrType],
    ManagementCommands[_StrType],
    ModuleCommands[_StrType],
    PubSubCommands[_StrType],
    ScriptCommands,
    FunctionCommands[_StrType],
    GearsCommands[_StrType],
    Generic[_StrType],
): ...
class AsyncCoreCommands(
    AsyncACLCommands[_StrType],
    AsyncClusterCommands,
    AsyncDataAccessCommands[_StrType],
    AsyncManagementCommands[_StrType],
    AsyncModuleCommands[_StrType],
    AsyncPubSubCommands[_StrType],
    AsyncScriptCommands,
    AsyncFunctionCommands[_StrType],
    AsyncGearsCommands[_StrType],
    Generic[_StrType],
): ...
