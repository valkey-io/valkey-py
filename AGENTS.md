# Repository guidance

valkey-py is a Python client for Valkey, supporting synchronous and
asynchronous clients, standalone servers, clusters, and Sentinel.
Python 3.11 or newer is required.

Read CONTRIBUTING.md before contributing. It documents the development
workflow, documentation conventions, and DCO requirements.

## Repository layout

- valkey/: synchronous clients and shared utilities.
- valkey/asyncio/: asynchronous clients and transport implementations.
- valkey/commands/: command mixins and module command namespaces, including
  shared implementations and async-specific overrides.
- valkey/_parsers/: protocol parsers, response callbacks, and command parsing.
- tests/: synchronous tests, shared fixtures, and parser tests.
- tests/test_asyncio/: asynchronous tests and fixtures.
- docs/: Sphinx documentation.
- dockers/ and compose.yaml: integration-test services.
- Makefile: development, verification, documentation, and packaging commands.
- pyproject.toml: dependencies, pytest settings, and typing configuration.
- .github/workflows/integration.yaml: CI verification matrix.

## Making changes

- Follow the structure and conventions of nearby code.
- Keep changes focused; avoid unrelated refactoring or formatting.
- Preserve public API compatibility unless the task explicitly requires
  a breaking change.
- Inspect shared mixins, inheritance, and overrides before introducing
  new implementations.
- For command changes, check argument construction, validation, return
  types, response callbacks, and relevant pipeline/cluster behavior.
- For connection and execution changes, consider retry behavior,
  exception handling, and resource cleanup.
- Preserve existing RESP2/RESP3 handling, decoding behavior, and support
  for the pure-Python and optional libvalkey parsers where relevant.

## Synchronous and asynchronous clients

- Features and fixes applicable to both clients must work in both.
- Inspect corresponding implementations in valkey/ and valkey/asyncio/.
  Shared code may cover both; async overrides may require separate changes.
- Add or update tests in both suites when the behavior applies to both,
  including when only shared implementation code changes.
- Preserve intentional differences in awaiting, iteration, cancellation,
  and resource cleanup.
- Explain when a change or test applies to only one client.

## Testing

- Run integration tests only against disposable test instances. Fixtures
  flush databases, including cluster primaries; never point tests at
  production or shared instances containing valuable data.
- Add regression tests for bug fixes and coverage for new behavior.
- Use existing fixtures and helpers in tests/conftest.py and
  tests/test_asyncio/conftest.py.
- Follow nearby tests for client creation, mocking, and cleanup.
- Use existing server-version guards and standalone/cluster markers.
  Do not broadly skip tests to make a failing change pass.
- Check both RESP2 and RESP3 when protocol-dependent behavior changes.
- Run focused tests during development, then broader relevant suites.
- Report checks run, failures, skips, and environment limitations.
  Never claim checks passed if they were not run.

## Development commands

Use a virtual environment and pip 25.1 or newer (required for --group):

    python -m venv .venv
    source .venv/bin/activate
    pip install --group dev
    pip install -e .

Integration tests generally require running Valkey services. The Docker-based
development environment requires Docker and Docker Compose v2.20.2 or newer:

    make devenv

Caution: make devenv first runs make clean, deleting build/dist and
stopping/removing the Compose containers. Do not use it when existing
environment state needs to be preserved.

Choose verification appropriate to the change; these targets are
alternatives or combinations, not a checklist to run in sequence:

- make standalone-tests: standalone tests, including sync and async.
- make cluster-tests: cluster tests, including sync and async.
- make tests: both standalone-tests and cluster-tests.
- make linters: formatting and lint checks.
- make all-tests: linters plus both test targets.

Do not rerun constituent targets after a combined target has already
covered them unless changes, failures, or a different configuration
require verification.
Documentation-only changes do not require the Python test suites.
The test targets do not start the required services.

Use ADDITIONAL_PYTEST_ARGS for focused runs, for example:

    make standalone-tests ADDITIONAL_PYTEST_ARGS="tests/test_commands.py tests/test_asyncio/test_commands.py -k test_name"

Use PROTOCOL=2 or PROTOCOL=3 to select the protocol.
Use USE_UVLOOP=1 when checking event-loop-sensitive async changes.

For typing changes, install the type-check dependency group and run mypy.
Consult the CI workflow for the complete verification matrix.

## Style and documentation

- Follow the existing Black, isort, and flake8 configuration.
- Add appropriate type hints; follow nearby sync/async typing patterns.
- Prefer Google-style docstrings without repeating types already expressed
  by annotations.
- Update docstrings and docs/ for public API or behavior changes.
- Build documentation with make build-docs when relevant.
- Follow CONTRIBUTING.md's DCO requirements when creating commits.
