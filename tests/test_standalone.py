"""Safety checks for standalone database isolation."""

from types import SimpleNamespace
from unittest.mock import Mock

import pytest

import valkey
from tests import standalone


def config(phase=None, worker=None):
    options = {
        "standalone_phase": phase,
        "valkey_url": "valkey://localhost:6379/0",
    }
    result = SimpleNamespace(getoption=options.get, hook=Mock())
    if worker is not None:
        result.workerinput = {"workerid": worker, "workercount": 16}
    return result


@pytest.mark.parametrize(
    "phase,worker,db",
    [
        (None, None, 9),
        ("exclusive", None, 9),
        ("parallel", None, 9),
        ("parallel", "gw0", 0),
        ("parallel", "gw15", 15),
    ],
)
def test_database_routing(phase, worker, db):
    options = standalone.connection_options(
        config(phase, worker), "valkey://localhost/5?db=7", db=9
    )
    assert options["db"] == db


def test_worker_database_overflow():
    with pytest.raises(pytest.UsageError):
        standalone.worker_database(config("parallel", "gw16"))


def test_startup_and_shutdown_cleanup(monkeypatch):
    client = Mock()
    factory = Mock()
    factory.return_value.__enter__ = Mock(return_value=client)
    factory.return_value.__exit__ = Mock(return_value=False)
    monkeypatch.setattr(valkey, "Valkey", factory)
    request = SimpleNamespace(config=config("parallel", "gw15"))
    fixture = standalone.isolated_database.__wrapped__(request)
    next(fixture)
    assert factory.call_args.kwargs["db"] == 15
    assert client.flushdb.call_count == 1
    fixture.close()
    assert client.flushdb.call_count == 2


@pytest.mark.parametrize("phase", ["parallel", "exclusive"])
def test_phase_partition(phase):
    def item(*markers):
        return SimpleNamespace(
            get_closest_marker=lambda name: True if name in markers else None
        )

    safe = item()
    exclusive = item("standalone_exclusive")
    cluster = item("onlycluster")
    items = [safe, exclusive, cluster]
    cfg = config(phase)
    standalone.pytest_collection_modifyitems(cfg, items)
    assert items == ([safe] if phase == "parallel" else [exclusive])


@pytest.mark.onlynoncluster
def test_clients_share_database(request, r, r2, decoded_r):
    db = standalone.worker_database(request.config)
    clients = (r, r2, decoded_r)
    databases = [
        client.connection_pool.connection_kwargs.get("db", 0) for client in clients
    ]
    assert len(set(databases)) == 1
    if db is not None:
        assert databases == [db] * 3
    r.set("isolation-sentinel", "present")
    assert r2.get("isolation-sentinel") == b"present"
    assert decoded_r.get("isolation-sentinel") == "present"
