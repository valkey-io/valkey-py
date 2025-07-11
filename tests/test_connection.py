import socket
import types
from unittest import mock
from unittest.mock import patch

import pytest
import valkey
from valkey import ConnectionPool, Valkey
from valkey._parsers import _LibvalkeyParser, _RESP2Parser, _RESP3Parser
from valkey.backoff import NoBackoff
from valkey.connection import (
    Connection,
    SSLConnection,
    UnixDomainSocketConnection,
    parse_url,
)
from valkey.exceptions import ConnectionError, InvalidResponse, TimeoutError
from valkey.retry import Retry
from valkey.utils import LIBVALKEY_AVAILABLE

from .conftest import skip_if_server_version_lt
from .mocks import MockSocket


@pytest.mark.skipif(LIBVALKEY_AVAILABLE, reason="PythonParser only")
@pytest.mark.onlynoncluster
def test_invalid_response(r):
    raw = b"x"
    parser = r.connection._parser
    with mock.patch.object(parser._buffer, "readline", return_value=raw):
        with pytest.raises(InvalidResponse) as cm:
            parser.read_response()
    assert str(cm.value) == f"Protocol Error: {raw!r}"


@skip_if_server_version_lt("4.0.0")
@pytest.mark.valkeymod
def test_loading_external_modules(r):
    def inner():
        pass

    r.load_external_module("myfuncname", inner)
    assert getattr(r, "myfuncname") == inner
    assert isinstance(getattr(r, "myfuncname"), types.FunctionType)

    # and call it
    from valkey.commands import ValkeyModuleCommands

    j = ValkeyModuleCommands.json
    r.load_external_module("sometestfuncname", j)

    # d = {'hello': 'world!'}
    # mod = j(r)
    # mod.set("fookey", ".", d)
    # assert mod.get('fookey') == d


class TestConnection:
    def test_disconnect(self):
        conn = Connection()
        mock_sock = mock.Mock()
        conn._sock = mock_sock
        conn.disconnect()
        mock_sock.shutdown.assert_called_once()
        mock_sock.close.assert_called_once()
        assert conn._sock is None

    def test_disconnect__shutdown_OSError(self):
        """An OSError on socket shutdown will still close the socket."""
        conn = Connection()
        mock_sock = mock.Mock()
        conn._sock = mock_sock
        conn._sock.shutdown.side_effect = OSError
        conn.disconnect()
        mock_sock.shutdown.assert_called_once()
        mock_sock.close.assert_called_once()
        assert conn._sock is None

    def test_disconnect__close_OSError(self):
        """An OSError on socket close will still clear out the socket."""
        conn = Connection()
        mock_sock = mock.Mock()
        conn._sock = mock_sock
        conn._sock.close.side_effect = OSError
        conn.disconnect()
        mock_sock.shutdown.assert_called_once()
        mock_sock.close.assert_called_once()
        assert conn._sock is None

    def clear(self, conn):
        conn.retry_on_error.clear()

    def test_retry_connect_on_timeout_error(self):
        """Test that the _connect function is retried in case of a timeout"""
        conn = Connection(retry_on_timeout=True, retry=Retry(NoBackoff(), 3))
        origin_connect = conn._connect
        conn._connect = mock.Mock()

        def mock_connect():
            # connect only on the last retry
            if conn._connect.call_count <= 2:
                raise socket.timeout
            else:
                return origin_connect()

        conn._connect.side_effect = mock_connect
        conn.connect()
        assert conn._connect.call_count == 3
        self.clear(conn)

    def test_connect_without_retry_on_os_error(self):
        """Test that the _connect function is not being retried in case of a OSError"""
        with patch.object(Connection, "_connect") as _connect:
            _connect.side_effect = OSError("")
            conn = Connection(retry_on_timeout=True, retry=Retry(NoBackoff(), 2))
            with pytest.raises(ConnectionError):
                conn.connect()
            assert _connect.call_count == 1
            self.clear(conn)

    def test_connect_timeout_error_without_retry(self):
        """Test that the _connect function is not being retried if retry_on_timeout is
        set to False"""
        conn = Connection(retry_on_timeout=False)
        conn._connect = mock.Mock()
        conn._connect.side_effect = socket.timeout

        with pytest.raises(TimeoutError) as e:
            conn.connect()
        assert conn._connect.call_count == 1
        assert str(e.value) == "Timeout connecting to server"
        self.clear(conn)


@pytest.mark.onlynoncluster
@pytest.mark.parametrize(
    "parser_class",
    [_RESP2Parser, _RESP3Parser, _LibvalkeyParser],
    ids=["RESP2Parser", "RESP3Parser", "LibvalkeyParser"],
)
def test_connection_parse_response_resume(r: valkey.Valkey, parser_class):
    """
    This test verifies that the Connection parser,
    be that PythonParser or LibvalkeyParser,
    can be interrupted at IO time and then resume parsing.
    """
    if parser_class is _LibvalkeyParser and not LIBVALKEY_AVAILABLE:
        pytest.skip("Libvalkey not available)")
    args = dict(r.connection_pool.connection_kwargs)
    args["parser_class"] = parser_class
    conn = Connection(**args)
    conn.connect()
    message = (
        b"*3\r\n$7\r\nmessage\r\n$8\r\nchannel1\r\n"
        b"$25\r\nhi\r\nthere\r\n+how\r\nare\r\nyou\r\n"
    )
    mock_socket = MockSocket(message, interrupt_every=2)

    if isinstance(conn._parser, _RESP2Parser) or isinstance(conn._parser, _RESP3Parser):
        conn._parser._buffer._sock = mock_socket
    else:
        conn._parser._sock = mock_socket
    for i in range(100):
        try:
            response = conn.read_response(disconnect_on_error=False)
            break
        except MockSocket.TestError:
            pass

    else:
        pytest.fail("didn't receive a response")
    assert response
    assert i > 0


@pytest.mark.onlynoncluster
@pytest.mark.parametrize(
    "Class",
    [
        Connection,
        SSLConnection,
        UnixDomainSocketConnection,
    ],
)
def test_pack_command(Class):
    """
    This test verifies that the pack_command works
    on all supported connections. #2581
    """
    cmd = (
        "HSET",
        "foo",
        "key",
        "value1",
        b"key_b",
        b"bytes str",
        b"key_i",
        67,
        "key_f",
        3.14159265359,
    )
    expected = (
        b"*10\r\n$4\r\nHSET\r\n$3\r\nfoo\r\n$3\r\nkey\r\n$6\r\nvalue1\r\n"
        b"$5\r\nkey_b\r\n$9\r\nbytes str\r\n$5\r\nkey_i\r\n$2\r\n67\r\n$5"
        b"\r\nkey_f\r\n$13\r\n3.14159265359\r\n"
    )

    actual = Class().pack_command(*cmd)[0]
    assert actual == expected, f"actual = {actual}, expected = {expected}"


@pytest.mark.onlynoncluster
def test_create_single_connection_client_from_url():
    client = valkey.Valkey.from_url(
        "valkey://localhost:6379/0?", single_connection_client=True
    )
    assert client.connection is not None


@pytest.mark.parametrize("from_url", (True, False), ids=("from_url", "from_args"))
def test_pool_auto_close(request, from_url):
    """Verify that basic Valkey instances have auto_close_connection_pool set to True"""

    url: str = request.config.getoption("--valkey-url")
    url_args = parse_url(url)

    def get_valkey_connection():
        if from_url:
            return Valkey.from_url(url)
        return Valkey(**url_args)

    r1 = get_valkey_connection()
    assert r1.auto_close_connection_pool is True
    r1.close()


@pytest.mark.parametrize("from_url", (True, False), ids=("from_url", "from_args"))
def test_valkey_connection_pool(request, from_url):
    """Verify that basic Valkey instances using `connection_pool`
    have auto_close_connection_pool set to False"""

    url: str = request.config.getoption("--valkey-url")
    url_args = parse_url(url)

    pool = None

    def get_valkey_connection():
        nonlocal pool
        if from_url:
            pool = ConnectionPool.from_url(url)
        else:
            pool = ConnectionPool(**url_args)
        return Valkey(connection_pool=pool)

    called = 0

    def mock_disconnect(_):
        nonlocal called
        called += 1

    with patch.object(ConnectionPool, "disconnect", mock_disconnect):
        with get_valkey_connection() as r1:
            assert r1.auto_close_connection_pool is False

    assert called == 0
    pool.disconnect()


@pytest.mark.parametrize("from_url", (True, False), ids=("from_url", "from_args"))
def test_valkey_from_pool(request, from_url):
    """Verify that basic Valkey instances created using `from_pool()`
    have auto_close_connection_pool set to True"""

    url: str = request.config.getoption("--valkey-url")
    url_args = parse_url(url)

    pool = None

    def get_valkey_connection():
        nonlocal pool
        if from_url:
            pool = ConnectionPool.from_url(url)
        else:
            pool = ConnectionPool(**url_args)
        return Valkey.from_pool(pool)

    called = 0

    def mock_disconnect(_):
        nonlocal called
        called += 1

    with patch.object(ConnectionPool, "disconnect", mock_disconnect):
        with get_valkey_connection() as r1:
            assert r1.auto_close_connection_pool is True

    assert called == 1
    pool.disconnect()


@pytest.mark.parametrize(
    "conn, error, expected_message",
    [
        (SSLConnection(), OSError(), "Error connecting to localhost:6379."),
        (SSLConnection(), OSError(12), "Error 12 connecting to localhost:6379."),
        (
            SSLConnection(),
            OSError(12, "Some Error"),
            "Error 12 connecting to localhost:6379. Some Error.",
        ),
        (
            UnixDomainSocketConnection(path="unix:///tmp/valkey.sock"),
            OSError(),
            "Error connecting to unix:///tmp/valkey.sock.",
        ),
        (
            UnixDomainSocketConnection(path="unix:///tmp/valkey.sock"),
            OSError(12),
            "Error 12 connecting to unix:///tmp/valkey.sock.",
        ),
        (
            UnixDomainSocketConnection(path="unix:///tmp/valkey.sock"),
            OSError(12, "Some Error"),
            "Error 12 connecting to unix:///tmp/valkey.sock. Some Error.",
        ),
    ],
)
def test_format_error_message(conn, error, expected_message):
    """Test that the _error_message function formats errors correctly"""
    error_message = conn._error_message(error)
    assert error_message == expected_message


def test_network_connection_failure():
    with pytest.raises(ConnectionError) as e:
        valkey = Valkey(port=9999)
        valkey.set("a", "b")
    assert str(e.value) == "Error 111 connecting to localhost:9999. Connection refused."


def test_unix_socket_connection_failure():
    with pytest.raises(ConnectionError) as e:
        valkey = Valkey(unix_socket_path="unix:///tmp/a.sock")
        valkey.set("a", "b")
    assert (
        str(e.value)
        == "Error 2 connecting to unix:///tmp/a.sock. No such file or directory."
    )


def test_parsing_unix_socket_relative_path():
    parsed = parse_url("unix:./valkey.sock")
    assert parsed["path"] == "./valkey.sock"
    assert parsed["connection_class"] is UnixDomainSocketConnection
    assert len(parsed) == 2
