import pytest

from tests.standalone import worker_database


@pytest.mark.onlynoncluster
async def test_clients_share_database(request, r, r2, decoded_r, connect_args):
    db = worker_database(request.config)
    clients = (r, r2, decoded_r)
    databases = [
        client.connection_pool.connection_kwargs.get("db", 0) for client in clients
    ]
    assert len(set(databases)) == 1
    if db is not None:
        assert databases == [db] * 3
        assert connect_args["db"] == db
    await r.set("isolation-sentinel", "present")
    assert await r2.get("isolation-sentinel") == b"present"
    assert await decoded_r.get("isolation-sentinel") == "present"
