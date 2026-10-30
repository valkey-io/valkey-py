from unittest.mock import Mock

import pytest

from valkey import Valkey
from valkey.commands.search.aggregation import AggregateRequest, Limit


@pytest.mark.parametrize("offset", [0, 3])
@pytest.mark.parametrize("count", [0, 1, 10])
def test_explicit_limit(offset, count):
    assert Limit(offset, count).build_args() == ["LIMIT", str(offset), str(count)]


def test_unspecified_limit():
    assert Limit().build_args() == []
    assert AggregateRequest().build_args() == ["*"]


def test_zero_limit_keeps_aggregation_stage_order():
    request = AggregateRequest().limit(0, 0).group_by("@category").limit(2, 0)
    assert request.build_args() == [
        "*",
        "LIMIT",
        "0",
        "0",
        "GROUPBY",
        "1",
        "@category",
        "LIMIT",
        "2",
        "0",
    ]


@pytest.mark.parametrize("protocol", [2, 3])
@pytest.mark.parametrize("count", [0, 2])
def test_aggregate_forwards_limit(protocol, count):
    client = Valkey(protocol=protocol)
    reply = [0] if protocol == 2 else {"results": []}
    client.execute_command = Mock(return_value=reply)
    result = client.ft("idx").aggregate(AggregateRequest().limit(0, count))
    client.execute_command.assert_called_once_with(
        "FT.AGGREGATE", "idx", "*", "LIMIT", "0", str(count)
    )
    assert (result.rows if protocol == 2 else result["results"]) == []
