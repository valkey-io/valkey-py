from valkey.typing import EncodedT

VALKEY_CLUSTER_HASH_SLOTS: int

def key_slot(key: EncodedT, bucket: int = 16384) -> int: ...
