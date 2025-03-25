import contextlib

import anyio
import pytest

from valkey.asyncio import Valkey
from valkey.asyncio.cluster import ValkeyCluster
from valkey.asyncio.utils import anyio_condition_wait_for

pytestmark = pytest.mark.anyio


class DelayProxy:
    def __init__(self, addr, valkey_addr, delay: float = 0.0):
        self.addr = addr
        self.valkey_addr = valkey_addr

        self.delay = delay

        self.task_group = None
        self.exit_stack = None

        self.listener = None
        self.send_event = anyio.Event()
        self.cond = anyio.Condition()
        self.running = 0

    async def __aenter__(self):
        async with contextlib.AsyncExitStack() as stack:
            self.task_group = await stack.enter_async_context(
                anyio.create_task_group(),
            )

            await self.start()

            self.exit_stack = stack.pop_all()

        return self

    async def __aexit__(self, *args):
        try:
            await self.stop()
        finally:
            return await self.exit_stack.__aexit__(*args)

    async def start(self):
        # test that we can connect to valkey
        with anyio.fail_after(2):
            stream = await anyio.connect_tcp(*self.valkey_addr)
            await stream.aclose()

        self.listener = await anyio.create_tcp_listener(
            local_host=self.addr[0], local_port=self.addr[1]
        )

        async def _serve(task_status: anyio.TASK_STATUS_IGNORED):
            async with self.listener:
                task_status.started()
                await self.listener.serve(self.handle, task_group=self.task_group)

        await self.task_group.start(_serve)

    @contextlib.contextmanager
    def set_delay(self, delay: float = 0.0):
        """
        Allow to override the delay for parts of tests which aren't time dependent,
        to speed up execution.
        """
        old_delay = self.delay
        self.delay = delay
        try:
            yield
        finally:
            self.delay = old_delay

    async def handle(self, client):
        # establish connection to valkey
        async with await anyio.connect_tcp(*self.valkey_addr) as stream:
            async with anyio.create_task_group() as tg:
                tg.start_soon(self.pipe, client, stream, "to valkey:", True)
                tg.start_soon(self.pipe, stream, client, "from valkey:")

    async def stop(self):
        self.task_group.cancel_scope.cancel()

        # Server does not wait for all spawned tasks.  We must do that also to ensure
        # that all sockets are closed.
        async with self.cond:
            await anyio_condition_wait_for(self.cond, lambda: self.running == 0)

    async def pipe(
        self,
        proxy,
        upstream,
        name="",
        set_event: bool = False,
    ):
        self.running += 1
        try:
            while True:
                try:
                    data = await proxy.receive(1000)
                except (anyio.EndOfStream, anyio.ClosedResourceError):
                    break
                # print(f"{name} read {len(data)} delay {self.delay}")
                if set_event:
                    self.send_event.set()
                await anyio.sleep(self.delay)
                await upstream.send(data)
        finally:
            try:
                await upstream.aclose()
            except RuntimeError:
                # ignore errors on close pertaining to no event loop. Don't want
                # to clutter the test output with errors if being garbage collected
                pass
            async with self.cond:
                self.running -= 1
                if self.running == 0:
                    self.cond.notify_all()


@pytest.mark.onlynoncluster
@pytest.mark.parametrize("delay", argvalues=[0.05, 0.5, 1, 2])
async def test_standalone(delay, master_host):
    # create a tcp socket proxy that relays data to Valkey and back,
    # inserting 0.1 seconds of delay
    async with DelayProxy(addr=("127.0.0.1", 5380), valkey_addr=master_host) as dp:
        for b in [True, False]:
            # note that we connect to proxy, rather than to Valkey directly
            async with Valkey(
                host="127.0.0.1", port=5380, single_connection_client=b
            ) as r:
                await r.set("foo", "foo")
                await r.set("bar", "bar")

                async def op(r):
                    with dp.set_delay(delay * 2):
                        return await r.get(
                            "foo"
                        )  # <-- this is the operation we want to cancel

                dp.send_event = anyio.Event()

                async with anyio.create_task_group() as tg:
                    tg.start_soon(op, r)
                    # Wait until the task has sent, and then some, to make sure it has
                    # settled on the read.
                    await dp.send_event.wait()
                    await anyio.sleep(0.01)  # a little extra time for prudence
                    tg.cancel_scope.cancel()

                # make sure that our previous request, cancelled while waiting for
                # a response, didn't leave the connection open and in a bad state
                assert await r.get("bar") == b"bar"
                assert await r.ping()
                assert await r.get("foo") == b"foo"


@pytest.mark.onlynoncluster
@pytest.mark.parametrize("delay", argvalues=[0.05, 0.5, 1, 2])
async def test_standalone_pipeline(delay, master_host):
    async with DelayProxy(addr=("127.0.0.1", 5380), valkey_addr=master_host) as dp:
        for b in [True, False]:
            async with Valkey(
                host="127.0.0.1", port=5380, single_connection_client=b
            ) as r:
                await r.set("foo", "foo")
                await r.set("bar", "bar")

                pipe = r.pipeline()

                pipe2 = r.pipeline()
                pipe2.get("bar")
                pipe2.ping()
                pipe2.get("foo")

                async def op(pipe):
                    with dp.set_delay(delay * 2):
                        return await pipe.get(
                            "foo"
                        ).execute()  # <-- this is the operation we want to cancel

                dp.send_event = anyio.Event()
                async with anyio.create_task_group() as tg:
                    tg.start_soon(op, pipe)
                    # wait until task has settled on the read
                    await dp.send_event.wait()
                    await anyio.sleep(0.01)
                    tg.cancel_scope.cancel()

                # we have now cancelled the pieline in the middle of a request,
                # make sure that the connection is still usable
                pipe.get("bar")
                pipe.ping()
                pipe.get("foo")
                await pipe.reset()

                # check that the pipeline is empty after reset
                assert await pipe.execute() == []

                # validating that the pipeline can be used as it could previously
                pipe.get("bar")
                pipe.ping()
                pipe.get("foo")
                assert await pipe.execute() == [b"bar", True, b"foo"]
                assert await pipe2.execute() == [b"bar", True, b"foo"]


@pytest.mark.onlycluster
async def test_cluster(master_host):
    delay = 0.1
    cluster_port = 16379
    remap_base = 7372
    n_nodes = 6
    hostname, _ = master_host

    def remap(address):
        host, port = address
        return host, remap_base + port - cluster_port

    proxies = []
    for i in range(n_nodes):
        port = cluster_port + i
        remapped = remap_base + i
        forward_addr = hostname, port
        proxy = DelayProxy(addr=("127.0.0.1", remapped), valkey_addr=forward_addr)
        proxies.append(proxy)

    def all_reset():
        for p in proxies:
            p.send_event = anyio.Event()

    async def wait_for_send():
        first_done = anyio.Event()

        async def _waiter(event):
            await event.wait()
            first_done.set()
            await anyio.lowlevel.checkpoint()

        async with anyio.create_task_group() as tg:
            for p in proxies:
                tg.start_soon(_waiter, p.send_event)
            await first_done.wait()
            tg.cancel_scope.cancel()

    @contextlib.contextmanager
    def set_delay(delay: float):
        with contextlib.ExitStack() as stack:
            for p in proxies:
                stack.enter_context(p.set_delay(delay))
            yield

    async with contextlib.AsyncExitStack() as stack:
        for p in proxies:
            await stack.enter_async_context(p)

        r = ValkeyCluster.from_url(
            f"valkey://127.0.0.1:{remap_base}", address_remap=remap
        )
        try:
            await r.initialize()
            await r.set("foo", "foo")
            await r.set("bar", "bar")

            async def op(r):
                with set_delay(delay):
                    return await r.get("foo")

            all_reset()

            async with anyio.create_task_group() as tg:
                tg.start_soon(op, r)
                # Wait for whichever DelayProxy gets the request first
                await wait_for_send()
                await anyio.sleep(0.01)
                tg.cancel_scope.cancel()

            # try a number of requests to exercise all the connections
            async def doit():
                assert await r.get("bar") == b"bar"
                assert await r.ping()
                assert await r.get("foo") == b"foo"

            async with anyio.create_task_group() as tg:
                for _ in range(10):
                    tg.start_soon(doit)
        finally:
            await r.aclose()
