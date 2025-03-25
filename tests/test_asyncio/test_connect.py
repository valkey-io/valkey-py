import logging
import re
import socket
import ssl

import anyio
import pytest
from anyio.abc import TaskStatus
from anyio.streams.tls import TLSListener

from valkey.asyncio.connection import (
    Connection,
    SSLConnection,
    UnixDomainSocketConnection,
)

from ..ssl_utils import get_ssl_filename

pytestmark = pytest.mark.anyio


_logger = logging.getLogger(__name__)


_CLIENT_NAME = "test-suite-client"
_CMD_SEP = b"\r\n"
_SUCCESS_RESP = b"+OK" + _CMD_SEP
_ERROR_RESP = b"-ERR" + _CMD_SEP
_SUPPORTED_CMDS = {f"CLIENT SETNAME {_CLIENT_NAME}": _SUCCESS_RESP}


@pytest.fixture
def tcp_address():
    # TODO: use `free_tcp_port` when anyio>=4.9
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()


@pytest.fixture
def uds_address(tmpdir):
    return tmpdir / "uds.sock"


async def test_tcp_connect(tcp_address):
    host, port = tcp_address
    conn = Connection(host=host, port=port, client_name=_CLIENT_NAME, socket_timeout=10)
    await _assert_connect(conn, tcp_address)


async def test_uds_connect(uds_address):
    path = str(uds_address)
    conn = UnixDomainSocketConnection(
        path=path, client_name=_CLIENT_NAME, socket_timeout=10
    )
    await _assert_connect(conn, path)


@pytest.mark.ssl
@pytest.mark.parametrize(
    "ssl_ciphers",
    [
        "AES256-SHA:DHE-RSA-AES256-SHA:AES128-SHA:DHE-RSA-AES128-SHA",
        "ECDHE-ECDSA-AES256-GCM-SHA384",
        "ECDHE-RSA-AES128-GCM-SHA256",
    ],
)
async def test_tcp_ssl_tls12_custom_ciphers(tcp_address, ssl_ciphers):
    host, port = tcp_address
    certfile = get_ssl_filename("client-cert.pem")
    keyfile = get_ssl_filename("client-key.pem")
    ca_certfile = get_ssl_filename("ca-cert.pem")
    conn = SSLConnection(
        host=host,
        port=port,
        client_name=_CLIENT_NAME,
        ssl_ca_certs=ca_certfile,
        socket_timeout=10,
        ssl_min_version=ssl.TLSVersion.TLSv1_2,
        ssl_ciphers=ssl_ciphers,
    )
    await _assert_connect(conn, tcp_address, certfile=certfile, keyfile=keyfile)
    await conn.disconnect()


@pytest.mark.ssl
@pytest.mark.parametrize(
    "ssl_min_version",
    [
        ssl.TLSVersion.TLSv1_2,
        pytest.param(
            ssl.TLSVersion.TLSv1_3,
            marks=pytest.mark.skipif(not ssl.HAS_TLSv1_3, reason="requires TLSv1.3"),
        ),
    ],
)
async def test_tcp_ssl_connect(tcp_address, ssl_min_version):
    host, port = tcp_address
    certfile = get_ssl_filename("client-cert.pem")
    keyfile = get_ssl_filename("client-key.pem")
    ca_certfile = get_ssl_filename("ca-cert.pem")
    conn = SSLConnection(
        host=host,
        port=port,
        client_name=_CLIENT_NAME,
        ssl_ca_certs=ca_certfile,
        socket_timeout=10,
        ssl_min_version=ssl_min_version,
    )
    await _assert_connect(conn, tcp_address, certfile=certfile, keyfile=keyfile)
    await conn.disconnect()


@pytest.mark.ssl
@pytest.mark.skipif(not ssl.HAS_TLSv1_3, reason="requires TLSv1.3")
async def test_tcp_ssl_version_mismatch(tcp_address):
    host, port = tcp_address
    certfile = get_ssl_filename("server-cert.pem")
    keyfile = get_ssl_filename("server-key.pem")
    conn = SSLConnection(
        host=host,
        port=port,
        client_name=_CLIENT_NAME,
        ssl_ca_certs=certfile,
        socket_timeout=1,
        ssl_min_version=ssl.TLSVersion.TLSv1_3,
    )
    with pytest.raises(Exception):
        await _assert_connect(
            conn,
            tcp_address,
            certfile=certfile,
            keyfile=keyfile,
            maximum_ssl_version=ssl.TLSVersion.TLSv1_2,
        )
    await conn.disconnect()


async def _assert_connect(
    conn,
    server_address,
    certfile=None,
    keyfile=None,
    minimum_ssl_version=ssl.TLSVersion.TLSv1_2,
    maximum_ssl_version=ssl.TLSVersion.TLSv1_3,
):
    if isinstance(server_address, str):
        listener = await anyio.create_unix_listener(server_address)
    else:
        host, port = server_address
        listener = await anyio.create_tcp_listener(local_host=host, local_port=port)

    if certfile:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.minimum_version = minimum_ssl_version
        context.maximum_version = maximum_ssl_version
        context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        listener = TLSListener(listener, context, standard_compatible=False)

    finished = anyio.Event()

    async def _handler(server):
        async with server as client:
            await _valkey_request_handler(client)
        finished.set()

    async def _serve(*, task_status: TaskStatus = anyio.TASK_STATUS_IGNORED):
        async with listener as server:
            task_status.started()
            await server.serve(_handler)

    async with anyio.create_task_group() as tg:
        await tg.start(_serve)
        await conn.connect()
        await conn.disconnect()
        await finished.wait()
        tg.cancel_scope.cancel()


async def _valkey_request_handler(client):
    buffer = b""
    command = None
    command_ptr = None
    fragment_length = None
    while True:
        try:
            with anyio.move_on_after(0.5):
                buffer += await client.receive(1024)
        except anyio.EndOfStream:
            break
        parts = re.split(_CMD_SEP, buffer)
        buffer = parts[-1]
        for fragment in parts[:-1]:
            fragment = fragment.decode()
            _logger.info("Command fragment: %s", fragment)

            if fragment.startswith("*") and command is None:
                command = [None for _ in range(int(fragment[1:]))]
                command_ptr = 0
                fragment_length = None
                continue

            if fragment.startswith("$") and command[command_ptr] is None:
                fragment_length = int(fragment[1:])
                continue

            assert len(fragment) == fragment_length
            command[command_ptr] = fragment
            command_ptr += 1

            if command_ptr < len(command):
                continue

            command = " ".join(command)
            _logger.info("Command %s", command)
            resp = _SUPPORTED_CMDS.get(command, _ERROR_RESP)
            _logger.info("Response from %s", resp)
            await client.send(resp)
            command = None
    _logger.info("Exit handler")
