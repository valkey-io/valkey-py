import sys

from valkey import asyncio  # noqa
from valkey.backoff import default_backoff
from valkey.client import Valkey, StrictValkey
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
    ValkeyError,
    ResponseError,
    TimeoutError,
    WatchError,
)
from valkey.sentinel import (
    Sentinel,
    SentinelConnectionPool,
    SentinelManagedConnection,
    SentinelManagedSSLConnection,
)
from valkey.utils import from_url

if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata


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
    "from_url",
    "default_backoff",
    "InvalidResponse",
    "OutOfMemoryError",
    "PubSubError",
    "ReadOnlyError",
    "Valkey",
    "ValkeyCluster",
    "ValkeyError",
    "ResponseError",
    "Sentinel",
    "SentinelConnectionPool",
    "SentinelManagedConnection",
    "SentinelManagedSSLConnection",
    "SSLConnection",
    "UsernamePasswordCredentialProvider",
    "StrictValkey",
    "TimeoutError",
    "UnixDomainSocketConnection",
    "WatchError",
]
