import contextlib
import multiprocessing

import pytest
import valkey
from valkey.connection import Connection, ConnectionPool
from valkey.exceptions import ConnectionError

from .conftest import _get_client


@contextlib.contextmanager
def exit_callback(callback, *args):
    try:
        yield
    finally:
        callback(*args)


class TestMultiprocessing:
    # Test connection sharing between forks.
    # See issue #1085 for details.

    # use a multi-connection client as that's the only type that is
    # actually fork/process-safe
    @pytest.fixture()
    def r(self, request):
        return _get_client(
            valkey.Valkey, request=request, single_connection_client=False
        )

    @pytest.fixture()
    def multiprocessing_ctx(self):
        curr_start_method = multiprocessing.get_start_method(allow_none=False)
        if curr_start_method == "forkserver":
            return multiprocessing.get_context("fork")
        return multiprocessing.get_context(curr_start_method)

    def test_close_connection_in_child(self, master_host, multiprocessing_ctx):
        """
        A connection owned by a parent and closed by a child doesn't
        destroy the file descriptors so a parent can still use it.
        """
        conn = Connection(host=master_host[0], port=master_host[1])
        conn.send_command("ping")
        assert conn.read_response() == b"PONG"

        def target(conn):
            conn.send_command("ping")
            assert conn.read_response() == b"PONG"
            conn.disconnect()

        proc = multiprocessing_ctx.Process(target=target, args=(conn,))
        proc.start()
        proc.join(3)
        assert proc.exitcode == 0

        # The connection was created in the parent but disconnected in the
        # child. The child called socket.close() but did not call
        # socket.shutdown() because it wasn't the "owning" process.
        # Therefore the connection still works in the parent.
        conn.send_command("ping")
        assert conn.read_response() == b"PONG"

    def test_close_connection_in_parent(self, master_host, multiprocessing_ctx):
        """
        A connection owned by a parent is unusable by a child if the parent
        (the owning process) closes the connection.
        """
        conn = Connection(host=master_host[0], port=master_host[1])
        conn.send_command("ping")
        assert conn.read_response() == b"PONG"

        def target(conn, ev):
            ev.wait()
            # the parent closed the connection. because it also created the
            # connection, the connection is shutdown and the child
            # cannot use it.
            with pytest.raises(ConnectionError):
                conn.send_command("ping")

        ev = multiprocessing.Event()
        proc = multiprocessing_ctx.Process(target=target, args=(conn, ev))
        proc.start()

        conn.disconnect()
        ev.set()

        proc.join(3)
        assert proc.exitcode == 0

    @pytest.mark.parametrize("max_connections", [1, 2, None])
    def test_pool(self, max_connections, master_host, multiprocessing_ctx):
        """
        A child will create its own connections when using a pool created
        by a parent.
        """
        pool = ConnectionPool.from_url(
            f"valkey://{master_host[0]}:{master_host[1]}",
            max_connections=max_connections,
        )

        conn = pool.get_connection("ping")
        main_conn_pid = conn.pid
        with exit_callback(pool.release, conn):
            conn.send_command("ping")
            assert conn.read_response() == b"PONG"

        def target(pool):
            with exit_callback(pool.disconnect):
                conn = pool.get_connection("ping")
                assert conn.pid != main_conn_pid
                with exit_callback(pool.release, conn):
                    assert conn.send_command("ping") is None
                    assert conn.read_response() == b"PONG"

        proc = multiprocessing_ctx.Process(target=target, args=(pool,))
        proc.start()
        proc.join(3)
        assert proc.exitcode == 0

        # Check that connection is still alive after fork process has exited
        # and disconnected the connections in its pool
        conn = pool.get_connection("ping")
        with exit_callback(pool.release, conn):
            assert conn.send_command("ping") is None
            assert conn.read_response() == b"PONG"

    @pytest.mark.parametrize("max_connections", [1, 2, None])
    def test_close_pool_in_main(
        self, max_connections, master_host, multiprocessing_ctx
    ):
        """
        A child process that uses the same pool as its parent isn't affected
        when the parent disconnects all connections within the pool.
        """
        pool = ConnectionPool.from_url(
            f"valkey://{master_host[0]}:{master_host[1]}",
            max_connections=max_connections,
        )

        conn = pool.get_connection("ping")
        assert conn.send_command("ping") is None
        assert conn.read_response() == b"PONG"

        def target(pool, disconnect_event):
            conn = pool.get_connection("ping")
            with exit_callback(pool.release, conn):
                assert conn.send_command("ping") is None
                assert conn.read_response() == b"PONG"
                disconnect_event.wait()
                assert conn.send_command("ping") is None
                assert conn.read_response() == b"PONG"

        ev = multiprocessing.Event()

        proc = multiprocessing_ctx.Process(target=target, args=(pool, ev))
        proc.start()

        pool.disconnect()
        ev.set()
        proc.join(3)
        assert proc.exitcode == 0

    def test_valkey_client(self, r, multiprocessing_ctx):
        "A valkey client created in a parent can also be used in a child"
        assert r.ping() is True

        def target(client):
            assert client.ping() is True
            del client

        proc = multiprocessing_ctx.Process(target=target, args=(r,))
        proc.start()
        proc.join(3)
        assert proc.exitcode == 0

        assert r.ping() is True
