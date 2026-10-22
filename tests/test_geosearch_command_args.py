"""Zero-valued GEOSEARCH arguments must reach the server.

``GeoCommands._geosearchgeneric`` (shared by GEOSEARCH and GEOSEARCHSTORE for
both the sync and the async client) decides whether an option was supplied by
truthiness.  Values that are valid but falsy -- ``radius=0``, ``width=0``,
``height=0``, ``count=0`` and ``member=""`` -- were therefore dropped, so
``GEOSEARCH key FROMLONLAT 0 0`` went out with no BYRADIUS/BYBOX clause at all
and ``FROMMEMBER`` and ``FROMLONLAT`` could be sent together.

These tests need no server: they inspect the arguments handed to
``execute_command``.
"""

from unittest import mock

import pytest

import valkey
import valkey.exceptions as exceptions


def geosearch_args(*args, **kwargs):
    """Return the GEOSEARCH arguments as they would be sent to the server."""
    client = valkey.Valkey()
    with mock.patch.object(client, "execute_command", return_value=[]) as m:
        client.geosearch("places", *args, **kwargs)
        return list(m.call_args[0])


def test_geosearch_forwards_zero_origin_and_zero_radius():
    # (0, 0) is the equator/prime meridian intersection, a real origin.
    args = geosearch_args(longitude=0, latitude=0, radius=0, unit="m")
    assert args == ["GEOSEARCH", "places", b"FROMLONLAT", 0, 0, b"BYRADIUS", 0, "m"]


def test_geosearch_forwards_zero_box_dimension():
    args = geosearch_args(longitude=1, latitude=2, width=0, height=1, unit="m")
    assert args[-4:] == [b"BYBOX", 0, 1, "m"]


def test_geosearch_forwards_zero_count():
    args = geosearch_args(longitude=1, latitude=2, radius=10, count=0, unit="m")
    assert args[-2:] == [b"COUNT", 0]

    # An omitted count still omits the clause.
    args = geosearch_args(longitude=1, latitude=2, radius=10, unit="m")
    assert b"COUNT" not in args


def test_geosearch_forwards_empty_member():
    # An empty member name is a member name, just like an empty ZADD member.
    args = geosearch_args(member="", radius=100, unit="m")
    assert args == ["GEOSEARCH", "places", b"FROMMEMBER", "", b"BYRADIUS", 100, "m"]


def test_geosearch_rejects_zero_origin_next_to_member():
    # The mutual exclusion must not depend on the coordinate being non-zero.
    with pytest.raises(exceptions.DataError):
        geosearch_args(member="Palermo", longitude=0, latitude=0, radius=100)


def test_geosearch_rejects_zero_radius_next_to_box():
    with pytest.raises(exceptions.DataError):
        geosearch_args(longitude=1, latitude=2, radius=0, width=100, height=100)


def test_geosearchstore_forwards_zero_radius():
    client = valkey.Valkey()
    with mock.patch.object(client, "execute_command", return_value=0) as m:
        client.geosearchstore("dest", "places", longitude=0, latitude=0, radius=0)
        args = list(m.call_args[0])
    assert args == [
        "GEOSEARCHSTORE",
        "dest",
        "places",
        b"FROMLONLAT",
        0,
        0,
        b"BYRADIUS",
        0,
        "m",
    ]


async def test_async_geosearch_forwards_zero_arguments():
    client = valkey.asyncio.Valkey()
    mock_execute = mock.AsyncMock(return_value=[])
    with mock.patch.object(client, "execute_command", new=mock_execute):
        await client.geosearch("places", longitude=0, latitude=0, radius=0, unit="m")
    args = list(mock_execute.call_args[0])
    assert args[2:5] == [b"FROMLONLAT", 0, 0]
    assert args[-3:] == [b"BYRADIUS", 0, "m"]

    mock_execute.reset_mock()
    with mock.patch.object(client, "execute_command", new=mock_execute):
        with pytest.raises(exceptions.DataError):
            await client.geosearch(
                "places", member="Palermo", longitude=0, latitude=0, radius=100
            )
