from datetime import datetime
from typing import (
    Any,
    Awaitable,
    Callable,
    Generic,
    Iterable,
    Iterator,
    Literal,
    Mapping,
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

from ..client import _CommandOptions, _Key, _Value

_ScoreCastFuncReturn = TypeVar("_ScoreCastFuncReturn")
_StrType = TypeVar("_StrType", bound=str | bytes)

class ACLCommands(CommandsProtocol):
    def acl_cat(self, category: str | None = None, **kwargs) -> list[str]: ...
    def acl_deluser(self, *username: str, **kwargs) -> int: ...
    def acl_dryrun(self, username, *args, **kwargs): ...
    def acl_genpass(self, bits: int | None = None, **kwargs) -> str: ...
    def acl_getuser(self, username: str, **kwargs) -> dict[str, Any] | None: ...
    def acl_help(self, **kwargs) -> list[str]: ...
    def acl_list(self, **kwargs) -> list[str]: ...
    def acl_log(self, count: int | None = None, **kwargs) -> list: ...
    def acl_log_reset(self, **kwargs) -> bool: ...
    def acl_load(self, **kwargs) -> bool: ...
    def acl_save(self, **kwargs): ...
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
    ) -> bool: ...
    def acl_users(self, **kwargs) -> list[str]: ...
    def acl_whoami(self, **kwargs) -> str: ...

class AsyncACLCommands(CommandsProtocol):
    async def acl_cat(self, category: str | None = None, **kwargs) -> list[str]: ...
    async def acl_deluser(self, *username: str, **kwargs) -> int: ...
    async def acl_dryrun(self, username, *args, **kwargs): ...
    async def acl_genpass(self, bits: int | None = None, **kwargs) -> str: ...
    async def acl_getuser(self, username: str, **kwargs) -> dict[str, Any] | None: ...
    async def acl_help(self, **kwargs) -> list[str]: ...
    async def acl_list(self, **kwargs) -> list[str]: ...
    async def acl_log(self, count: int | None = None, **kwargs) -> list: ...
    async def acl_log_reset(self, **kwargs) -> bool: ...
    async def acl_load(self, **kwargs) -> bool: ...
    async def acl_save(self, **kwargs): ...
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
    ) -> bool: ...
    async def acl_users(self, **kwargs) -> list[str]: ...
    async def acl_whoami(self, **kwargs) -> str: ...

class ManagementCommands(CommandsProtocol):
    def auth(self, password: str, username: str | None = None, **kwargs): ...
    def bgrewriteaof(self, **kwargs): ...
    def bgsave(self, schedule: bool = True, **kwargs): ...
    def role(self): ...
    def client_kill(self, address: str, **kwargs) -> bool: ...
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
    ): ...
    def client_info(self, **kwargs) -> dict[str, Any]: ...
    def client_list(
        self, _type: str | None = None, client_id: list[EncodableT] = [], **kwargs
    ) -> list[dict[str, Any]]: ...
    def client_getname(self, **kwargs) -> str | None: ...
    def client_getredir(self, **kwargs): ...
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
    def client_trackinginfo(self, **kwargs) -> list[Any]: ...
    def client_setname(self, name: str, **kwargs) -> bool: ...
    def client_setinfo(self, attr: str, value: str, **kwargs) -> bool: ...
    def client_unblock(self, client_id: int, error: bool = False, **kwargs) -> bool: ...
    def client_pause(self, timeout: int, all: bool = True, **kwargs) -> bool: ...
    def client_unpause(self, **kwargs): ...
    def client_no_evict(self, mode: str) -> str: ...
    def client_no_touch(self, mode: str) -> str: ...
    def command(self, **kwargs): ...
    def command_info(self, **kwargs) -> None: ...
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
    ) -> bool: ...
    def config_resetstat(self, **kwargs) -> bool: ...
    def config_rewrite(self, **kwargs): ...
    def dbsize(self, **kwargs) -> int: ...
    def debug_object(self, key: KeyT, **kwargs) -> dict[str, str | int]: ...
    def debug_segfault(self, **kwargs) -> None: ...
    def echo(self, value: EncodableT, **kwargs) -> bytes: ...
    def flushall(self, asynchronous: bool = False, **kwargs) -> bool: ...
    def flushdb(self, asynchronous: bool = False, **kwargs) -> bool: ...
    def sync(self): ...
    def psync(self, replicationid: str, offset: int): ...
    def swapdb(self, first: int, second: int, **kwargs) -> bool: ...
    def select(self, index: int, **kwargs) -> bool: ...
    def info(
        self, section: str | None = None, *args: list[str], **kwargs
    ) -> dict[str, Any]: ...
    def lastsave(self, **kwargs) -> datetime | None: ...
    def latency_doctor(self) -> None: ...
    def latency_graph(self) -> None: ...
    def lolwut(self, *version_numbers: str | float, **kwargs) -> bytes: ...
    def reset(self) -> str: ...
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
    def memory_usage(self, key: KeyT, samples: int | None = None, **kwargs): ...
    def memory_purge(self, **kwargs) -> bool: ...
    def latency_histogram(self, *args) -> None: ...
    def latency_history(self, event: str): ...
    def latency_latest(self): ...
    def latency_reset(self, *events: str): ...
    def ping(self, **kwargs) -> bool: ...
    def quit(self, **kwargs) -> bool: ...
    def replicaof(self, *args, **kwargs): ...
    def save(self, **kwargs) -> bool: ...
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
    def slowlog_reset(self, **kwargs) -> bool: ...
    def time(self, **kwargs) -> tuple[int, int]: ...
    def wait(self, num_replicas: int, timeout: int, **kwargs) -> int: ...
    def waitaof(self, num_local: int, num_replicas: int, timeout: int, **kwargs): ...
    def hello(self) -> None: ...
    def failover(self) -> None: ...

class AsyncManagementCommands(CommandsProtocol):
    async def auth(self, password: str, username: str | None = None, **kwargs): ...
    async def bgrewriteaof(self, **kwargs): ...
    async def bgsave(self, schedule: bool = True, **kwargs): ...
    async def role(self): ...
    async def client_kill(self, address: str, **kwargs) -> bool: ...
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
    ): ...
    async def client_info(self, **kwargs) -> dict[str, Any]: ...
    async def client_list(
        self, _type: str | None = None, client_id: list[EncodableT] = [], **kwargs
    ) -> list[dict[str, Any]]: ...
    async def client_getname(self, **kwargs) -> str | None: ...
    async def client_getredir(self, **kwargs): ...
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
    async def client_trackinginfo(self, **kwargs) -> list[Any]: ...
    async def client_setname(self, name: str, **kwargs) -> bool: ...
    async def client_setinfo(self, attr: str, value: str, **kwargs) -> bool: ...
    async def client_unblock(
        self, client_id: int, error: bool = False, **kwargs
    ) -> bool: ...
    async def client_pause(self, timeout: int, all: bool = True, **kwargs) -> bool: ...
    async def client_unpause(self, **kwargs): ...
    async def client_no_evict(self, mode: str) -> str: ...
    async def client_no_touch(self, mode: str) -> str: ...
    async def command(self, **kwargs): ...
    async def command_info(self, **kwargs) -> None: ...
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
    ) -> bool: ...
    async def config_resetstat(self, **kwargs) -> bool: ...
    async def config_rewrite(self, **kwargs): ...
    async def dbsize(self, **kwargs) -> int: ...
    async def debug_object(self, key: KeyT, **kwargs) -> dict[str, str | int]: ...
    async def debug_segfault(self, **kwargs) -> None: ...
    async def echo(self, value: EncodableT, **kwargs) -> bytes: ...
    async def flushall(self, asynchronous: bool = False, **kwargs) -> bool: ...
    async def flushdb(self, asynchronous: bool = False, **kwargs) -> bool: ...
    async def sync(self): ...
    async def psync(self, replicationid: str, offset: int): ...
    async def swapdb(self, first: int, second: int, **kwargs) -> bool: ...
    async def select(self, index: int, **kwargs) -> bool: ...
    async def info(
        self, section: str | None = None, *args: list[str], **kwargs
    ) -> dict[str, Any]: ...
    async def lastsave(self, **kwargs) -> datetime | None: ...
    async def latency_doctor(self) -> None: ...
    async def latency_graph(self) -> None: ...
    async def lolwut(self, *version_numbers: str | float, **kwargs) -> bytes: ...
    async def reset(self) -> str: ...
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
    async def memory_usage(self, key: KeyT, samples: int | None = None, **kwargs): ...
    async def memory_purge(self, **kwargs) -> bool: ...
    async def latency_histogram(self, *args) -> None: ...
    async def latency_history(self, event: str): ...
    async def latency_latest(self): ...
    async def latency_reset(self, *events: str): ...
    async def ping(self, **kwargs) -> bool: ...
    async def quit(self, **kwargs) -> bool: ...
    async def replicaof(self, *args, **kwargs): ...
    async def save(self, **kwargs) -> bool: ...
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
    async def slowlog_reset(self, **kwargs) -> bool: ...
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
        client: Valkey | AsyncValkey,
        key: str,
        default_overflow: str | None = None,
    ) -> None: ...
    def reset(self) -> None: ...
    def overflow(self, overflow: str): ...
    def incrby(
        self,
        fmt: str,
        offset: BitfieldOffsetT,
        increment: int,
        overflow: str | None = None,
    ): ...
    def get(self, fmt: str, offset: BitfieldOffsetT): ...
    def set(self, fmt: str, offset: BitfieldOffsetT, value: int): ...
    @property
    def command(self): ...
    def execute(self): ...

class BasicKeyCommands(Generic[_StrType]):
    def append(self, key: KeyT, value: EncodableT): ...
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
        items: list | None = None,
    ): ...
    def bitop(self, operation: str, dest: KeyT, *keys: KeyT): ...
    def bitpos(
        self,
        key: KeyT,
        bit: int,
        start: int | None = None,
        end: int | None = None,
        mode: str | None = None,
    ): ...
    def copy(
        self,
        source: str,
        destination: str,
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
    def expiretime(self, key: str) -> int: ...
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
    ): ...
    def __getitem__(self, name: KeyT): ...
    def getbit(self, name: KeyT, offset: int) -> int: ...
    def getrange(self, key: KeyT, start: int, end: int): ...
    def getset(self, name: KeyT, value: EncodableT) -> _StrType | None: ...
    def incr(self, name: KeyT, amount: int = 1) -> int: ...
    def incrby(self, name: KeyT, amount: int = 1) -> int: ...
    def incrbyfloat(self, name: KeyT, amount: float = 1.0) -> float: ...
    def keys(self, pattern: PatternT = "*", **kwargs) -> list[_StrType]: ...
    def lmove(
        self, first_list: str, second_list: str, src: str = "LEFT", dest: str = "RIGHT"
    ) -> _Value: ...
    def blmove(
        self,
        first_list: str,
        second_list: str,
        timeout: int,
        src: str = "LEFT",
        dest: str = "RIGHT",
    ) -> _Value | None: ...
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
    def pexpiretime(self, key: str) -> int: ...
    def psetex(self, name: KeyT, time_ms: ExpiryT, value: EncodableT) -> bool: ...
    def pttl(self, name: KeyT) -> int: ...
    def hrandfield(
        self, key: str, count: int | None = None, withvalues: bool = False
    ): ...
    def randomkey(self, **kwargs) -> bytes: ...
    def rename(self, src: KeyT, dst: KeyT) -> bool: ...
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
    ): ...
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
    ) -> bool | _StrType: ...
    def __setitem__(self, name: KeyT, value: EncodableT) -> None: ...
    def setbit(self, name: KeyT, offset: int, value: int) -> int: ...
    def setex(self, name: KeyT, time: ExpiryT, value: EncodableT) -> bool: ...
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
    def substr(self, name: KeyT, start: int, end: int = -1) -> str: ...
    def touch(self, *args: KeyT): ...
    def ttl(self, name: KeyT) -> int: ...
    def type(self, name: KeyT) -> bytes: ...
    def watch(self, *names: KeyT) -> bool: ...
    def unwatch(self) -> bool: ...
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

class AsyncBasicKeyCommands(Generic[_StrType]):
    async def append(self, key: KeyT, value: EncodableT): ...
    async def bitcount(
        self,
        key: KeyT,
        start: int | None = None,
        end: int | None = None,
        mode: str | None = None,
    ) -> int: ...
    async def bitfield(
        self, key: KeyT, default_overflow: str | None = None
    ) -> BitFieldOperation: ...
    async def bitfield_ro(
        self,
        key: KeyT,
        encoding: str,
        offset: BitfieldOffsetT,
        items: list | None = None,
    ): ...
    async def bitop(self, operation: str, dest: KeyT, *keys: KeyT): ...
    async def bitpos(
        self,
        key: KeyT,
        bit: int,
        start: int | None = None,
        end: int | None = None,
        mode: str | None = None,
    ): ...
    async def copy(
        self,
        source: str,
        destination: str,
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
    async def expiretime(self, key: str) -> int: ...
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
    ): ...
    async def __getitem__(self, name: KeyT): ...
    async def getbit(self, name: KeyT, offset: int) -> int: ...
    async def getrange(self, key: KeyT, start: int, end: int): ...
    async def getset(self, name: KeyT, value: EncodableT) -> _StrType | None: ...
    async def incr(self, name: KeyT, amount: int = 1) -> int: ...
    async def incrby(self, name: KeyT, amount: int = 1) -> int: ...
    async def incrbyfloat(self, name: KeyT, amount: float = 1.0) -> float: ...
    async def keys(self, pattern: PatternT = "*", **kwargs) -> list[_StrType]: ...
    async def lmove(
        self, first_list: str, second_list: str, src: str = "LEFT", dest: str = "RIGHT"
    ) -> _Value: ...
    async def blmove(
        self,
        first_list: str,
        second_list: str,
        timeout: int,
        src: str = "LEFT",
        dest: str = "RIGHT",
    ) -> _Value | None: ...
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
    async def pexpiretime(self, key: str) -> int: ...
    async def psetex(self, name: KeyT, time_ms: ExpiryT, value: EncodableT) -> bool: ...
    async def pttl(self, name: KeyT) -> int: ...
    async def hrandfield(
        self, key: str, count: int | None = None, withvalues: bool = False
    ): ...
    async def randomkey(self, **kwargs) -> bytes: ...
    async def rename(self, src: KeyT, dst: KeyT) -> bool: ...
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
    ): ...
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
    ) -> bool | _StrType: ...
    async def __setitem__(self, name: KeyT, value: EncodableT) -> None: ...
    async def setbit(self, name: KeyT, offset: int, value: int) -> int: ...
    async def setex(self, name: KeyT, time: ExpiryT, value: EncodableT) -> bool: ...
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
    async def substr(self, name: KeyT, start: int, end: int = -1) -> str: ...
    async def touch(self, *args: KeyT): ...
    async def ttl(self, name: KeyT) -> int: ...
    async def type(self, name: KeyT) -> bytes: ...
    async def watch(self, *names: KeyT) -> bool: ...
    async def unwatch(self) -> bool: ...
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

class ListCommands(Generic[_StrType]):
    @overload
    def blpop(
        self, keys: _Value | Iterable[_Value], timeout: Literal[0]
    ) -> tuple[_StrType, _StrType]: ...
    @overload
    def blpop(
        self, keys: _Value | Iterable[_Value], timeout: float
    ) -> tuple[_StrType, _StrType] | None: ...
    @overload
    def brpop(
        self, keys: _Value | Iterable[_Value], timeout: Literal[0]
    ) -> tuple[_StrType, _StrType]: ...
    @overload
    def brpop(
        self, keys: _Value | Iterable[_Value], timeout: float
    ) -> tuple[_StrType, _StrType] | None: ...
    @overload
    def brpoplpush(self, src: _Value, dst: _Value, timeout: Literal[0]) -> _StrType: ...
    @overload
    def brpoplpush(
        self, src: _Value, dst: _Value, timeout: float
    ) -> _StrType | None: ...
    @overload
    def blmpop(
        self,
        timeout: Literal[0],
        numkeys: int,
        *keys: _Value,
        direction: Literal["LEFT"] | Literal["RIGHT"],
        count: int = 1,
    ) -> tuple[_StrType, list[_StrType]]: ...
    @overload
    def blmpop(
        self,
        timeout: float,
        numkeys: int,
        *keys: _Value,
        direction: Literal["LEFT"] | Literal["RIGHT"],
        count: int = 1,
    ) -> tuple[_StrType, list[_StrType]] | None: ...
    def lmpop(
        self,
        numkeys: int,
        *keys: _Value,
        direction: Literal["LEFT"] | Literal["RIGHT"],
        count: int = 1,
    ) -> tuple[_StrType, list[_StrType]] | None: ...
    def lindex(self, name: _Value, index: int) -> _StrType | None: ...
    def linsert(
        self,
        name: _Value,
        where: Literal["BEFORE"] | Literal["AFTER"],
        refvalue: _Value,
        value: _Value,
    ) -> int: ...
    def llen(self, name: _Value) -> int: ...
    @overload
    def lpop(self, name: _Value) -> _StrType | None: ...
    @overload
    def lpop(self, name: _Value, count: int) -> list[_StrType] | None: ...
    def lpush(self, name: _Value, *values: _Value) -> int: ...
    def lpushx(self, name: _Value, *values: _Value) -> int: ...
    def lrange(self, name: _Value, start: int, end: int) -> list[_StrType]: ...
    def lrem(self, name: _Value, count: int, value: _Value) -> int: ...
    def lset(self, name: _Value, index: int, value: _Value) -> bool: ...
    def ltrim(self, name: _Value, start: int, end: int) -> bool: ...
    @overload
    def rpop(self, name: _Value) -> _StrType | None: ...
    @overload
    def rpop(self, name: _Value, count: int) -> list[_StrType] | None: ...
    def rpoplpush(self, src: _Value, dst: _Value) -> _StrType: ...
    def rpush(self, name: _Value, *values: _Value) -> int: ...
    def rpushx(self, name: _Value, *values: _Value) -> int: ...
    @overload
    def lpos(
        self,
        name: _Value,
        rank: int | None = None,
        count: None = None,
        maxlen: int | None = None,
    ) -> _StrType | None: ...
    @overload
    def lpos(
        self,
        name: _Value,
        rank: int | None = None,
        *,
        count: int,
        maxlen: int | None = None,
    ) -> list[_StrType] | None: ...
    @overload
    def lpos(
        self,
        name: _Value,
        value: _Value,
        rank: int | None,
        count: int,
        maxlen: int | None = None,
    ) -> list[_StrType] | None: ...
    @overload
    def sort(
        self,
        name: _Value,
        start: int | None = None,
        num: int | None = None,
        by: _Value | None = None,
        get: _Value | Sequence[_Value] | None = None,
        desc: bool = False,
        alpha: bool = False,
        store: None = None,
        groups: bool | None = False,
    ) -> list[_StrType]: ...
    @overload
    def sort(
        self,
        name: _Value,
        start: int | None = None,
        num: int | None = None,
        by: _Value | None = None,
        get: _Value | Sequence[_Value] | None = None,
        desc: bool = False,
        alpha: bool = False,
        *,
        store: _Value,
        groups: bool = False,
    ) -> int: ...
    @overload
    def sort(
        self,
        name: _Value,
        start: int | None,
        num: int | None,
        by: _Value | None,
        get: _Value | Sequence[_Value] | None,
        desc: bool,
        alpha: bool,
        store: _Value,
        groups: bool = False,
    ) -> int: ...
    def sort_ro(
        self,
        key: _Value,
        start: int | None = None,
        num: int | None = None,
        by: str | None = None,
        get: list[str] | None = None,
        desc: bool = False,
        alpha: bool = False,
    ) -> list[_StrType]: ...

class AsyncListCommands(Generic[_StrType]):
    @overload
    async def blpop(
        self, keys: _Value | Iterable[_Value], timeout: Literal[0]
    ) -> tuple[_StrType, _StrType]: ...
    @overload
    async def blpop(
        self, keys: _Value | Iterable[_Value], timeout: float
    ) -> tuple[_StrType, _StrType] | None: ...
    @overload
    async def brpop(
        self, keys: _Value | Iterable[_Value], timeout: Literal[0]
    ) -> tuple[_StrType, _StrType]: ...
    @overload
    async def brpop(
        self, keys: _Value | Iterable[_Value], timeout: float
    ) -> tuple[_StrType, _StrType] | None: ...
    @overload
    async def brpoplpush(
        self, src: _Value, dst: _Value, timeout: Literal[0]
    ) -> _StrType: ...
    @overload
    async def brpoplpush(
        self, src: _Value, dst: _Value, timeout: float
    ) -> _StrType | None: ...
    @overload
    async def blmpop(
        self,
        timeout: Literal[0],
        numkeys: int,
        *keys: _Value,
        direction: Literal["LEFT"] | Literal["RIGHT"],
        count: int = 1,
    ) -> tuple[_StrType, list[_StrType]]: ...
    @overload
    async def blmpop(
        self,
        timeout: float,
        numkeys: int,
        *keys: _Value,
        direction: Literal["LEFT"] | Literal["RIGHT"],
        count: int = 1,
    ) -> tuple[_StrType, list[_StrType]] | None: ...
    async def lmpop(
        self,
        numkeys: int,
        *keys: _Value,
        direction: Literal["LEFT"] | Literal["RIGHT"],
        count: int = 1,
    ) -> tuple[_StrType, list[_StrType]] | None: ...
    async def lindex(self, name: _Value, index: int) -> _StrType | None: ...
    async def linsert(
        self,
        name: _Value,
        where: Literal["BEFORE"] | Literal["AFTER"],
        refvalue: _Value,
        value: _Value,
    ) -> int: ...
    async def llen(self, name: _Value) -> int: ...
    @overload
    async def lpop(self, name: _Value) -> _StrType | None: ...
    @overload
    async def lpop(self, name: _Value, count: int) -> list[_StrType] | None: ...
    async def lpush(self, name: _Value, *values: _Value) -> int: ...
    async def lpushx(self, name: _Value, *values: _Value) -> int: ...
    async def lrange(self, name: _Value, start: int, end: int) -> list[_StrType]: ...
    async def lrem(self, name: _Value, count: int, value: _Value) -> int: ...
    async def lset(self, name: _Value, index: int, value: _Value) -> bool: ...
    async def ltrim(self, name: _Value, start: int, end: int) -> bool: ...
    @overload
    async def rpop(self, name: _Value) -> _StrType | None: ...
    @overload
    async def rpop(self, name: _Value, count: int) -> list[_StrType] | None: ...
    async def rpoplpush(self, src: _Value, dst: _Value) -> _StrType: ...
    async def rpush(self, name: _Value, *values: _Value) -> int: ...
    async def rpushx(self, name: _Value, *values: _Value) -> int: ...
    @overload
    async def lpos(
        self,
        name: _Value,
        rank: int | None = None,
        count: None = None,
        maxlen: int | None = None,
    ) -> _StrType | None: ...
    @overload
    async def lpos(
        self,
        name: _Value,
        rank: int | None = None,
        *,
        count: int,
        maxlen: int | None = None,
    ) -> list[_StrType] | None: ...
    @overload
    async def lpos(
        self,
        name: _Value,
        value: _Value,
        rank: int | None,
        count: int,
        maxlen: int | None = None,
    ) -> list[_StrType] | None: ...
    @overload
    async def sort(
        self,
        name: _Value,
        start: int | None = None,
        num: int | None = None,
        by: _Value | None = None,
        get: _Value | Sequence[_Value] | None = None,
        desc: bool = False,
        alpha: bool = False,
        store: None = None,
        groups: bool | None = False,
    ) -> list[_StrType]: ...
    @overload
    async def sort(
        self,
        name: _Value,
        start: int | None = None,
        num: int | None = None,
        by: _Value | None = None,
        get: _Value | Sequence[_Value] | None = None,
        desc: bool = False,
        alpha: bool = False,
        *,
        store: _Value,
        groups: bool = False,
    ) -> int: ...
    @overload
    async def sort(
        self,
        name: _Value,
        start: int | None,
        num: int | None,
        by: _Value | None,
        get: _Value | Sequence[_Value] | None,
        desc: bool,
        alpha: bool,
        store: _Value,
        groups: bool = False,
    ) -> int: ...
    async def sort_ro(
        self,
        key: _Value,
        start: int | None = None,
        num: int | None = None,
        by: str | None = None,
        get: list[str] | None = None,
        desc: bool = False,
        alpha: bool = False,
    ) -> list[_StrType]: ...

class ScanCommands(Generic[_StrType]):
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
        name: _Value,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
    ) -> tuple[int, list[_StrType]]: ...
    def sscan_iter(
        self, name: _Value, match: _Key | None = None, count: int | None = None
    ) -> Iterator[_StrType]: ...
    def hscan(
        self,
        name: _Value,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
        no_values: bool | None = None,
    ) -> tuple[int, dict[_StrType, _StrType]]: ...
    def hscan_iter(
        self,
        name: _Value,
        match: _Key | None = None,
        count: int | None = None,
        no_values: bool | None = None,
    ) -> Iterator[tuple[_StrType, _StrType]]: ...
    @overload
    def zscan(
        self,
        name: _Value,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
    ) -> tuple[int, list[tuple[_StrType, float]]]: ...
    @overload
    def zscan(
        self,
        name: _Value,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
        *,
        score_cast_func: Callable[[_StrType], _ScoreCastFuncReturn],
    ) -> tuple[int, list[tuple[_StrType, _ScoreCastFuncReturn]]]: ...
    @overload
    def zscan(
        self,
        name: _Value,
        cursor: int,
        match: _Key | None,
        count: int | None,
        score_cast_func: Callable[[_StrType], _ScoreCastFuncReturn],
    ) -> tuple[int, list[tuple[_StrType, _ScoreCastFuncReturn]]]: ...
    @overload
    def zscan_iter(
        self, name: _Value, match: _Key | None = None, count: int | None = None
    ) -> Iterator[tuple[_StrType, float]]: ...
    @overload
    def zscan_iter(
        self,
        name: _Value,
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

class AsyncScanCommands(Generic[_StrType]):
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
    ) -> Iterator[_StrType]: ...
    async def sscan(
        self,
        name: _Value,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
    ) -> tuple[int, list[_StrType]]: ...
    async def sscan_iter(
        self, name: _Value, match: _Key | None = None, count: int | None = None
    ) -> Iterator[_StrType]: ...
    async def hscan(
        self,
        name: _Value,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
        no_values: bool | None = None,
    ) -> tuple[int, dict[_StrType, _StrType]]: ...
    async def hscan_iter(
        self,
        name: _Value,
        match: _Key | None = None,
        count: int | None = None,
        no_values: bool | None = None,
    ) -> Iterator[tuple[_StrType, _StrType]]: ...
    @overload
    async def zscan(
        self,
        name: _Value,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
    ) -> tuple[int, list[tuple[_StrType, float]]]: ...
    @overload
    async def zscan(
        self,
        name: _Value,
        cursor: int = 0,
        match: _Key | None = None,
        count: int | None = None,
        *,
        score_cast_func: Callable[[_StrType], _ScoreCastFuncReturn],
    ) -> tuple[int, list[tuple[_StrType, _ScoreCastFuncReturn]]]: ...
    @overload
    async def zscan(
        self,
        name: _Value,
        cursor: int,
        match: _Key | None,
        count: int | None,
        score_cast_func: Callable[[_StrType], _ScoreCastFuncReturn],
    ) -> tuple[int, list[tuple[_StrType, _ScoreCastFuncReturn]]]: ...
    @overload
    async def zscan_iter(
        self, name: _Value, match: _Key | None = None, count: int | None = None
    ) -> Iterator[tuple[_StrType, float]]: ...
    @overload
    async def zscan_iter(
        self,
        name: _Value,
        match: _Key | None = None,
        count: int | None = None,
        *,
        score_cast_func: Callable[[_StrType], _ScoreCastFuncReturn],
    ) -> Iterator[tuple[_StrType, _ScoreCastFuncReturn]]: ...
    @overload
    async def zscan_iter(
        self,
        name: KeyT,
        match: PatternT | None,
        count: int | None,
        score_cast_func: Callable[[_StrType], _ScoreCastFuncReturn],
    ) -> Iterator[tuple[_StrType, _ScoreCastFuncReturn]]: ...

class SetCommands(Generic[_StrType]):
    def sadd(self, name: _Value, *values: _Value) -> int: ...
    def scard(self, name: _Value) -> int: ...
    def sdiff(
        self, keys: _Value | Iterable[_Value], *args: _Value
    ) -> list[_StrType]: ...
    def sdiffstore(
        self, dest: _Value, keys: _Value | Iterable[_Value], *args: _Value
    ) -> int: ...
    def sinter(
        self, keys: _Value | Iterable[_Value], *args: _Value
    ) -> list[_StrType]: ...
    def sintercard(
        self, numkeys: int, keys: Iterable[_Value], limit: int = 0
    ) -> int: ...
    def sinterstore(
        self, dest: _Value, keys: _Value | Iterable[_Value], *args: _Value
    ) -> int: ...
    def sismember(self, name: _Value, value: _Value) -> Literal[0] | Literal[1]: ...
    def smembers(self, name: _Value) -> list[_StrType]: ...
    def smismember(
        self, name: _Value, values: _Value | Iterable[_Value], *args: _Value
    ) -> list[Literal[0] | Literal[1]]: ...
    def smove(self, src: _Value, dst: _Value, value: _Value) -> bool: ...
    @overload
    def spop(self, name: _Value, count: None = None) -> _StrType | None: ...
    @overload
    def spop(self, name: _Value, count: int) -> list[_StrType] | None: ...
    @overload
    def srandmember(self, name: _Value, number: None = None) -> _StrType | None: ...
    @overload
    def srandmember(self, name: _Value, number: int) -> list[_StrType] | None: ...
    def srem(self, name: _Value, *values: _Value) -> int: ...
    def sunion(
        self, keys: _Value | Iterable[_Value], *args: _Value
    ) -> list[_StrType]: ...
    def sunionstore(
        self, dest: _Value, keys: _Value | Iterable[_Value], *args: _Value
    ) -> int: ...

class AsyncSetCommands(Generic[_StrType]):
    async def sadd(self, name: _Value, *values: _Value) -> int: ...
    async def scard(self, name: _Value) -> int: ...
    async def sdiff(
        self, keys: _Value | Iterable[_Value], *args: _Value
    ) -> list[_StrType]: ...
    async def sdiffstore(
        self, dest: _Value, keys: _Value | Iterable[_Value], *args: _Value
    ) -> int: ...
    async def sinter(
        self, keys: _Value | Iterable[_Value], *args: _Value
    ) -> list[_StrType]: ...
    async def sintercard(
        self, numkeys: int, keys: Iterable[_Value], limit: int = 0
    ) -> int: ...
    async def sinterstore(
        self, dest: _Value, keys: _Value | Iterable[_Value], *args: _Value
    ) -> int: ...
    async def sismember(
        self, name: _Value, value: _Value
    ) -> Literal[0] | Literal[1]: ...
    async def smembers(self, name: _Value) -> list[_StrType]: ...
    async def smismember(
        self, name: _Value, values: _Value | Iterable[_Value], *args: _Value
    ) -> list[Literal[0] | Literal[1]]: ...
    async def smove(self, src: _Value, dst: _Value, value: _Value) -> bool: ...
    @overload
    async def spop(self, name: _Value, count: None = None) -> _StrType | None: ...
    @overload
    async def spop(self, name: _Value, count: int) -> list[_StrType] | None: ...
    @overload
    async def srandmember(
        self, name: _Value, number: None = None
    ) -> _StrType | None: ...
    @overload
    async def srandmember(self, name: _Value, number: int) -> list[_StrType] | None: ...
    async def srem(self, name: _Value, *values: _Value) -> int: ...
    async def sunion(
        self, keys: _Value | Iterable[_Value], *args: _Value
    ) -> list[_StrType]: ...
    async def sunionstore(
        self, dest: _Value, keys: _Value | Iterable[_Value], *args: _Value
    ) -> int: ...

# NOTE: The StreamCommands stubs might be incomplete or inaccurate.
class StreamCommands(Generic[_StrType]):
    def xack(self, name: _Value, groupname: GroupT, *ids: StreamIdT) -> int: ...
    def xadd(
        self,
        name: _Value,
        fields: dict[_Value, AnyEncodableT],
        id: StreamIdT = "*",
        maxlen: int | None = None,
        approximate: bool = True,
        nomkstream: bool = False,
        minid: StreamIdT | None = None,
        limit: int | None = None,
    ) -> _StrType: ...
    def xautoclaim(
        self,
        name: _Key,
        groupname: GroupT,
        consumername: ConsumerT,
        min_idle_time: int,
        start_id: StreamIdT = "0-0",
        count: int | None = None,
        justid: bool = False,
    ): ...
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
    ): ...
    def xdel(self, name: _Key, *ids: StreamIdT) -> int: ...
    def xgroup_create(
        self,
        name: _Key,
        groupname: GroupT,
        id: StreamIdT = "$",
        mkstream: bool = False,
        entries_read: int | None = None,
    ) -> bool: ...
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
    ) -> bool: ...
    def xinfo_consumers(
        self, name: _Key, groupname: GroupT
    ) -> list[dict[_StrType, Any]]: ...
    def xinfo_groups(self, name: _Key) -> list[dict[_StrType, Any]]: ...
    def xinfo_stream(self, name: _Key, full: bool = False) -> dict[_StrType, Any]: ...
    def xlen(self, name: _Key) -> int: ...
    def xpending(self, name: _Key, groupname: GroupT) -> dict[_StrType, Any]: ...
    def xpending_range(
        self,
        name: _Key,
        groupname: GroupT,
        min: StreamIdT,
        max: StreamIdT,
        count: int,
        consumername: ConsumerT | None = None,
        idle: int | None = None,
    ): ...
    def xrange(
        self,
        name: _Key,
        min: StreamIdT = "-",
        max: StreamIdT = "+",
        count: int | None = None,
    ) -> list[tuple[StreamIdT, dict[_StrType, _StrType]]]: ...
    def xread(
        self,
        streams: Mapping[AnyKeyT, AnyStreamIdT],
        count: int | None = None,
        block: int | None = None,
    ): ...
    def xreadgroup(
        self,
        groupname: GroupT,
        consumername: ConsumerT,
        streams: Mapping[AnyKeyT, AnyStreamIdT],
        count: int | None = None,
        block: int | None = None,
        noack: bool = False,
    ): ...
    def xrevrange(
        self,
        name: _Key,
        max: StreamIdT = "+",
        min: StreamIdT = "-",
        count: int | None = None,
    ) -> list[tuple[StreamIdT, dict[_StrType, _StrType]]]: ...
    def xtrim(
        self,
        name: _Key,
        maxlen: int | None = None,
        approximate: bool = True,
        minid: StreamIdT | None = None,
        limit: int | None = None,
    ) -> int: ...

class AsyncStreamCommands(Generic[_StrType]):
    async def xack(self, name: _Value, groupname: GroupT, *ids: StreamIdT) -> int: ...
    async def xadd(
        self,
        name: _Value,
        fields: dict[_Value, AnyEncodableT],
        id: StreamIdT = "*",
        maxlen: int | None = None,
        approximate: bool = True,
        nomkstream: bool = False,
        minid: StreamIdT | None = None,
        limit: int | None = None,
    ) -> _StrType: ...
    async def xautoclaim(
        self,
        name: _Key,
        groupname: GroupT,
        consumername: ConsumerT,
        min_idle_time: int,
        start_id: StreamIdT = "0-0",
        count: int | None = None,
        justid: bool = False,
    ): ...
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
    ): ...
    async def xdel(self, name: _Key, *ids: StreamIdT) -> int: ...
    async def xgroup_create(
        self,
        name: _Key,
        groupname: GroupT,
        id: StreamIdT = "$",
        mkstream: bool = False,
        entries_read: int | None = None,
    ) -> bool: ...
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
    ) -> bool: ...
    async def xinfo_consumers(
        self, name: _Key, groupname: GroupT
    ) -> list[dict[_StrType, Any]]: ...
    async def xinfo_groups(self, name: _Key) -> list[dict[_StrType, Any]]: ...
    async def xinfo_stream(
        self, name: _Key, full: bool = False
    ) -> dict[_StrType, Any]: ...
    async def xlen(self, name: _Key) -> int: ...
    async def xpending(self, name: _Key, groupname: GroupT) -> dict[_StrType, Any]: ...
    async def xpending_range(
        self,
        name: _Key,
        groupname: GroupT,
        min: StreamIdT,
        max: StreamIdT,
        count: int,
        consumername: ConsumerT | None = None,
        idle: int | None = None,
    ): ...
    async def xrange(
        self,
        name: _Key,
        min: StreamIdT = "-",
        max: StreamIdT = "+",
        count: int | None = None,
    ) -> list[tuple[StreamIdT, dict[_StrType, _StrType]]]: ...
    async def xread(
        self,
        streams: Mapping[AnyKeyT, AnyStreamIdT],
        count: int | None = None,
        block: int | None = None,
    ): ...
    async def xreadgroup(
        self,
        groupname: GroupT,
        consumername: ConsumerT,
        streams: Mapping[AnyKeyT, AnyStreamIdT],
        count: int | None = None,
        block: int | None = None,
        noack: bool = False,
    ): ...
    async def xrevrange(
        self,
        name: _Key,
        max: StreamIdT = "+",
        min: StreamIdT = "-",
        count: int | None = None,
    ) -> list[tuple[StreamIdT, dict[_StrType, _StrType]]]: ...
    async def xtrim(
        self,
        name: _Key,
        maxlen: int | None = None,
        approximate: bool = True,
        minid: StreamIdT | None = None,
        limit: int | None = None,
    ) -> int: ...

class SortedSetCommands(Generic[_StrType]):
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
    ) -> int: ...
    def zcard(self, name: _Key) -> int: ...
    def zcount(self, name: _Key, min: ZScoreBoundT, max: ZScoreBoundT) -> int: ...
    def zdiff(
        self, keys: Sequence[_Key], withscores: bool = False
    ) -> list[_StrType]: ...
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
    ) -> list[tuple[_StrType, float]]: ...
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
    ) -> list[tuple[_StrType, float]]: ...
    def zpopmin(
        self, name: _Key, count: int | None = None
    ) -> list[tuple[_StrType, float]]: ...
    @overload
    def zrandmember(self, key: _Key) -> _StrType | None: ...
    # TODO: Should zrandmember return list of tuples when withscores=True?
    @overload
    def zrandmember(
        self, key: _Key, count: int, withscores: bool = False
    ) -> list[_StrType]: ...
    def bzpopmax(self, keys: KeysT, timeout: TimeoutSecT = 0) -> ResponseT: ...
    def bzpopmin(self, keys: KeysT, timeout: TimeoutSecT = 0) -> ResponseT: ...
    def zmpop(
        self,
        num_keys: int,
        keys: list[str],
        min: bool | None = False,
        max: bool | None = False,
        count: int | None = 1,
    ) -> Awaitable[list] | list: ...
    def bzmpop(
        self,
        timeout: float,
        numkeys: int,
        keys: list[str],
        min: bool | None = False,
        max: bool | None = False,
        count: int | None = 1,
    ) -> list | None: ...
    def zrange(
        self,
        name: KeyT,
        start: int,
        end: int,
        desc: bool = False,
        withscores: bool = False,
        score_cast_func: type | Callable = ...,
        byscore: bool = False,
        bylex: bool = False,
        offset: int = None,
        num: int = None,
    ) -> ResponseT: ...
    def zrevrange(
        self,
        name: KeyT,
        start: int,
        end: int,
        withscores: bool = False,
        score_cast_func: type | Callable = ...,
    ) -> ResponseT: ...
    def zrangestore(
        self,
        dest: KeyT,
        name: KeyT,
        start: int,
        end: int,
        byscore: bool = False,
        bylex: bool = False,
        desc: bool = False,
        offset: int | None = None,
        num: int | None = None,
    ) -> ResponseT: ...
    def zrangebylex(
        self,
        name: KeyT,
        min: EncodableT,
        max: EncodableT,
        start: int | None = None,
        num: int | None = None,
    ) -> ResponseT: ...
    def zrevrangebylex(
        self,
        name: KeyT,
        max: EncodableT,
        min: EncodableT,
        start: int | None = None,
        num: int | None = None,
    ) -> ResponseT: ...
    def zrangebyscore(
        self,
        name: KeyT,
        min: ZScoreBoundT,
        max: ZScoreBoundT,
        start: int | None = None,
        num: int | None = None,
        withscores: bool = False,
        score_cast_func: type | Callable = ...,
    ) -> ResponseT: ...
    def zrevrangebyscore(
        self,
        name: KeyT,
        max: ZScoreBoundT,
        min: ZScoreBoundT,
        start: int | None = None,
        num: int | None = None,
        withscores: bool = False,
        score_cast_func: type | Callable = ...,
    ): ...
    def zrank(
        self, name: KeyT, value: EncodableT, withscore: bool = False
    ) -> ResponseT: ...
    def zrem(self, name: KeyT, *values: FieldT) -> ResponseT: ...
    def zremrangebylex(
        self, name: KeyT, min: EncodableT, max: EncodableT
    ) -> ResponseT: ...
    def zremrangebyrank(self, name: KeyT, min: int, max: int) -> ResponseT: ...
    def zremrangebyscore(
        self, name: KeyT, min: ZScoreBoundT, max: ZScoreBoundT
    ) -> ResponseT: ...
    def zrevrank(
        self, name: KeyT, value: EncodableT, withscore: bool = False
    ) -> ResponseT: ...
    def zscore(self, name: KeyT, value: EncodableT) -> ResponseT: ...
    def zunion(
        self,
        keys: Sequence[KeyT] | Mapping[AnyKeyT, float],
        aggregate: str | None = None,
        withscores: bool = False,
    ) -> ResponseT: ...
    def zunionstore(
        self,
        dest: KeyT,
        keys: Sequence[KeyT] | Mapping[AnyKeyT, float],
        aggregate: str | None = None,
    ) -> ResponseT: ...
    def zmscore(self, key: KeyT, members: list[str]) -> ResponseT: ...

AsyncSortedSetCommands = SortedSetCommands

class HyperlogCommands(CommandsProtocol):
    def pfadd(self, name: KeyT, *values: FieldT) -> ResponseT: ...
    def pfcount(self, *sources: KeyT) -> ResponseT: ...
    def pfmerge(self, dest: KeyT, *sources: KeyT) -> ResponseT: ...

AsyncHyperlogCommands = HyperlogCommands

class HashCommands(CommandsProtocol):
    def hdel(self, name: str, *keys: str) -> Awaitable[int] | int: ...
    def hexists(self, name: str, key: str) -> Awaitable[bool] | bool: ...
    def hget(self, name: str, key: str) -> Awaitable[str | None] | str | None: ...
    def hgetall(self, name: str) -> Awaitable[dict] | dict: ...
    def hincrby(self, name: str, key: str, amount: int = 1) -> Awaitable[int] | int: ...
    def hincrbyfloat(
        self, name: str, key: str, amount: float = 1.0
    ) -> Awaitable[float] | float: ...
    def hkeys(self, name: str) -> Awaitable[list] | list: ...
    def hlen(self, name: str) -> Awaitable[int] | int: ...
    def hset(
        self,
        name: str,
        key: str | None = None,
        value: str | None = None,
        mapping: dict | None = None,
        items: list | None = None,
    ) -> Awaitable[int] | int: ...
    def hsetnx(self, name: str, key: str, value: str) -> Awaitable[bool] | bool: ...
    def hmset(self, name: str, mapping: dict) -> Awaitable[str] | str: ...
    def hmget(self, name: str, keys: list, *args: list) -> Awaitable[list] | list: ...
    def hvals(self, name: str) -> Awaitable[list] | list: ...
    def hstrlen(self, name: str, key: str) -> Awaitable[int] | int: ...

AsyncHashCommands = HashCommands

class Script:
    registered_client: Incomplete
    script: Incomplete
    sha: Incomplete
    def __init__(self, registered_client: Valkey, script: ScriptTextT) -> None: ...
    def __call__(
        self,
        keys: Sequence[KeyT] | None = None,
        args: Iterable[EncodableT] | None = None,
        client: Valkey | None = None,
    ): ...

class AsyncScript:
    registered_client: Incomplete
    script: Incomplete
    sha: Incomplete
    def __init__(self, registered_client: AsyncValkey, script: ScriptTextT) -> None: ...
    async def __call__(
        self,
        keys: Sequence[KeyT] | None = None,
        args: Iterable[EncodableT] | None = None,
        client: AsyncValkey | None = None,
    ): ...

class PubSubCommands(CommandsProtocol):
    def publish(
        self, channel: ChannelT, message: EncodableT, **kwargs
    ) -> ResponseT: ...
    def spublish(self, shard_channel: ChannelT, message: EncodableT) -> ResponseT: ...
    def pubsub_channels(self, pattern: PatternT = "*", **kwargs) -> ResponseT: ...
    def pubsub_shardchannels(self, pattern: PatternT = "*", **kwargs) -> ResponseT: ...
    def pubsub_numpat(self, **kwargs) -> ResponseT: ...
    def pubsub_numsub(self, *args: ChannelT, **kwargs) -> ResponseT: ...
    def pubsub_shardnumsub(self, *args: ChannelT, **kwargs) -> ResponseT: ...

AsyncPubSubCommands = PubSubCommands

class ScriptCommands(CommandsProtocol):
    def eval(
        self, script: str, numkeys: int, *keys_and_args: str
    ) -> Awaitable[str] | str: ...
    def eval_ro(
        self, script: str, numkeys: int, *keys_and_args: str
    ) -> Awaitable[str] | str: ...
    def evalsha(
        self, sha: str, numkeys: int, *keys_and_args: str
    ) -> Awaitable[str] | str: ...
    def evalsha_ro(
        self, sha: str, numkeys: int, *keys_and_args: str
    ) -> Awaitable[str] | str: ...
    def script_exists(self, *args: str) -> ResponseT: ...
    def script_debug(self, *args) -> None: ...
    def script_flush(
        self, sync_type: Literal["SYNC"] | Literal["ASYNC"] = None
    ) -> ResponseT: ...
    def script_kill(self) -> ResponseT: ...
    def script_load(self, script: ScriptTextT) -> ResponseT: ...
    def register_script(self, script: ScriptTextT) -> Script: ...

class AsyncScriptCommands(ScriptCommands):
    async def script_debug(self, *args) -> None: ...
    def register_script(self, script: ScriptTextT) -> AsyncScript: ...

class GeoCommands(CommandsProtocol):
    def geoadd(
        self,
        name: KeyT,
        values: Sequence[EncodableT],
        nx: bool = False,
        xx: bool = False,
        ch: bool = False,
    ) -> ResponseT: ...
    def geodist(
        self, name: KeyT, place1: FieldT, place2: FieldT, unit: str | None = None
    ) -> ResponseT: ...
    def geohash(self, name: KeyT, *values: FieldT) -> ResponseT: ...
    def geopos(self, name: KeyT, *values: FieldT) -> ResponseT: ...
    def georadius(
        self,
        name: KeyT,
        longitude: float,
        latitude: float,
        radius: float,
        unit: str | None = None,
        withdist: bool = False,
        withcoord: bool = False,
        withhash: bool = False,
        count: int | None = None,
        sort: str | None = None,
        store: KeyT | None = None,
        store_dist: KeyT | None = None,
        any: bool = False,
    ) -> ResponseT: ...
    def georadiusbymember(
        self,
        name: KeyT,
        member: FieldT,
        radius: float,
        unit: str | None = None,
        withdist: bool = False,
        withcoord: bool = False,
        withhash: bool = False,
        count: int | None = None,
        sort: str | None = None,
        store: KeyT | None = None,
        store_dist: KeyT | None = None,
        any: bool = False,
    ) -> ResponseT: ...
    def geosearch(
        self,
        name: KeyT,
        member: FieldT | None = None,
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
    ) -> ResponseT: ...
    def geosearchstore(
        self,
        dest: KeyT,
        name: KeyT,
        member: FieldT | None = None,
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
    ) -> ResponseT: ...

AsyncGeoCommands = GeoCommands

class ModuleCommands(CommandsProtocol):
    def module_load(self, path, *args) -> ResponseT: ...
    def module_loadex(
        self, path: str, options: list[str] | None = None, args: list[str] | None = None
    ) -> ResponseT: ...
    def module_unload(self, name) -> ResponseT: ...
    def module_list(self) -> ResponseT: ...
    def command_info(self) -> None: ...
    def command_count(self) -> ResponseT: ...
    def command_getkeys(self, *args) -> ResponseT: ...
    def command(self) -> ResponseT: ...

class Script:
    registered_client: Incomplete
    script: Incomplete
    sha: Incomplete
    def __init__(self, registered_client, script) -> None: ...
    def __call__(self, keys=[], args=[], client=None): ...
    def get_encoder(self): ...

class AsyncModuleCommands(ModuleCommands):
    async def command_info(self) -> None: ...

class ClusterCommands(CommandsProtocol):
    def cluster(self, cluster_arg, *args, **kwargs) -> ResponseT: ...
    def readwrite(self, **kwargs) -> ResponseT: ...
    def readonly(self, **kwargs) -> ResponseT: ...

AsyncClusterCommands = ClusterCommands

class FunctionCommands:
    def function_load(
        self, code: str, replace: bool | None = False
    ) -> Awaitable[str] | str: ...
    def function_delete(self, library: str) -> Awaitable[str] | str: ...
    def function_flush(self, mode: str = "SYNC") -> Awaitable[str] | str: ...
    def function_list(
        self, library: str | None = "*", withcode: bool | None = False
    ) -> Awaitable[list] | list: ...
    def fcall(
        self, function, numkeys: int, *keys_and_args: list | None
    ) -> Awaitable[str] | str: ...
    def fcall_ro(
        self, function, numkeys: int, *keys_and_args: list | None
    ) -> Awaitable[str] | str: ...
    def function_dump(self) -> Awaitable[str] | str: ...
    def function_restore(
        self, payload: str, policy: str | None = "APPEND"
    ) -> Awaitable[str] | str: ...
    def function_kill(self) -> Awaitable[str] | str: ...
    def function_stats(self) -> Awaitable[list] | list: ...

AsyncFunctionCommands = FunctionCommands

class GearsCommands:
    def tfunction_load(
        self, lib_code: str, replace: bool = False, config: str | None = None
    ) -> ResponseT: ...
    def tfunction_delete(self, lib_name: str) -> ResponseT: ...
    def tfunction_list(
        self, with_code: bool = False, verbose: int = 0, lib_name: str | None = None
    ) -> ResponseT: ...
    def tfcall(
        self, lib_name: str, func_name: str, keys: KeysT = None, *args: list
    ) -> ResponseT: ...
    def tfcall_async(
        self, lib_name: str, func_name: str, keys: KeysT = None, *args: list
    ) -> ResponseT: ...

AsyncGearsCommands = GearsCommands

class DataAccessCommands(
    BasicKeyCommands,
    HyperlogCommands,
    HashCommands,
    GeoCommands,
    ListCommands,
    ScanCommands,
    SetCommands,
    StreamCommands,
    SortedSetCommands,
): ...
class AsyncDataAccessCommands(
    AsyncBasicKeyCommands,
    AsyncHyperlogCommands,
    AsyncHashCommands,
    AsyncGeoCommands,
    AsyncListCommands,
    AsyncScanCommands,
    AsyncSetCommands,
    AsyncStreamCommands,
    AsyncSortedSetCommands,
): ...
class CoreCommands(
    ACLCommands,
    ClusterCommands,
    DataAccessCommands,
    ManagementCommands,
    ModuleCommands,
    PubSubCommands,
    ScriptCommands,
    FunctionCommands,
    GearsCommands,
): ...
class AsyncCoreCommands(
    AsyncACLCommands,
    AsyncClusterCommands,
    AsyncDataAccessCommands,
    AsyncManagementCommands,
    AsyncModuleCommands,
    AsyncPubSubCommands,
    AsyncScriptCommands,
    AsyncFunctionCommands,
    AsyncGearsCommands,
): ...
