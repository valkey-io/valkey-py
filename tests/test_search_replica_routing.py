"""
Unit tests for FT.SEARCH replica routing fix.

Verifies that search read commands are routed to replicas when
read_from_replicas=True, while write commands always go to primaries.
"""

import unittest
from unittest.mock import MagicMock, patch

from valkey.cluster import AbstractValkeyCluster, ClusterNode, ValkeyCluster


class TestSearchCommandClassification(unittest.TestCase):
    """Test that search commands are correctly classified."""

    def test_no_overlap_between_write_and_read(self):
        """Write and read command lists must not overlap."""
        write_set = set(AbstractValkeyCluster.SEARCH_WRITE_COMMANDS[0])
        read_set = set(AbstractValkeyCluster.SEARCH_READ_COMMANDS[0])
        self.assertFalse(write_set & read_set)

    def test_search_commands_is_union(self):
        """SEARCH_COMMANDS must be the union of read + write."""
        all_cmds = AbstractValkeyCluster.SEARCH_COMMANDS[0]
        for cmd in AbstractValkeyCluster.SEARCH_WRITE_COMMANDS[0]:
            self.assertIn(cmd, all_cmds)
        for cmd in AbstractValkeyCluster.SEARCH_READ_COMMANDS[0]:
            self.assertIn(cmd, all_cmds)


class TestDetermineNodesRouting(unittest.TestCase):
    """Test _determine_nodes routing behavior for search commands."""

    def _make_cluster(self, read_from_replicas=False):
        """Create a mock ValkeyCluster."""
        with patch.object(ValkeyCluster, "__init__", lambda self, **kwargs: None):
            cluster = ValkeyCluster()

        primary = MagicMock(spec=ClusterNode)
        primary.name = "primary1"
        replica = MagicMock(spec=ClusterNode)
        replica.name = "replica1"
        all_nodes = [primary, replica]

        cluster.read_from_replicas = read_from_replicas
        cluster.command_flags = {}
        cluster.nodes_manager = MagicMock()
        cluster.nodes_manager.default_node = primary
        cluster.get_nodes = MagicMock(return_value=all_nodes)

        return cluster, primary, all_nodes

    def test_ft_search_to_primary_without_replicas(self):
        """FT.SEARCH routes to primary when read_from_replicas=False."""
        cluster, primary, _ = self._make_cluster(read_from_replicas=False)
        nodes = cluster._determine_nodes("FT.SEARCH", "idx", "*")
        self.assertEqual(nodes, [primary])

    def test_ft_search_to_any_node_with_replicas(self):
        """FT.SEARCH routes to any node when read_from_replicas=True."""
        cluster, _, all_nodes = self._make_cluster(read_from_replicas=True)
        nodes = cluster._determine_nodes("FT.SEARCH", "idx", "*")
        self.assertEqual(len(nodes), 1)
        self.assertIn(nodes[0], all_nodes)

    def test_ft_create_always_to_primary(self):
        """FT.CREATE always routes to primary."""
        cluster, primary, _ = self._make_cluster(read_from_replicas=True)
        nodes = cluster._determine_nodes("FT.CREATE", "idx", "ON", "HASH")
        self.assertEqual(nodes, [primary])

    def test_ft_dropindex_always_to_primary(self):
        """FT.DROPINDEX always routes to primary."""
        cluster, primary, _ = self._make_cluster(read_from_replicas=True)
        nodes = cluster._determine_nodes("FT.DROPINDEX", "idx")
        self.assertEqual(nodes, [primary])


if __name__ == "__main__":
    unittest.main(verbosity=2)
