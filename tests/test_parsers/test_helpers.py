from valkey._parsers.helpers import parse_info
from valkey.client import Valkey
from valkey.sentinel import Sentinel


def test_parse_info():
    info_output = """
# Modules
module:name=search,ver=999999,api=1,filters=0,usedby=[],using=[ReJSON],options=[handle-io-errors]

# search_fields_statistics
search_fields_text:Text=3
search_fields_tag:Tag=2,Sortable=1

# search_version
search_version:99.99.99
search_redis_version:7.2.2 - oss

# search_runtime_configurations
search_query_timeout_ms:500
    """
    info = parse_info(info_output)

    assert isinstance(info["modules"], list)
    assert isinstance(info["modules"][0], dict)
    assert info["modules"][0]["name"] == "search"

    assert isinstance(info["search_fields_text"], dict)
    assert info["search_fields_text"]["Text"] == 3

    assert isinstance(info["search_fields_tag"], dict)
    assert info["search_fields_tag"]["Tag"] == 2
    assert info["search_fields_tag"]["Sortable"] == 1

    assert info["search_version"] == "99.99.99"
    assert info["search_redis_version"] == "7.2.2 - oss"
    assert info["search_query_timeout_ms"] == 500


def test_parse_info_list():
    info_output = """
list_one:a,
list_two:a b,,c,10,1.1
    """
    info = parse_info(info_output)

    assert isinstance(info["list_one"], list)
    assert info["list_one"] == ["a"]

    assert isinstance(info["list_two"], list)
    assert info["list_two"] == ["a b", "c", 10, 1.1]


def test_parse_info_list_dict_mixed():
    info_output = """
list_one:a,b=1
list_two:a b=foo,,c,d=bar,e,
    """
    info = parse_info(info_output)

    assert isinstance(info["list_one"], dict)
    assert info["list_one"] == {"a": True, "b": 1}

    assert isinstance(info["list_two"], dict)
    assert info["list_two"] == {"a b": "foo", "c": True, "d": "bar", "e": True}


SENTINEL_STATE_VALUES = {
    "name": "mymaster",
    "ip": "127.0.0.1",
    "port": 6379,
    "runid": "0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f",
    "flags": "master",
    "num-slaves": 0,
    "num-other-sentinels": 1,
    "quorum": 2,
}

SENTINEL_DERIVED_BOOLEANS = (
    "is_master",
    "is_slave",
    "is_sdown",
    "is_odown",
    "is_sentinel",
    "is_disconnected",
    "is_master_down",
)


def _sentinel_resp3_state(**overrides):
    return dict(SENTINEL_STATE_VALUES, **overrides)


def _sentinel_resp2_state(state):
    """Render a sentinel state the way RESP2 does: a flat field/value array."""
    flat = []
    for field, value in state.items():
        flat += [field, value]
    return flat


def _make_sentinel(sentinel_clients):
    sentinel = Sentinel.__new__(Sentinel)
    sentinel.sentinels = sentinel_clients
    sentinel.min_other_sentinels = 0
    return sentinel


def test_sentinel_state_resp3_matches_resp2_shape():
    """SENTINEL MASTER/MASTERS/SENTINELS keep their documented shape on RESP3.

    RESP2 answers SENTINEL MASTERS as an array of flat field/value arrays and
    the client keys the parsed masters by name, so RESP3 -- where Sentinel
    answers maps -- must produce the same mapping. It must also derive the
    ``is_*`` booleans the RESP2 parser derives, since sentinel clients for
    both protocols share these response callbacks.
    """
    # whatever protocol the client runs, it selects its callbacks from here
    for protocol in (2, 3):
        kwargs = Valkey(protocol=protocol).connection_pool.connection_kwargs
        assert kwargs["protocol"] == protocol

    master = _sentinel_resp3_state()
    resp3_callbacks = Valkey(protocol=3).response_callbacks
    resp2_callbacks = Valkey(protocol=2).response_callbacks

    masters = resp3_callbacks["SENTINEL MASTERS"]([master])
    assert isinstance(masters, dict)
    assert list(masters) == [master["name"]]
    assert masters[master["name"]]["ip"] == master["ip"]

    for parsed in (
        masters[master["name"]],
        resp3_callbacks["SENTINEL MASTER"](master),
        resp3_callbacks["SENTINEL SENTINELS"]([master])[0],
    ):
        # RESP2 exposes the flags as a set of names; RESP3 must not disagree
        assert set(parsed) >= {"flags", *SENTINEL_DERIVED_BOOLEANS}
        assert parsed["flags"] == {"master"}
        assert parsed["is_master"] is True
        for flag in SENTINEL_DERIVED_BOOLEANS:
            assert parsed[flag] == (flag == "is_master")

    resp2_masters = resp2_callbacks["SENTINEL MASTERS"]([_sentinel_resp2_state(master)])
    for field, value in SENTINEL_STATE_VALUES.items():
        if field == "flags":
            continue
        assert masters[master["name"]][field] == resp2_masters[master["name"]][field]


def test_sentinel_state_resp3_decodes_bytes_fields():
    """Resp3 sentinel states decode their field names when not auto-decoded."""
    state = _sentinel_resp3_state()
    raw = {field.encode(): value for field, value in state.items()}

    parsed = Valkey(protocol=3).response_callbacks["SENTINEL MASTER"](raw)

    assert set(parsed) >= set(state)
    assert parsed["ip"] == "127.0.0.1"
    assert parsed["port"] == 6379
    assert parsed["num-other-sentinels"] == 1
    assert parsed["is_master"] is True


class _Resp3SentinelClient:
    """A sentinel client running protocol 3, parsed by its real callbacks."""

    def sentinel_masters(self):
        return Valkey(protocol=3).response_callbacks["SENTINEL MASTERS"](
            [_sentinel_resp3_state()]
        )


def test_discover_master_and_filter_slaves_from_resp3_states():
    """Sentinel.discover_master/filter_slaves consume RESP3 sentinel states."""
    sentinel = _make_sentinel([_Resp3SentinelClient()])
    assert sentinel.discover_master("mymaster") == ("127.0.0.1", 6379)

    slaves = Valkey(protocol=3).response_callbacks["SENTINEL SENTINELS"](
        [
            _sentinel_resp3_state(flags="slave"),
            _sentinel_resp3_state(flags="slave,s_down"),
            _sentinel_resp3_state(flags="slave,o_down"),
        ]
    )
    assert sentinel.filter_slaves(slaves) == [("127.0.0.1", 6379)]
