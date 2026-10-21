"""Unit tests for the disjunct and optional query nodes.

These tests exercise the pure-Python query building logic and do not require a
running Valkey server.
"""

from valkey.commands.search.querystring import (
    OptionalNode,
    disjunct,
    disjunct_union,
    intersect,
    union,
)


class TestDisjunctNode:
    """``disjunct`` renders ``-(...)``, so the ``-`` applies to every child.

    RediSearch binds the ``-`` of ``(-foo bar)`` to the first child only, which
    reads as "require bar, exclude foo" -- not the "exclude all of these" the
    node documents.
    """

    def test_prefix_covers_every_child(self):
        assert disjunct("foo", "bar").to_string() == "-(foo bar)"

    def test_single_child_needs_no_parens(self):
        assert disjunct("foo").to_string() == "-foo"

    def test_nested_union_stays_grouped(self):
        assert disjunct(union("foo", "bar"), "baz").to_string() == "-((foo|bar) baz)"

    def test_disjunct_union(self):
        assert disjunct_union("foo", "bar").to_string() == "-(foo|bar)"

    def test_composition_with_intersect(self):
        assert (
            intersect(disjunct("foo", "bar"), "baz").to_string() == "(-(foo bar) baz)"
        )

    def test_explicit_paren_choice_is_honoured(self):
        assert disjunct("foo", "bar").to_string(True) == "-(foo bar)"
        assert disjunct("foo", "bar").to_string(False) == "-foo bar"


class TestOptionalNode:
    """``optional`` renders ``~(...)`` for the same reason."""

    def test_prefix_covers_every_child(self):
        assert OptionalNode("foo", "bar").to_string() == "~(foo bar)"

    def test_single_child_needs_no_parens(self):
        assert OptionalNode("foo").to_string() == "~foo"

    def test_explicit_paren_choice_is_honoured(self):
        assert OptionalNode("foo", "bar").to_string(True) == "~(foo bar)"
        assert OptionalNode("foo", "bar").to_string(False) == "~foo bar"
