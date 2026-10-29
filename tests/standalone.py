"""Standalone phase selection and per-worker database isolation."""

import os

import pytest

import valkey
from valkey.connection import parse_url


def pytest_addoption(parser):
    group = parser.getgroup("standalone parallel tests")
    group.addoption("--standalone-phase", choices=("parallel", "exclusive"))


def worker_database(config):
    """Return a database only for an explicitly isolated standalone worker."""
    if config.getoption("standalone_phase") != "parallel":
        return None
    worker = getattr(config, "workerinput", None)
    if worker is None:
        return None
    name = worker["workerid"]
    if not name.startswith("gw") or not name[2:].isdigit():
        raise pytest.UsageError(f"Unsupported worker identity: {name}")
    db = int(name[2:])
    if not 0 <= db < worker["workercount"]:
        raise pytest.UsageError(f"Worker {name} has no allocated database")
    return db


def worker_name(name: str) -> str:
    """Namespace resources such as Pub/Sub channels that SELECT cannot isolate."""
    worker = os.environ.get("PYTEST_XDIST_WORKER")
    return f"{worker}:{name}" if worker else name


def connection_options(config, url, **kwargs):
    """Preserve factory precedence, then apply the isolated worker database."""
    options = parse_url(url)
    options.update(kwargs)
    db = worker_database(config)
    if db is not None:
        options["db"] = db
    return options


def pytest_configure(config):
    config._standalone_error = False
    phase = config.getoption("standalone_phase")
    if not phase:
        return
    if config.getoption("lf", False) or config.getoption("stepwise", False):
        raise pytest.UsageError("Use pytest directly for --lf/--sw selection")
    if hasattr(config, "workerinput"):
        return
    workers = config.getoption("numprocesses", 0) or 0
    if phase == "exclusive":
        if workers or config.getoption("dist", "no") != "no":
            raise pytest.UsageError("The exclusive phase must run without xdist")
    elif (
        not isinstance(workers, int)
        or workers < 1
        or config.getoption("dist", "no") != "load"
        or str(config.getoption("maxworkerrestart", None)) != "0"
    ):
        raise pytest.UsageError(
            "Parallel standalone tests require a positive worker count, --dist=load, "
            "and --max-worker-restart=0"
        )


def preflight(config, info):
    """Validate isolation using the existing session server-information lookup."""
    if not config.getoption("standalone_phase"):
        return
    url = config.getoption("valkey_url")
    if info["cluster_enabled"]:
        raise pytest.UsageError("Standalone phase execution rejects Cluster")
    if (
        hasattr(config, "workerinput")
        or config.getoption("standalone_phase") != "parallel"
    ):
        return
    try:
        with valkey.Valkey.from_url(url) as client:
            capacity = int(client.config_get("databases")["databases"])
        workers = config.getoption("numprocesses")
        if workers > capacity:
            raise pytest.UsageError(
                f"Requested {workers} workers, but server has {capacity} databases"
            )
    except (valkey.ValkeyError, KeyError, TypeError, ValueError) as error:
        raise pytest.UsageError(
            f"Standalone isolation preflight failed: {error}"
        ) from error


def pytest_collection_modifyitems(config, items):
    phase = config.getoption("standalone_phase")
    if not phase:
        return
    selected, deselected = [], []
    for item in items:
        safe = item.get_closest_marker("standalone_exclusive") is None
        keep = not item.get_closest_marker("onlycluster") and (
            safe == (phase == "parallel")
        )
        (selected if keep else deselected).append(item)
    items[:] = selected
    config.hook.pytest_deselected(items=deselected)


@pytest.hookimpl(wrapper=True)
def pytest_make_collect_report(collector):
    report = yield
    if report.failed:
        collector.config._standalone_error = True
    return report


@pytest.hookimpl(optionalhook=True)
def pytest_testnodedown(node, error):
    node.config._standalone_error |= bool(
        error or getattr(node, "workeroutput", {}).get("standalone_error", False)
    )


@pytest.hookimpl(wrapper=True)
def pytest_sessionfinish(session, exitstatus):
    yield
    config = session.config
    if config.getoption("standalone_phase"):
        if hasattr(config, "workerinput"):
            config.workeroutput["standalone_error"] = config._standalone_error
        elif config._standalone_error or (
            session.testsfailed and not session.testscollected
        ):
            session.exitstatus = pytest.ExitCode.INTERNAL_ERROR


@pytest.fixture(scope="session", autouse=True)
def isolated_database(request):
    db = worker_database(request.config)
    if db is None:
        yield
        return
    options = connection_options(request.config, request.config.getoption("valkey_url"))
    with valkey.Valkey(**options) as client:
        client.flushdb()
        try:
            yield
        finally:
            client.flushdb()
