import argparse
import math
import time
from collections.abc import Callable
from typing import TypeVar
from unittest import mock
from unittest.mock import Mock
from urllib.parse import urlparse

import pytest
import valkey
from packaging.version import Version
from valkey import Sentinel
from valkey.backoff import NoBackoff
from valkey.connection import Connection, parse_url
from valkey.exceptions import ValkeyClusterException
from valkey.retry import Retry

VALKEY_INFO = {}
default_valkey_url = "valkey://localhost:6379/0"
default_protocol = "2"
default_valkeymod_url = "valkey://localhost:6379"

# default ssl client ignores verification for the purpose of testing
default_valkey_ssl_url = "valkeys://localhost:6666"
default_cluster_nodes = 6

_DecoratedTest = TypeVar("_DecoratedTest", bound="Callable")
_TestDecorator = Callable[[_DecoratedTest], _DecoratedTest]


# Taken from python3.9
class BooleanOptionalAction(argparse.Action):
    def __init__(
        self,
        option_strings,
        dest,
        default=None,
        type=None,
        choices=None,
        required=False,
        help=None,
        metavar=None,
    ):
        _option_strings = []
        for option_string in option_strings:
            _option_strings.append(option_string)

            if option_string.startswith("--"):
                option_string = "--no-" + option_string[2:]
                _option_strings.append(option_string)

        if help is not None and default is not None:
            help += f" (default: {default})"

        super().__init__(
            option_strings=_option_strings,
            dest=dest,
            nargs=0,
            default=default,
            type=type,
            choices=choices,
            required=required,
            help=help,
            metavar=metavar,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        if option_string in self.option_strings:
            setattr(namespace, self.dest, not option_string.startswith("--no-"))

    def format_usage(self):
        return " | ".join(self.option_strings)


def pytest_addoption(parser):
    parser.addoption(
        "--valkey-url",
        default=default_valkey_url,
        action="store",
        help="Valkey connection string, defaults to `%(default)s`",
    )

    parser.addoption(
        "--protocol",
        default=default_protocol,
        action="store",
        help="Protocol version, defaults to `%(default)s`",
    )
    parser.addoption(
        "--valkey-ssl-url",
        default=default_valkey_ssl_url,
        action="store",
        help="Valkey SSL connection string, defaults to `%(default)s`",
    )

    parser.addoption(
        "--valkey-cluster-nodes",
        default=default_cluster_nodes,
        action="store",
        help="The number of cluster nodes that need to be "
        "available before the test can start,"
        " defaults to `%(default)s`",
    )

    parser.addoption(
        "--uvloop", action=BooleanOptionalAction, help="Run tests with uvloop"
    )

    parser.addoption(
        "--sentinels",
        action="store",
        default="localhost:26379,localhost:26380,localhost:26381",
        help="Comma-separated list of sentinel IPs and ports",
    )
    parser.addoption(
        "--master-service",
        action="store",
        default="valkey-py-test",
        help="Name of the Valkey master service that the sentinels are monitoring",
    )


def _get_info(valkey_url):
    client = valkey.Valkey.from_url(valkey_url)
    info = client.info()
    client.connection_pool.disconnect()
    return info


def pytest_sessionstart(session):
    # during test discovery, e.g. with VS Code, we may not
    # have a server running.
    valkey_url = session.config.getoption("--valkey-url")
    try:
        info = _get_info(valkey_url)
        version = info["valkey_version"]
        arch_bits = info["arch_bits"]
        cluster_enabled = info["cluster_enabled"]
    except valkey.ConnectionError:
        # provide optimistic defaults
        info = {}
        version = "10.0.0"
        arch_bits = 64
        cluster_enabled = False
    VALKEY_INFO["version"] = version
    VALKEY_INFO["arch_bits"] = arch_bits
    VALKEY_INFO["cluster_enabled"] = cluster_enabled
    # store VALKEY_INFO in config so that it is available from "condition strings"
    session.config.VALKEY_INFO = VALKEY_INFO

    # module info
    try:
        VALKEY_INFO["modules"] = info["modules"]
    except (KeyError, valkey.exceptions.ConnectionError):
        pass

    if cluster_enabled:
        cluster_nodes = session.config.getoption("--valkey-cluster-nodes")
        wait_for_cluster_creation(valkey_url, cluster_nodes)

    use_uvloop = session.config.getoption("--uvloop")

    if use_uvloop:
        try:
            import uvloop

            uvloop.install()
        except ImportError as e:
            raise RuntimeError("Cannot import uvloop, make sure it is installed") from e


def wait_for_cluster_creation(valkey_url, cluster_nodes, timeout=60):
    """Waits for the cluster creation to complete.
    As soon as all :cluster_nodes: nodes become available, the cluster will be
    considered ready.
    :param valkey_url: the cluster's url, e.g. valkey://localhost:16379/0
    :param cluster_nodes: The number of nodes in the cluster
    :param timeout: the amount of time to wait (in seconds).
    """
    now = time.time()
    end_time = now + timeout
    client = None
    print(f"Waiting for {cluster_nodes} cluster nodes to become available")
    while now < end_time:
        try:
            client = valkey.ValkeyCluster.from_url(valkey_url)
            if len(client.get_nodes()) == int(cluster_nodes):
                print("All nodes are available!")
                break
        except ValkeyClusterException:
            pass
        time.sleep(1)
        now = time.time()
    if now >= end_time:
        available_nodes = 0 if client is None else len(client.get_nodes())
        raise ValkeyClusterException(
            f"The cluster did not become available after {timeout} seconds. "
            f"Only {available_nodes} nodes out of {cluster_nodes} are available"
        )


def skip_if_server_version_lt(min_version: str) -> _TestDecorator:
    valkey_version = VALKEY_INFO.get("version", "0")
    check = Version(valkey_version) < Version(min_version)
    return pytest.mark.skipif(check, reason=f"Valkey version required >= {min_version}")


def skip_if_server_version_gte(min_version: str) -> _TestDecorator:
    valkey_version = VALKEY_INFO.get("version", "0")
    check = Version(valkey_version) >= Version(min_version)
    return pytest.mark.skipif(check, reason=f"Valkey version required < {min_version}")


def skip_if_version_is_one_of(versions: list[str]) -> _TestDecorator:
    valkey_version = VALKEY_INFO.get("version", "0")
    check = Version(valkey_version) in [Version(v) for v in versions]
    return pytest.mark.skipif(
        check, reason=f"Valkey version required not in {versions}"
    )


def skip_unless_arch_bits(arch_bits: int) -> _TestDecorator:
    return pytest.mark.skipif(
        VALKEY_INFO.get("arch_bits", "") != arch_bits,
        reason=f"server is not {arch_bits}-bit",
    )


def skip_ifmodversion_lt(min_version: str, module_name: str):
    try:
        modules = VALKEY_INFO["modules"]
    except KeyError:
        return pytest.mark.skipif(True, reason="Valkey server does not have modules")
    if modules == []:
        return pytest.mark.skipif(True, reason="No valkey modules found")

    for j in modules:
        if module_name == j.get("name"):
            version = j.get("ver")
            mv = int(
                "".join([f"{int(segment):02}" for segment in min_version.split(".")])
            )
            check = version < mv
            return pytest.mark.skipif(check, reason="Valkey module version")

    raise AttributeError(f"No valkey module named {module_name}")


def skip_if_nocryptography() -> _TestDecorator:
    try:
        import cryptography  # noqa

        return pytest.mark.skipif(False, reason="Cryptography dependency found")
    except ImportError:
        return pytest.mark.skipif(True, reason="No cryptography dependency")


def skip_if_cryptography() -> _TestDecorator:
    try:
        import cryptography  # noqa

        return pytest.mark.skipif(True, reason="Cryptography dependency found")
    except ImportError:
        return pytest.mark.skipif(False, reason="No cryptography dependency")


def _get_client(
    cls, request, single_connection_client=True, flushdb=True, from_url=None, **kwargs
):
    """Helper for fixtures or tests that need a Valkey client.

    Uses the "--valkey-url" command line argument for connection info. Unlike
    ConnectionPool.from_url, keyword arguments to this function override
    values specified in the URL.
    """
    if from_url is None:
        valkey_url = request.config.getoption("--valkey-url")
    else:
        valkey_url = from_url
    if "protocol" not in valkey_url and kwargs.get("protocol") is None:
        kwargs["protocol"] = request.config.getoption("--protocol")

    cluster_mode = VALKEY_INFO["cluster_enabled"]
    if not cluster_mode:
        url_options = parse_url(valkey_url)
        url_options.update(kwargs)
        pool = valkey.ConnectionPool(**url_options)
        client = cls(connection_pool=pool)
    else:
        client = valkey.ValkeyCluster.from_url(valkey_url, **kwargs)
        single_connection_client = False
    if single_connection_client:
        client = client.client()
    if request:

        def teardown():
            if not cluster_mode:
                if flushdb:
                    try:
                        client.flushdb()
                    except valkey.ConnectionError:
                        # handle cases where a test disconnected a client
                        # just manually retry the flushdb
                        client.flushdb()
                client.close()
                client.connection_pool.disconnect()
            else:
                cluster_teardown(client, flushdb)

        request.addfinalizer(teardown)
    return client


def cluster_teardown(client, flushdb):
    if flushdb:
        try:
            client.flushdb(target_nodes="primaries")
        except valkey.ConnectionError:
            # handle cases where a test disconnected a client
            # just manually retry the flushdb
            client.flushdb(target_nodes="primaries")
    client.close()
    client.disconnect_connection_pools()


@pytest.fixture
def r(request):
    with _get_client(valkey.Valkey, request) as client:
        yield client


@pytest.fixture
def decoded_r(request):
    with _get_client(valkey.Valkey, request, decode_responses=True) as client:
        yield client


@pytest.fixture
def r_timeout(request):
    with _get_client(valkey.Valkey, request, socket_timeout=1) as client:
        yield client


@pytest.fixture
def r2(request):
    """A second client for tests that need multiple."""
    with _get_client(valkey.Valkey, request) as client:
        yield client


@pytest.fixture
def sslclient(request):
    with _get_client(valkey.Valkey, request, ssl=True) as client:
        yield client


@pytest.fixture
def sentinel_setup(local_cache, request):
    sentinel_ips = request.config.getoption("--sentinels")
    sentinel_endpoints = [
        (ip.strip(), int(port.strip()))
        for ip, port in (endpoint.split(":") for endpoint in sentinel_ips.split(","))
    ]
    kwargs = request.param.get("kwargs", {}) if hasattr(request, "param") else {}
    sentinel = Sentinel(
        sentinel_endpoints,
        socket_timeout=0.1,
        client_cache=local_cache,
        protocol=3,
        **kwargs,
    )
    yield sentinel
    for s in sentinel.sentinels:
        s.close()


@pytest.fixture
def master(request, sentinel_setup):
    master_service = request.config.getoption("--master-service")
    master = sentinel_setup.master_for(master_service)
    yield master
    master.close()


def _gen_cluster_mock_resp(r, response):
    connection = Mock(spec=Connection)
    connection.retry = Retry(NoBackoff(), 0)
    connection.read_response.return_value = response
    connection._get_from_local_cache.return_value = None
    with mock.patch.object(r, "connection", connection):
        yield r


@pytest.fixture
def mock_cluster_resp_ok(request, **kwargs):
    r = _get_client(valkey.Valkey, request, **kwargs)
    yield from _gen_cluster_mock_resp(r, "OK")


@pytest.fixture
def mock_cluster_resp_int(request, **kwargs):
    r = _get_client(valkey.Valkey, request, **kwargs)
    yield from _gen_cluster_mock_resp(r, 2)


@pytest.fixture
def mock_cluster_resp_info(request, **kwargs):
    r = _get_client(valkey.Valkey, request, **kwargs)
    response = (
        "cluster_state:ok\r\ncluster_slots_assigned:16384\r\n"
        "cluster_slots_ok:16384\r\ncluster_slots_pfail:0\r\n"
        "cluster_slots_fail:0\r\ncluster_known_nodes:7\r\n"
        "cluster_size:3\r\ncluster_current_epoch:7\r\n"
        "cluster_my_epoch:2\r\ncluster_stats_messages_sent:170262\r\n"
        "cluster_stats_messages_received:105653\r\n"
    )
    yield from _gen_cluster_mock_resp(r, response)


@pytest.fixture
def mock_cluster_resp_nodes(request, **kwargs):
    r = _get_client(valkey.Valkey, request, **kwargs)
    response = (
        "c8253bae761cb1ecb2b61857d85dfe455a0fec8b 172.17.0.7:7006 "
        "slave aa90da731f673a99617dfe930306549a09f83a6b 0 "
        "1447836263059 5 connected\n"
        "9bd595fe4821a0e8d6b99d70faa660638a7612b3 172.17.0.7:7008 "
        "master - 0 1447836264065 0 connected\n"
        "aa90da731f673a99617dfe930306549a09f83a6b 172.17.0.7:7003 "
        "myself,master - 0 0 2 connected 5461-10922\n"
        "1df047e5a594f945d82fc140be97a1452bcbf93e 172.17.0.7:7007 "
        "slave 19efe5a631f3296fdf21a5441680f893e8cc96ec 0 "
        "1447836262556 3 connected\n"
        "4ad9a12e63e8f0207025eeba2354bcf4c85e5b22 172.17.0.7:7005 "
        "master - 0 1447836262555 7 connected 0-5460\n"
        "19efe5a631f3296fdf21a5441680f893e8cc96ec 172.17.0.7:7004 "
        "master - 0 1447836263562 3 connected 10923-16383\n"
        "fbb23ed8cfa23f17eaf27ff7d0c410492a1093d6 172.17.0.7:7002 "
        "master,fail - 1447829446956 1447829444948 1 disconnected\n"
    )
    yield from _gen_cluster_mock_resp(r, response)


@pytest.fixture
def mock_cluster_resp_slaves(request, **kwargs):
    r = _get_client(valkey.Valkey, request, **kwargs)
    response = (
        "['1df047e5a594f945d82fc140be97a1452bcbf93e 172.17.0.7:7007 "
        "slave 19efe5a631f3296fdf21a5441680f893e8cc96ec 0 "
        "1447836789290 3 connected']"
    )
    yield from _gen_cluster_mock_resp(r, response)


@pytest.fixture(scope="session")
def master_host(request):
    url = request.config.getoption("--valkey-url")
    parts = urlparse(url)
    return parts.hostname, (parts.port or 6379)


@pytest.fixture
def valkey_version():
    return Version(VALKEY_INFO["version"])


def wait_for_command(client, monitor, command, key=None):
    # issue a command with a key name that's local to this process.
    # if we find a command with our key before the command we're waiting
    # for, something went wrong
    if key is None:
        # generate key
        id_str = str(client.client_id())
        key = f"__VALKEY-PY-{id_str}__"
    client.get(key)
    while True:
        monitor_response = monitor.next_command()
        if command in monitor_response["command"]:
            return monitor_response
        if key in monitor_response["command"]:
            return None


def is_resp2_connection(r):
    if isinstance(r, valkey.Valkey) or isinstance(r, valkey.asyncio.Valkey):
        protocol = r.connection_pool.connection_kwargs.get("protocol")
    elif isinstance(r, valkey.cluster.AbstractValkeyCluster):
        protocol = r.nodes_manager.connection_kwargs.get("protocol")
    return protocol in ["2", 2, None]


def get_protocol_version(r):
    if isinstance(r, valkey.Valkey) or isinstance(r, valkey.asyncio.Valkey):
        return r.connection_pool.connection_kwargs.get("protocol")
    elif isinstance(r, valkey.cluster.AbstractValkeyCluster):
        return r.nodes_manager.connection_kwargs.get("protocol")


def assert_resp_response(r, response, resp2_expected, resp3_expected):
    protocol = get_protocol_version(r)
    if protocol in [2, "2", None]:
        assert response == resp2_expected
    else:
        assert response == resp3_expected


def assert_geo_is_close(coords, expected_coords):
    """Verifies that the coordinates are close within the floating point tolerance.

    Valkey uses 52-bit precision
    """
    for a, b in zip(coords, expected_coords):
        assert math.isclose(a, b)


def assert_resp_response_isclose(r, response, resp2_expected, resp3_expected):
    """Verifies that the responses are close within the floating point tolerance."""
    protocol = get_protocol_version(r)

    if protocol in [2, "2", None]:
        assert_geo_is_close(response[0], resp2_expected[0])
        assert response[1:] == resp2_expected[1:]
    else:
        assert_geo_is_close(response[0], resp3_expected[0])
        assert response[1:] == resp3_expected[1:]


def assert_resp_response_in(r, response, resp2_expected, resp3_expected):
    protocol = get_protocol_version(r)
    if protocol in [2, "2", None]:
        assert response in resp2_expected
    else:
        assert response in resp3_expected
