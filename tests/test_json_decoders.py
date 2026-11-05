"""Unit tests for the JSON response decoders, without a running server."""

import pytest

from valkey.commands.json.decoders import decode_list, unstring


class TestUnstring:
    """``unstring`` converts a numeric string to int or float, and nothing else.

    The pattern used to be ``"^\\d+.\\d+$"`` -- the dot unescaped, so it matched
    any character, and the integer pattern was not anchored at the end, so a
    prefix was enough.
    """

    def test_integer_stays_an_integer(self):
        result = unstring("100")
        assert result == 100
        assert isinstance(result, int)

    def test_float(self):
        result = unstring("100.5")
        assert result == 100.5
        assert isinstance(result, float)

    @pytest.mark.parametrize(
        "value",
        ["10x20", "100abc", "a1.2b", "1.2.3", "1,000"],
    )
    def test_a_non_number_is_returned_unchanged(self, value):
        assert unstring(value) == value

    def test_a_dot_that_is_not_a_decimal_point_does_not_raise(self):
        """``"10x20"`` used to match the float pattern and raise ValueError."""
        assert unstring("10x20") == "10x20"


class TestDecodeList:
    def test_decodes_scalars(self):
        assert decode_list(b"45.55") == 45.55
        assert decode_list("45.55") == 45.55

    def test_decodes_each_element(self):
        assert decode_list(["hello", b"world"]) == ["hello", "world"]
