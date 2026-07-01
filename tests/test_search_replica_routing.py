"""
Unit tests for FT.SEARCH replica routing fix.

These tests verify that search read commands (FT.SEARCH, FT.AGGREGATE, etc.)
are correctly routed to replica nodes when read_from_replicas=True, while
search write commands (FT.CREATE, FT.DROPINDEX, etc.) always go to primaries.
"""

import sys
import unittest
from unittest.mock import MagicMock, patch, PropertyMock

sys.path.insert(0, ".")

from valkey.cluster import ValkeyCluster, AbstractValkeyCluster, ClusterNode
from valkey.commands import READ_COMMANDS


class TestSearchCommandClassification(unittest.TestCase):
    """Test that search commands are correctly classified."""

    def test_ft_search_in_read_commands(self):
        """FT.SEARCH must be in READ_COMMANDS for replica routing."""
        self.assertIn("FT.SEARCH", READ_COMMANDS)

    def test_ft_aggregate_in_read_commands(self):
        """FT.AGGREGATE must be in READ_COMMANDS for replica routing."""
        self.assertIn("FT.AGGREGATE", READ_COMMANDS)

    def test_ft_info_in_read_commands(self):
        """FT.INFO must be in READ_COMMANDS for replica routing."""
        self.assertIn("FT.INFO", READ_COMMANDS)

    def test_ft_list_in_read_commands(self):
        """FT._LIST must be in READ_COMMANDS for replica routing."""
        self.assertIn("FT._LIST", READ_COMMANDS)

    def test_ft_create_not_in_read_commands(self):
        """FT.CREATE must NOT be in READ_COMMANDS (it's a write)."""
        self.assertNotIn("FT.CREATE", READ_COMMANDS)

    def test_ft_dropindex_not_in_read_commands(self):
        """FT.DROPINDEX must NOT be in READ_COMMANDS (it's a write)."""
        self.assertNotIn("FT.DROPINDEX", READ_COMMANDS)

    def test_ft_alter_not_in_read_commands(self):
        """FT.ALTER must NOT be in READ_COMMANDS (it's a write)."""
        self.assertNotIn("FT.ALTER", READ_COMMANDS)

    def test_search_write_commands_defined(self):
        """SEARCH_WRITE_COMMANDS must contain all write-only search commands."""
        write_cmds = AbstractValkeyCluster.SEARCH_WRITE_COMMANDS[0]
        self.assertIn("FT.CREATE", write_cmds)
        self.assertIn("FT.ALTER", write_cmds)
        self.assertIn("FT.DROPINDEX", write_cmds)
        self.assertIn("FT.DROP", write_cmds)
        self.assertNotIn("FT.SEARCH", write_cmds)
        self.assertNotIn("FT.AGGREGATE", write_cmds)

    def test_search_read_commands_defined(self):
        """SEARCH_READ_COMMANDS must contain all read-only search commands."""
        read_cmds = AbstractValkeyCluster.SEARCH_READ_COMMANDS[0]
        self.assertIn("FT.SEARCH", read_cmds)
        self.assertIn("FT.AGGREGATE", read_cmds)
        self.assertIn("FT.INFO", read_cmds)
        self.assertIn("FT._LIST", read_cmds)
        self.assertNotIn("FT.CREATE", read_cmds)
        self.assertNotIn("FT.DROPINDEX", read_cmds)

    def test_search_commands_backward_compat(self):
        """SEARCH_COMMANDS should contain all commands (union of read + write)."""
        all_cmds = AbstractValkeyCluster.SEARCH_COMMANDS[0]
        write_cmds = AbstractValkeyCluster.SEARCH_WRITE_COMMANDS[0]
        read_cmds = AbstractValkeyCluster.SEARCH_READ_COMMANDS[0]
        # All write commands should be in SEARCH_COMMANDS
        for cmd in write_cmds:
            self.assertIn(cmd, all_cmds)
        # All read commands should be in SEARCH_COMMANDS
        for cmd in read_cmds:
            self.assertIn(cmd, all_cmds)

    def test_no_overlap_between_write_and_read(self):
        """Write and read command lists must not overlap."""
        write_set = set(AbstractValkeyCluster.SEARCH_WRITE_COMMANDS[0])
        read_set = set(AbstractValkeyCluster.SEARCH_READ_COMMANDS[0])
        overlap = write_set & read_set
        self.assertEqual(overlap, set(), f"Overlapping commands: {overlap}")


class TestDetermineNodesRouting(unittest.TestCase):
    """Test _determine_nodes routing behavior for search commands."""

    def _create_mock_cluster(self, read_from_replicas=False):
        """Create a mock ValkeyCluster with controllable nodes."""
        with patch.object(ValkeyCluster, "__init__", lambda self, **kwargs: None):
            cluster = ValkeyCluster()

        # Set up mock nodes
        primary1 = MagicMock(spec=ClusterNode)
        primary1.name = "primary1"
        primary1.server_type = "primary"

        primary2 = MagicMock(spec=ClusterNode)
        primary2.name = "primary2"
        primary2.server_type = "primary"

        replica1 = MagicMock(spec=ClusterNode)
        replica1.name = "replica1"
        replica1.server_type = "replica"

        replica2 = MagicMock(spec=ClusterNode)
        replica2.name = "replica2"
        replica2.server_type = "replica"

        all_nodes = [primary1, primary2, replica1, replica2]
        primaries = [primary1, primary2]
        replicas = [replica1, replica2]

        # Configure the cluster mock
        cluster.read_from_replicas = read_from_replicas
        cluster.command_flags = {}
        cluster.nodes_manager = MagicMock()
        cluster.nodes_manager.default_node = primary1

        cluster.get_nodes = MagicMock(return_value=all_nodes)
        cluster.get_primaries = MagicMock(return_value=primaries)
        cluster.get_replicas = MagicMock(return_value=replicas)
        cluster.get_random_node = MagicMock(return_value=replica1)

        return cluster, primary1, primary2, replica1, replica2, all_nodes

    def test_ft_search_routes_to_primary_without_read_from_replicas(self):
        """FT.SEARCH should route to default_node (primary) when read_from_replicas=False."""
        cluster, primary1, _, _, _, _ = self._create_mock_cluster(
            read_from_replicas=False
        )
        nodes = cluster._determine_nodes("FT.SEARCH", "my_index", "@field:{value}")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0], primary1)  # default_node is primary1

    def test_ft_search_routes_to_any_node_with_read_from_replicas(self):
        """FT.SEARCH should route to any node (including replicas) when read_from_replicas=True."""
        cluster, primary1, primary2, replica1, replica2, all_nodes = (
            self._create_mock_cluster(read_from_replicas=True)
        )

        # Run multiple times to verify randomization includes replicas
        nodes_seen = set()
        for _ in range(100):
            nodes = cluster._determine_nodes("FT.SEARCH", "my_index", "@field:{value}")
            self.assertEqual(len(nodes), 1)
            nodes_seen.add(nodes[0].name)

        # With 100 iterations and 4 nodes, we should see more than just primaries
        self.assertGreater(
            len(nodes_seen), 1, "Expected distribution across multiple nodes"
        )

    def test_ft_aggregate_routes_to_any_node_with_read_from_replicas(self):
        """FT.AGGREGATE should route to any node when read_from_replicas=True."""
        cluster, _, _, _, _, all_nodes = self._create_mock_cluster(
            read_from_replicas=True
        )
        nodes = cluster._determine_nodes(
            "FT.AGGREGATE", "my_index", "@field:{value}"
        )
        self.assertEqual(len(nodes), 1)
        self.assertIn(nodes[0], all_nodes)

    def test_ft_create_always_routes_to_primary(self):
        """FT.CREATE must always route to primary regardless of read_from_replicas."""
        cluster, primary1, _, _, _, _ = self._create_mock_cluster(
            read_from_replicas=True
        )
        nodes = cluster._determine_nodes(
            "FT.CREATE", "my_index", "ON", "HASH", "SCHEMA", "field", "TEXT"
        )
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0], primary1)  # Must be default_node (primary)

    def test_ft_dropindex_always_routes_to_primary(self):
        """FT.DROPINDEX must always route to primary regardless of read_from_replicas."""
        cluster, primary1, _, _, _, _ = self._create_mock_cluster(
            read_from_replicas=True
        )
        nodes = cluster._determine_nodes("FT.DROPINDEX", "my_index")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0], primary1)

    def test_ft_info_routes_to_replica_with_read_from_replicas(self):
        """FT.INFO should route to any node when read_from_replicas=True."""
        cluster, _, _, _, _, all_nodes = self._create_mock_cluster(
            read_from_replicas=True
        )
        nodes = cluster._determine_nodes("FT.INFO", "my_index")
        self.assertEqual(len(nodes), 1)
        self.assertIn(nodes[0], all_nodes)


if __name__ == "__main__":
    unittest.main(verbosity=2)
