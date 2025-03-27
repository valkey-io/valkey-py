# https://github.com/pyinvoke/invoke/issues/833
import inspect
import os
import shutil

from invoke import run, task

if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec


@task
def devenv(c):
    """Brings up the test environment, by wrapping docker compose."""
    clean(c)
    cmd = "docker compose --profile all up -d"
    run(cmd)


@task
def build_docs(c):
    """Generates the sphinx documentation."""
    run("pip install -r docs/requirements.txt")
    run("make -C docs html")


@task
def linters(c, color=False):
    """Run code linters"""
    run(f"flake8 --color {'always' if color else 'never'} tests valkey")
    run(
        f"black {'--color' if color else ''} --target-version py38 --check --diff tests valkey"
    )
    run(f"isort {'--color' if color else ''} --check-only --diff tests valkey")
    run("vulture valkey whitelist.py --min-confidence 80")
    run("flynt --fail-on-change --dry-run tests valkey")


@task
def all_tests(c, color=False):
    """Run all linters, and tests in valkey-py."""
    linters(c, color=color)
    tests(c, color=color)


@task(iterable=["async_backend"])
def tests(c, async_backend, protocol=2, color=False):
    """Run the valkey-py test suite against the current python,
    with and without libvalkey.
    """
    print("Starting Valkey tests")
    standalone_tests(c, async_backend=async_backend, protocol=protocol, color=color)
    cluster_tests(c, async_backend=async_backend, protocol=protocol, color=color)


@task(iterable=["async_backend"])
def standalone_tests(c, async_backend, protocol=2, color=False):
    """Run tests against a standalone valkey instance"""
    aopts = f"--async-backend={' '.join(async_backend)}" if async_backend else ""
    run(
        f"pytest --color={'yes' if color else 'no'} --protocol={protocol} --cov=./ --cov-report=xml:coverage_valkey.xml -W always -m 'not onlycluster' {aopts} --junit-xml=standalone-results.xml"
    )


@task(iterable=["async_backend"])
def cluster_tests(c, async_backend, protocol=2, color=False):
    """Run tests against a valkey cluster"""
    cluster_url = "valkey://localhost:16379/0"
    aopts = f"--async-backend={' '.join(async_backend)}" if async_backend else ""
    run(
        f"pytest --color={'yes' if color else 'no'} --protocol={protocol} --cov=./ --cov-report=xml:coverage_clusteclient.xml -W always -m 'not onlynoncluster and not valkeymod' --valkey-url={cluster_url} {aopts} --junit-xml=cluster-results.xml"
    )


@task
def clean(c):
    """Stop all dockers, and clean up the built binaries, if generated."""
    if os.path.isdir("build"):
        shutil.rmtree("build")
    if os.path.isdir("dist"):
        shutil.rmtree("dist")
    run("docker compose --profile all rm -s -f")


@task
def package(c):
    """Create the python packages"""
    run("python setup.py sdist bdist_wheel")
