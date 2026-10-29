"""Run isolated standalone workers, then the exclusive remainder."""

import os
import shlex
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import coverage


def validate_args(args):
    """Keep runner-owned options out of both phases."""
    reserved = (
        "--numprocesses",
        "--dist",
        "--tx",
        "--px",
        "--maxprocesses",
        "--maxschedchunk",
        "--max-worker-restart",
        "--standalone-",
        "--cov",
        "--junit",
    )
    for arg in args:
        if arg.startswith(reserved) or (arg.startswith("-n") and arg != "--"):
            raise ValueError(
                f"Combined target manages or does not support {arg!r}; "
                "use pytest directly"
            )


def run_phase(command, env):
    """Reap the owned process group before returning, including on interruption."""
    process = subprocess.Popen(command, env=env, start_new_session=True)
    try:
        return process.wait()
    finally:
        # Workers must never survive into the exclusive phase.
        if process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGTERM)
                process.wait(timeout=10)
            except (ProcessLookupError, subprocess.TimeoutExpired):
                pass
        # Also kill any workers left behind after their controller exited.
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()


def main():
    try:
        workers = int(sys.argv[1])
        args = sys.argv[2:]
        validate_args(args + shlex.split(os.environ.get("PYTEST_ADDOPTS", "")))
    except (ValueError, IndexError) as error:
        print(error, file=sys.stderr)
        return 4

    infix = "-uvloop" if "--uvloop" in args else ""
    result = 0
    with tempfile.TemporaryDirectory(prefix="valkey-standalone-") as directory:
        data_files = []
        for phase in ("parallel", "exclusive"):
            data = Path(directory) / f".coverage.{phase}"
            env = {**os.environ, "COVERAGE_FILE": str(data)}
            command = [
                sys.executable,
                "-m",
                "pytest",
                *args,
                f"--standalone-phase={phase}",
                "-n",
                str(workers if phase == "parallel" else 0),
                "--dist=load" if phase == "parallel" else "--dist=no",
                "--max-worker-restart=0",
                "--maxschedchunk=1",
                "--cov=./",
                "--cov-report=",
                f"--junit-xml=standalone{infix}-{phase}-results.xml",
            ]
            start = time.perf_counter()
            code = run_phase(command, env)
            if code == 5:  # An empty phase is valid for focused selections.
                code = 0
            print(f"Standalone {phase}: {time.perf_counter() - start:.2f}s", flush=True)
            result = result or code
            if data.exists():
                data_files.append(str(data))
            if code not in (0, 1):
                break
        if data_files:
            cov = coverage.Coverage()
            cov.combine(data_files)
            cov.save()
            cov.xml_report(outfile="coverage_valkey.xml")
    return result


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal.default_int_handler)
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
