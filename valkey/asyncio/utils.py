from typing import TYPE_CHECKING

if TYPE_CHECKING:
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
