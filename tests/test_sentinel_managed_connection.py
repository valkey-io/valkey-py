import time
from unittest import mock

import pytest

import valkey
from valkey.sentinel import SentinelManagedConnection

DEMOTION_ERROR = (
    "UNBLOCKED force unblock from blocking operation, "
    "instance state changed (master -> replica?)"
)


class TestSentinelManagedConnectionDemotedMaster:
    """
    A master that becomes a replica, for instance during a coordinated
    failover, answers every client blocked on BLPOP/BRPOP/XREAD... with an
    UNBLOCKED error and closes the connection. For a master connection this
    means the same as READONLY: the master moved.
    """

    def _connect(self, master_host):
        connection_pool = mock.Mock()
        connection_pool.get_master_address = mock.Mock(
            return_value=(master_host[0], master_host[1])
        )
        connection_pool.is_master = True
        connection_pool.check_connection = False
        conn = SentinelManagedConnection(connection_pool=connection_pool)
        conn.connect()
        return conn

    def test_unblocked_by_demotion_is_a_connection_error(self, master_host):
        conn = self._connect(master_host)
        try:
            conn.send_command("PING")
            with mock.patch.object(
                conn._parser,
                "read_response",
                return_value=valkey.ResponseError(DEMOTION_ERROR),
            ):
                with pytest.raises(valkey.ConnectionError) as e:
                    conn.read_response()
            assert str(e.value) == "The previous master is now a slave"
            assert conn._sock is None
        finally:
            conn.disconnect()

    def test_unblocked_by_demotion_on_a_replica_connection_is_raised(self, master_host):
        conn = self._connect(master_host)
        conn.connection_pool.is_master = False
        try:
            conn.send_command("PING")
            with mock.patch.object(
                conn._parser,
                "read_response",
                return_value=valkey.ResponseError(DEMOTION_ERROR),
            ):
                with pytest.raises(valkey.ResponseError) as e:
                    conn.read_response()
            assert not isinstance(e.value, valkey.ConnectionError)
            assert conn._sock is not None
        finally:
            conn.disconnect()

    @pytest.mark.onlynoncluster
    def test_client_unblock_error_is_not_a_demotion(self, master_host):
        """
        CLIENT UNBLOCK ... ERROR also answers UNBLOCKED, with another message:
        the server did not change role, so the error must reach the caller.
        """
        conn = self._connect(master_host)
        admin = valkey.Valkey(host=master_host[0], port=master_host[1])
        try:
            conn.send_command("CLIENT", "ID")
            client_id = conn.read_response()
            conn.send_command("BLPOP", "valkey-py:unblocked-test", 5)
            unblocked = False
            for _ in range(50):
                if admin.client_unblock(client_id, error=True):
                    unblocked = True
                    break
                time.sleep(0.01)
            assert unblocked
            with pytest.raises(valkey.ResponseError) as e:
                conn.read_response()
            assert str(e.value).startswith("UNBLOCKED client unblocked")
            assert not isinstance(e.value, valkey.ConnectionError)
        finally:
            admin.close()
            conn.disconnect()
