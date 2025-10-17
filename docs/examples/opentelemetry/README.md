# Example for valkey-py OpenTelemetry instrumentation

This example demonstrates how to monitor Valkey using [OpenTelemetry](https://opentelemetry.io/) and
[Uptrace](https://github.com/uptrace/uptrace). It requires Docker to start Valkey Server and Uptrace.

See
[Monitoring valkey-py performance with OpenTelemetry](https://valkey-py.readthedocs.io/en/latest/opentelemetry.html)
for details.

**Step 1**. Download the example using Git:

```shell
git clone https://github.com/valkey-io/valkey-py.git
cd example/opentelemetry
```

**Step 2**. Optionally, create a virtualenv:

```shell
python3 -m venv .venv
source .venv/bin/active
```

**Step 3**. Install the package:

```shell
pip install .
```

**Step 4**. Start the services using Docker and make sure Uptrace is running:

```shell
docker compose up -d
docker compose logs uptrace
```

**Step 5**. Run the Valkey client example and follow the link from the CLI to view the trace:

```shell
python3 main.py
trace: http://localhost:14318/traces/ee029d8782242c8ed38b16d961093b35
```

![Valkey trace](./image/valkey-py-trace.png)

You can also open Uptrace UI at [http://localhost:14318](http://localhost:14318) to view available
spans, logs, and metrics.
