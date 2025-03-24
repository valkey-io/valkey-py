from typing import TYPE_CHECKING

import anyio

if TYPE_CHECKING:
    from typing import Any, Awaitable, Callable, List

    from valkey.asyncio.client import Pipeline, Valkey


def from_url(url, **kwargs):
    """
    Returns an active Valkey client generated from the given database URL.

    Will attempt to extract the database id from the path url fragment, if
    none is provided.
    """
    from valkey.asyncio.client import Valkey

    return Valkey.from_url(url, **kwargs)


class pipeline:
    def __init__(self, valkey_obj: "Valkey"):
        self.p: "Pipeline" = valkey_obj.pipeline()

    async def __aenter__(self) -> "Pipeline":
        return self.p

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.p.execute()
        del self.p


async def anyio_gather(
    *tasks: "Awaitable[Any]", return_exceptions: bool = False
) -> "List[Any]":
    results = [None] * len(tasks)

    async def _wrapper(idx: int, task: "Awaitable[Any]") -> "Any":
        with anyio.CancelScope(shield=True):
            try:
                results[idx] = await task
            except Exception as e:
                if return_exceptions:
                    results[idx] = e
                else:
                    raise

    async with anyio.create_task_group() as tg:
        for idx, task in enumerate(tasks):
            tg.start_soon(_wrapper, idx, task)

    return results


async def anyio_condition_wait_for(
    condition: anyio.Condition, predicate: "Callable[[], bool]"
) -> bool:
    result = predicate()
    while not result:
        await condition.wait()
        result = predicate()
    return result
