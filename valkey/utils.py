import contextlib
import logging
from functools import wraps
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Iterable,
    Iterator,
    Mapping,
    TypeVar,
    overload,
)

try:
    import libvalkey  # noqa

    # Only support libvalkey 4.0.0 and above
    LIBVALKEY_AVAILABLE = int(libvalkey.__version__.split(".")[0]) >= 4
except ImportError:
    LIBVALKEY_AVAILABLE = False

try:
    import ssl  # noqa

    SSL_AVAILABLE = True
except ImportError:
    SSL_AVAILABLE = False

try:
    import cryptography  # noqa

    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False

from importlib import metadata

if TYPE_CHECKING:
    from valkey.asyncio.client import Pipeline as AsyncPipeline
    from valkey.asyncio.client import Valkey as AsyncValkey
    from valkey.asyncio.cluster import ClusterPipeline as AsyncClusterPipeline
    from valkey.asyncio.cluster import ValkeyCluster as AsyncValkeyCluster
    from valkey.client import Pipeline, Valkey
    from valkey.cluster import ClusterPipeline, ValkeyCluster


def from_url(url: str, **kwargs: dict[str, Any]) -> "Valkey":
    """
    Returns an active Valkey client generated from the given database URL.

    Will attempt to extract the database id from the path url fragment, if
    none is provided.
    """
    from valkey.client import Valkey

    return Valkey.from_url(url, **kwargs)


@overload
@contextlib.contextmanager
def pipeline(valkey_obj: "Valkey") -> Iterator["Pipeline"]: ...


@overload
@contextlib.contextmanager
def pipeline(valkey_obj: "ValkeyCluster") -> Iterator["ClusterPipeline"]: ...


@overload
@contextlib.contextmanager
def pipeline(valkey_obj: "AsyncValkey") -> Iterator["AsyncPipeline"]: ...


@overload
@contextlib.contextmanager
def pipeline(valkey_obj: "AsyncValkeyCluster") -> Iterator["AsyncClusterPipeline"]: ...


@contextlib.contextmanager
def pipeline(
    valkey_obj: "Valkey | ValkeyCluster | AsyncValkey | AsyncValkeyCluster",
) -> "Iterator[Pipeline | ClusterPipeline | AsyncPipeline | AsyncClusterPipeline]":
    p = valkey_obj.pipeline()
    yield p
    p.execute()


T = TypeVar("T")


@overload
def str_if_bytes(value: bytes) -> str: ...


@overload
def str_if_bytes(value: T) -> T: ...


def str_if_bytes(value: bytes | T) -> str | T:
    return (
        value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value
    )


def safe_str(value: Any) -> str:
    return str(str_if_bytes(value))


def dict_merge(*dicts: Mapping[str, Any]) -> dict[str, Any]:
    """
    Merge all provided dicts into 1 dict.
    *dicts : `dict`
        dictionaries to merge
    """
    merged: dict[str, Any] = {}

    for d in dicts:
        merged.update(d)

    return merged


list_keys_to_dict = dict.fromkeys


def merge_result(command: Any, res: dict[Any, Iterable[T]]) -> list[T]:
    """
    Merge all items in `res` into a list.

    This command is used when sending a command to multiple nodes
    and the result from each node should be merged into a single list.

    res : 'dict'
    """
    result = set()

    for v in res.values():
        for value in v:
            result.add(value)

    return list(result)


def warn_deprecated(
    name: str,
    reason: str = "",
    version: str = "",
    stacklevel: int = 2,
) -> None:
    import warnings

    msg = f"Call to deprecated {name}."
    if reason:
        msg += f" ({reason})"
    if version:
        msg += f" -- Deprecated since version {version}."
    warnings.warn(msg, category=DeprecationWarning, stacklevel=stacklevel)


def deprecated_function(
    reason: str = "",
    version: str = "",
    name: str | None = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator to mark a function as deprecated.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: dict[str, Any]) -> T:
            warn_deprecated(name or func.__name__, reason, version, stacklevel=3)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def _set_info_logger() -> None:
    """
    Set up a logger that log info logs to stdout.
    (This is used by the default push response handler)
    """
    if "push_response" not in logging.root.manager.loggerDict.keys():
        logger = logging.getLogger("push_response")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)


def get_lib_version() -> str:
    try:
        libver = metadata.version("valkey")
    except metadata.PackageNotFoundError:
        libver = "99.99.99"
    return libver


def format_error_message(host_error: str, exception: BaseException) -> str:
    if not exception.args:
        return f"Error connecting to {host_error}."
    elif len(exception.args) == 1:
        return f"Error {exception.args[0]} connecting to {host_error}."
    else:
        return (
            f"Error {exception.args[0]} connecting to {host_error}. "
            f"{exception.args[1]}."
        )
