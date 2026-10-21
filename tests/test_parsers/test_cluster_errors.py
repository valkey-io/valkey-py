import pytest
from valkey._parsers import (
    _AsyncRESP2Parser,
    _AsyncRESP3Parser,
    _RESP2Parser,
    _RESP3Parser,
)
from valkey.asyncio.cluster import ClusterParser as AsyncClusterParser
from valkey.cluster import ClusterParser
from valkey.exceptions import (
    AskError,
    ClusterDownError,
    MovedError,
    ResponseError,
    TryAgainError,
)

ERRORS = [
    ("CLUSTERDOWN The cluster is down", ClusterDownError),
    ("MOVED 3999 127.0.0.1:6381", MovedError),
    ("ASK 3999 127.0.0.1:6381", AskError),
    ("TRYAGAIN Multiple keys request during rehashing of slot", TryAgainError),
]


@pytest.mark.parametrize(
    "cluster_parser,resp3_parser",
    [(ClusterParser, _RESP3Parser), (AsyncClusterParser, _AsyncRESP3Parser)],
)
@pytest.mark.parametrize("response,exception_class", ERRORS)
def test_resp3_switch_keeps_cluster_errors(
    cluster_parser, resp3_parser, response, exception_class
):
    # What Connection.on_connect does when protocol=3 replaces a RESP2 parser.
    parser = resp3_parser(socket_read_size=65536)
    parser.EXCEPTION_CLASSES = cluster_parser.EXCEPTION_CLASSES

    assert type(parser.parse_error(response)) is exception_class


@pytest.mark.parametrize(
    "parser_class",
    [_RESP2Parser, _RESP3Parser, _AsyncRESP2Parser, _AsyncRESP3Parser],
)
def test_plain_parser_does_not_map_cluster_errors(parser_class):
    parser = parser_class(socket_read_size=65536)

    assert type(parser.parse_error("CLUSTERDOWN The cluster is down")) is ResponseError


def test_parse_error_still_works_on_the_class():
    assert type(ClusterParser.parse_error("MOVED 3999 127.0.0.1:6381")) is MovedError
    assert type(_RESP3Parser.parse_error("MOVED 3999 127.0.0.1:6381")) is ResponseError
