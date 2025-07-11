import copy
import random
import time
from abc import ABC, abstractmethod
from collections import OrderedDict, defaultdict
from enum import Enum
from typing import List, Sequence, Union

from valkey.typing import KeyT, ResponseT


class EvictionPolicy(str, Enum):
    LRU = "lru"
    LFU = "lfu"
    RANDOM = "random"


DEFAULT_EVICTION_POLICY = EvictionPolicy.LRU

DEFAULT_DENY_LIST = [
    "BF.CARD",
    "BF.DEBUG",
    "BF.EXISTS",
    "BF.INFO",
    "BF.MEXISTS",
    "BF.SCANDUMP",
    "CF.COMPACT",
    "CF.COUNT",
    "CF.DEBUG",
    "CF.EXISTS",
    "CF.INFO",
    "CF.MEXISTS",
    "CF.SCANDUMP",
    "CMS.INFO",
    "CMS.QUERY",
    "DUMP",
    "EXPIRETIME",
    "FT.AGGREGATE",
    "FT.ALIASADD",
    "FT.ALIASDEL",
    "FT.ALIASUPDATE",
    "FT.CURSOR",
    "FT.EXPLAIN",
    "FT.EXPLAINCLI",
    "FT.GET",
    "FT.INFO",
    "FT.MGET",
    "FT.PROFILE",
    "FT.SEARCH",
    "FT.SPELLCHECK",
    "FT.SUGGET",
    "FT.SUGLEN",
    "FT.SYNDUMP",
    "FT.TAGVALS",
    "FT._ALIASADDIFNX",
    "FT._ALIASDELIFX",
    "HRANDFIELD",
    "JSON.DEBUG",
    "PEXPIRETIME",
    "PFCOUNT",
    "PTTL",
    "SRANDMEMBER",
    "TDIGEST.BYRANK",
    "TDIGEST.BYREVRANK",
    "TDIGEST.CDF",
    "TDIGEST.INFO",
    "TDIGEST.MAX",
    "TDIGEST.MIN",
    "TDIGEST.QUANTILE",
    "TDIGEST.RANK",
    "TDIGEST.REVRANK",
    "TDIGEST.TRIMMED_MEAN",
    "TOPK.INFO",
    "TOPK.LIST",
    "TOPK.QUERY",
    "TOUCH",
    "TTL",
]

DEFAULT_ALLOW_LIST = [
    "BITCOUNT",
    "BITFIELD_RO",
    "BITPOS",
    "EXISTS",
    "GEODIST",
    "GEOHASH",
    "GEOPOS",
    "GEORADIUSBYMEMBER_RO",
    "GEORADIUS_RO",
    "GEOSEARCH",
    "GET",
    "GETBIT",
    "GETRANGE",
    "HEXISTS",
    "HGET",
    "HGETALL",
    "HKEYS",
    "HLEN",
    "HMGET",
    "HSTRLEN",
    "HVALS",
    "JSON.ARRINDEX",
    "JSON.ARRLEN",
    "JSON.GET",
    "JSON.MGET",
    "JSON.OBJKEYS",
    "JSON.OBJLEN",
    "JSON.RESP",
    "JSON.STRLEN",
    "JSON.TYPE",
    "LCS",
    "LINDEX",
    "LLEN",
    "LPOS",
    "LRANGE",
    "MGET",
    "SCARD",
    "SDIFF",
    "SINTER",
    "SINTERCARD",
    "SISMEMBER",
    "SMEMBERS",
    "SMISMEMBER",
    "SORT_RO",
    "STRLEN",
    "SUBSTR",
    "SUNION",
    "TS.GET",
    "TS.INFO",
    "TS.RANGE",
    "TS.REVRANGE",
    "TYPE",
    "XLEN",
    "XPENDING",
    "XRANGE",
    "XREAD",
    "XREVRANGE",
    "ZCARD",
    "ZCOUNT",
    "ZDIFF",
    "ZINTER",
    "ZINTERCARD",
    "ZLEXCOUNT",
    "ZMSCORE",
    "ZRANGE",
    "ZRANGEBYLEX",
    "ZRANGEBYSCORE",
    "ZRANK",
    "ZREVRANGE",
    "ZREVRANGEBYLEX",
    "ZREVRANGEBYSCORE",
    "ZREVRANK",
    "ZSCORE",
    "ZUNION",
]

_RESPONSE = "response"
_KEYS = "keys"
_CTIME = "ctime"
_ACCESS_COUNT = "access_count"


class AbstractCache(ABC):
    """
    An abstract base class for client caching implementations.
    If you want to implement your own cache you must support these methods.
    """

    @abstractmethod
    def set(
        self,
        command: Union[str, Sequence[str]],
        response: ResponseT,
        keys_in_command: List[KeyT],
    ):
        pass

    @abstractmethod
    def get(self, command: Union[str, Sequence[str]]) -> ResponseT:
        pass

    @abstractmethod
    def delete_command(self, command: Union[str, Sequence[str]]):
        pass

    @abstractmethod
    def delete_commands(self, commands: List[Union[str, Sequence[str]]]):
        pass

    @abstractmethod
    def flush(self):
        pass

    @abstractmethod
    def invalidate_key(self, key: KeyT):
        pass


class _LocalCache(AbstractCache):
    """
    A caching mechanism for storing valkey commands and their responses.

    Args:
        max_size (int): The maximum number of commands to be stored in the cache.
        ttl (int): The time-to-live for each command in seconds.
        eviction_policy (EvictionPolicy): The eviction policy to use for removing commands when the cache is full.

    Attributes:
        max_size (int): The maximum number of commands to be stored in the cache.
        ttl (int): The time-to-live for each command in seconds.
        eviction_policy (EvictionPolicy): The eviction policy used for cache management.
        cache (OrderedDict): The ordered dictionary to store commands and their metadata.
        key_commands_map (defaultdict): A mapping of keys to the set of commands that use each key.
        commands_ttl_list (list): A list to keep track of the commands in the order they were added.  # noqa
    """

    def __init__(
        self,
        max_size: int = 10000,
        ttl: int = 0,
        eviction_policy: EvictionPolicy = DEFAULT_EVICTION_POLICY,
    ):
        self.max_size = max_size
        self.ttl = ttl
        self.eviction_policy = eviction_policy
        self.cache = OrderedDict()
        self.key_commands_map = defaultdict(set)
        self.commands_ttl_list = []

    def set(
        self,
        command: Union[str, Sequence[str]],
        response: ResponseT,
        keys_in_command: List[KeyT],
    ):
        """
        Set a valkey command and its response in the cache.

        Args:
            command (Union[str, Sequence[str]]): The valkey command.
            response (ResponseT): The response associated with the command.
            keys_in_command (List[KeyT]): The list of keys used in the command.
        """
        if len(self.cache) >= self.max_size:
            self._evict()
        self.cache[command] = {
            _RESPONSE: response,
            _KEYS: keys_in_command,
            _CTIME: time.monotonic(),
            _ACCESS_COUNT: 0,  # Used only for LFU
        }
        self._update_key_commands_map(keys_in_command, command)
        self.commands_ttl_list.append(command)

    def get(self, command: Union[str, Sequence[str]]) -> ResponseT:
        """
        Get the response for a valkey command from the cache.

        Args:
            command (Union[str, Sequence[str]]): The valkey command.

        Returns:
            ResponseT: The response associated with the command, or None if the command is not in the cache.  # noqa
        """
        if command in self.cache:
            if self._is_expired(command):
                self.delete_command(command)
                return
            self._update_access(command)
            return copy.deepcopy(self.cache[command]["response"])

    def delete_command(self, command: Union[str, Sequence[str]]):
        """
        Delete a valkey command and its metadata from the cache.

        Args:
            command (Union[str, Sequence[str]]): The valkey command to be deleted.
        """
        if command in self.cache:
            keys_in_command = self.cache[command].get("keys")
            self._del_key_commands_map(keys_in_command, command)
            self.commands_ttl_list.remove(command)
            del self.cache[command]

    def delete_commands(self, commands: List[Union[str, Sequence[str]]]):
        """
        Delete multiple commands and their metadata from the cache.

        Args:
            commands (List[Union[str, Sequence[str]]]): The list of commands to be
            deleted.
        """
        for command in commands:
            self.delete_command(command)

    def flush(self):
        """Clear the entire cache, removing all valkey commands and metadata."""
        self.cache.clear()
        self.key_commands_map.clear()
        self.commands_ttl_list = []

    def _is_expired(self, command: Union[str, Sequence[str]]) -> bool:
        """
        Check if a valkey command has expired based on its time-to-live.

        Args:
            command (Union[str, Sequence[str]]): The valkey command.

        Returns:
            bool: True if the command has expired, False otherwise.
        """
        if self.ttl == 0:
            return False
        return time.monotonic() - self.cache[command]["ctime"] > self.ttl

    def _update_access(self, command: Union[str, Sequence[str]]):
        """
        Update the access information for a valkey command based on the eviction policy.

        Args:
            command (Union[str, Sequence[str]]): The valkey command.
        """
        if self.eviction_policy == EvictionPolicy.LRU:
            self.cache.move_to_end(command)
        elif self.eviction_policy == EvictionPolicy.LFU:
            self.cache[command]["access_count"] = (
                self.cache.get(command, {}).get("access_count", 0) + 1
            )
            self.cache.move_to_end(command)
        elif self.eviction_policy == EvictionPolicy.RANDOM:
            pass  # Random eviction doesn't require updates

    def _evict(self):
        """Evict a valkey command from the cache based on the eviction policy."""
        if self._is_expired(self.commands_ttl_list[0]):
            self.delete_command(self.commands_ttl_list[0])
        elif self.eviction_policy == EvictionPolicy.LRU:
            self.cache.popitem(last=False)
        elif self.eviction_policy == EvictionPolicy.LFU:
            min_access_command = min(
                self.cache, key=lambda k: self.cache[k].get("access_count", 0)
            )
            self.cache.pop(min_access_command)
        elif self.eviction_policy == EvictionPolicy.RANDOM:
            random_command = random.choice(list(self.cache.keys()))
            self.cache.pop(random_command)

    def _update_key_commands_map(
        self, keys: List[KeyT], command: Union[str, Sequence[str]]
    ):
        """
        Update the key_commands_map with command that uses the keys.

        Args:
            keys (List[KeyT]): The list of keys used in the command.
            command (Union[str, Sequence[str]]): The valkey command.
        """
        for key in keys:
            self.key_commands_map[key].add(command)

    def _del_key_commands_map(
        self, keys: List[KeyT], command: Union[str, Sequence[str]]
    ):
        """
        Remove a valkey command from the key_commands_map.

        Args:
            keys (List[KeyT]): The list of keys used in the valkey command.
            command (Union[str, Sequence[str]]): The valkey command.
        """
        for key in keys:
            self.key_commands_map[key].remove(command)

    def invalidate_key(self, key: KeyT):
        """
        Invalidate (delete) all valkey commands associated with a specific key.

        Args:
            key (KeyT): The key to be invalidated.
        """
        if key not in self.key_commands_map:
            return
        commands = list(self.key_commands_map[key])
        for command in commands:
            self.delete_command(command)
