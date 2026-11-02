from unittest.mock import AsyncMock

import pytest

from valkey.asyncio import Valkey
from valkey.commands.search.aggregation import AggregateRequest


@pytest.mark.parametrize("protocol", [2, 3])
@pytest.mark.parametrize("count", [0, 2])
async def test_aggregate_forwards_limit(protocol, count):
    client = Valkey(protocol=protocol)
    reply = [0] if protocol == 2 else {"results": []}
    client.execute_command = AsyncMock(return_value=reply)
    result = await client.ft("idx").aggregate(AggregateRequest().limit(0, count))
    client.execute_command.assert_awaited_once_with(
        "FT.AGGREGATE", "idx", "*", "LIMIT", "0", str(count)
    )
    assert (result.rows if protocol == 2 else result["results"]) == []
    await client.aclose()
