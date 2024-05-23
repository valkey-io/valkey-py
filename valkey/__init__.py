from importlib import metadata

from valkey import asyncio  # noqa
from valkey.backoff import default_backoff
from valkey.client import StrictValkey, Valkey
from valkey.cluster import ValkeyCluster
from valkey.connection import (
    BlockingConnectionPool,
    Connection,
    ConnectionPool,
    SSLConnection,
    UnixDomainSocketConnection,
)
from valkey.credentials import CredentialProvider, UsernamePasswordCredentialProvider
from valkey.exceptions import (
    AuthenticationError,
    AuthenticationWrongNumberOfArgsError,
    BusyLoadingError,
    ChildDeadlockedError,
    ConnectionError,
    DataError,
    InvalidResponse,
    OutOfMemoryError,
    PubSubError,
    ReadOnlyError,
    ResponseError,
    TimeoutError,
    ValkeyError,
    WatchError,
)
from valkey.sentinel import (
    Sentinel,
    SentinelConnectionPool,
    SentinelManagedConnection,
    SentinelManagedSSLConnection,
)
from valkey.utils import from_url


def int_or_str(value):
    try:
        return int(value)
    except ValueError:
        return value


try:
    __version__ = metadata.version("valkey")
except metadata.PackageNotFoundError:
    __version__ = "99.99.99"


try:
    VERSION = tuple(map(int_or_str, __version__.split(".")))
except AttributeError:
    VERSION = tuple([99, 99, 99])


Redis = Valkey
StrictRedis = StrictValkey
RedisCluster = ValkeyCluster
RedisError = ValkeyError


__all__ = [
    "AuthenticationError",
    "AuthenticationWrongNumberOfArgsError",
    "BlockingConnectionPool",
    "BusyLoadingError",
    "ChildDeadlockedError",
    "Connection",
    "ConnectionError",
    "ConnectionPool",
    "CredentialProvider",
    "DataError",
    "InvalidResponse",
    "OutOfMemoryError",
    "PubSubError",
    "ReadOnlyError",
    "Redis",
    "RedisCluster",
    "RedisError",
    "ResponseError",
    "SSLConnection",
    "Sentinel",
    "SentinelConnectionPool",
    "SentinelManagedConnection",
    "SentinelManagedSSLConnection",
    "StrictRedis",
    "StrictValkey",
    "TimeoutError",
    "UnixDomainSocketConnection",
    "UsernamePasswordCredentialProvider",
    "Valkey",
    "ValkeyCluster",
    "ValkeyError",
    "WatchError",
    "default_backoff",
    "from_url",
]
