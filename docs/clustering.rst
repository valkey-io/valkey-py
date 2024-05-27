Clustering
==========

valkey-py supports cluster mode and provides a client for `Valkey
Cluster <https://valkey.io/topics/cluster-tutorial>`__.

The cluster client is based on Grokzen’s
`redis-py-cluster <https://github.com/Grokzen/redis-py-cluster>`__, has
added bug fixes, and now supersedes that library. Support for these
changes is thanks to his contributions.

To learn more about Valkey Cluster, see `Valkey Cluster
specifications <https://valkey.io/topics/cluster-spec>`__.

`Creating clusters <#creating-clusters>`__ \| `Specifying Target
Nodes <#specifying-target-nodes>`__ \| `Multi-key
Commands <#multi-key-commands>`__ \| `Known PubSub
Limitations <#known-pubsub-limitations>`__

Creating clusters
-----------------

Connecting valkey-py to a Valkey Cluster instance(s) requires at a minimum
a single node for cluster discovery. There are multiple ways in which a
cluster instance can be created:

-  Using ‘host’ and ‘port’ arguments:

.. code:: python

   >>> from valkey.cluster import ValkeyCluster as Valkey
   >>> rc = Valkey(host='localhost', port=6379)
   >>> print(rc.get_nodes())
       [[host=127.0.0.1,port=6379,name=127.0.0.1:6379,server_type=primary,valkey_connection=Valkey<ConnectionPool<Connection<host=127.0.0.1,port=6379,db=0>>>], [host=127.0.0.1,port=6378,name=127.0.0.1:6378,server_type=primary,valkey_connection=Valkey<ConnectionPool<Connection<host=127.0.0.1,port=6378,db=0>>>], [host=127.0.0.1,port=6377,name=127.0.0.1:6377,server_type=replica,valkey_connection=Valkey<ConnectionPool<Connection<host=127.0.0.1,port=6377,db=0>>>]]

-  Using the Valkey URL specification:

.. code:: python

   >>> from valkey.cluster import ValkeyCluster as Valkey
   >>> rc = Valkey.from_url("valkey://localhost:6379/0")

-  Directly, via the ClusterNode class:

.. code:: python

   >>> from valkey.cluster import ValkeyCluster as Valkey
   >>> from valkey.cluster import ClusterNode
   >>> nodes = [ClusterNode('localhost', 6379), ClusterNode('localhost', 6378)]
   >>> rc = Valkey(startup_nodes=nodes)

When a ValkeyCluster instance is being created it first attempts to
establish a connection to one of the provided startup nodes. If none of
the startup nodes are reachable, a ‘ValkeyClusterException’ will be
thrown. After a connection to the one of the cluster’s nodes is
established, the ValkeyCluster instance will be initialized with 3
caches: a slots cache which maps each of the 16384 slots to the node/s
handling them, a nodes cache that contains ClusterNode objects (name,
host, port, valkey connection) for all of the cluster’s nodes, and a
commands cache contains all the server supported commands that were
retrieved using the Valkey ‘COMMAND’ output. See *ValkeyCluster specific
options* below for more.

ValkeyCluster instance can be directly used to execute Valkey commands.
When a command is being executed through the cluster instance, the
target node(s) will be internally determined. When using a key-based
command, the target node will be the node that holds the key’s slot.
Cluster management commands and other commands that are not key-based
have a parameter called ‘target_nodes’ where you can specify which nodes
to execute the command on. In the absence of target_nodes, the command
will be executed on the default cluster node. As part of cluster
instance initialization, the cluster’s default node is randomly selected
from the cluster’s primaries, and will be updated upon reinitialization.
Using r.get_default_node(), you can get the cluster’s default node, or
you can change it using the ‘set_default_node’ method.

The ‘target_nodes’ parameter is explained in the following section,
‘Specifying Target Nodes’.

.. code:: python

   >>> # target-nodes: the node that holds 'foo1's key slot
   >>> rc.set('foo1', 'bar1')
   >>> # target-nodes: the node that holds 'foo2's key slot
   >>> rc.set('foo2', 'bar2')
   >>> # target-nodes: the node that holds 'foo1's key slot
   >>> print(rc.get('foo1'))
   b'bar'
   >>> # target-node: default-node
   >>> print(rc.keys())
   [b'foo1']
   >>> # target-node: default-node
   >>> rc.ping()

Specifying Target Nodes
-----------------------

As mentioned above, all non key-based ValkeyCluster commands accept the
kwarg parameter ‘target_nodes’ that specifies the node/nodes that the
command should be executed on. The best practice is to specify target
nodes using ValkeyCluster class’s node flags: PRIMARIES, REPLICAS,
ALL_NODES, RANDOM. When a nodes flag is passed along with a command, it
will be internally resolved to the relevant node/s. If the nodes
topology of the cluster changes during the execution of a command, the
client will be able to resolve the nodes flag again with the new
topology and attempt to retry executing the command.

.. code:: python

   >>> from valkey.cluster import ValkeyCluster as Valkey
   >>> # run cluster-meet command on all of the cluster's nodes
   >>> rc.cluster_meet('127.0.0.1', 6379, target_nodes=Valkey.ALL_NODES)
   >>> # ping all replicas
   >>> rc.ping(target_nodes=Valkey.REPLICAS)
   >>> # ping a random node
   >>> rc.ping(target_nodes=Valkey.RANDOM)
   >>> # get the keys from all cluster nodes
   >>> rc.keys(target_nodes=Valkey.ALL_NODES)
   [b'foo1', b'foo2']
   >>> # execute bgsave in all primaries
   >>> rc.bgsave(Valkey.PRIMARIES)

You could also pass ClusterNodes directly if you want to execute a
command on a specific node / node group that isn’t addressed by the
nodes flag. However, if the command execution fails due to cluster
topology changes, a retry attempt will not be made, since the passed
target node/s may no longer be valid, and the relevant cluster or
connection error will be returned.

.. code:: python

   >>> node = rc.get_node('localhost', 6379)
   >>> # Get the keys only for that specific node
   >>> rc.keys(target_nodes=node)
   >>> # get Valkey info from a subset of primaries
   >>> subset_primaries = [node for node in rc.get_primaries() if node.port > 6378]
   >>> rc.info(target_nodes=subset_primaries)

In addition, the ValkeyCluster instance can query the Valkey instance of a
specific node and execute commands on that node directly. The Valkey
client, however, does not handle cluster failures and retries.

.. code:: python

   >>> cluster_node = rc.get_node(host='localhost', port=6379)
   >>> print(cluster_node)
   [host=127.0.0.1,port=6379,name=127.0.0.1:6379,server_type=primary,valkey_connection=Valkey<ConnectionPool<Connection<host=127.0.0.1,port=6379,db=0>>>]
   >>> r = cluster_node.valkey_connection
   >>> r.client_list()
   [{'id': '276', 'addr': '127.0.0.1:64108', 'fd': '16', 'name': '', 'age': '0', 'idle': '0', 'flags': 'N', 'db': '0', 'sub': '0', 'psub': '0', 'multi': '-1', 'qbuf': '26', 'qbuf-free': '32742', 'argv-mem': '10', 'obl': '0', 'oll': '0', 'omem': '0', 'tot-mem': '54298', 'events': 'r', 'cmd': 'client', 'user': 'default'}]
   >>> # Get the keys only for that specific node
   >>> r.keys()
   [b'foo1']

Multi-key Commands
------------------

Valkey supports multi-key commands in Cluster Mode, such as Set type
unions or intersections, mset and mget, as long as the keys all hash to
the same slot. By using ValkeyCluster client, you can use the known
functions (e.g. mget, mset) to perform an atomic multi-key operation.
However, you must ensure all keys are mapped to the same slot, otherwise
a ValkeyClusterException will be thrown. Valkey Cluster implements a
concept called hash tags that can be used in order to force certain keys
to be stored in the same hash slot, see `Keys hash
tag <https://valkey.io/topics/cluster-spec#keys-hash-tags>`__. You can
also use nonatomic for some of the multikey operations, and pass keys
that aren’t mapped to the same slot. The client will then map the keys
to the relevant slots, sending the commands to the slots’ node owners.
Non-atomic operations batch the keys according to their hash value, and
then each batch is sent separately to the slot’s owner.

.. code:: python

   # Atomic operations can be used when all keys are mapped to the same slot
   >>> rc.mset({'{foo}1': 'bar1', '{foo}2': 'bar2'})
   >>> rc.mget('{foo}1', '{foo}2')
   [b'bar1', b'bar2']
   # Non-atomic multi-key operations splits the keys into different slots
   >>> rc.mset_nonatomic({'foo': 'value1', 'bar': 'value2', 'zzz': 'value3')
   >>> rc.mget_nonatomic('foo', 'bar', 'zzz')
   [b'value1', b'value2', b'value3']

**Cluster PubSub:**

When a ClusterPubSub instance is created without specifying a node, a
single node will be transparently chosen for the pubsub connection on
the first command execution. The node will be determined by: 1. Hashing
the channel name in the request to find its keyslot 2. Selecting a node
that handles the keyslot: If read_from_replicas is set to true, a
replica can be selected.

Known PubSub Limitations
------------------------

Pattern subscribe and publish do not currently work properly due to key
slots. If we hash a pattern like fo\* we will receive a keyslot for that
string but there are endless possibilities for channel names based on
this pattern - unknowable in advance. This feature is not disabled but
the commands are not currently recommended for use. See
`valkey-py-cluster
documentation <https://valkey-py-cluster.readthedocs.io/en/stable/pubsub.html>`__
for more.

.. code:: python

   >>> p1 = rc.pubsub()
   # p1 connection will be set to the node that holds 'foo' keyslot
   >>> p1.subscribe('foo')
   # p2 connection will be set to node 'localhost:6379'
   >>> p2 = rc.pubsub(rc.get_node('localhost', 6379))

**Read Only Mode**

By default, Valkey Cluster always returns MOVE redirection response on
accessing a replica node. You can overcome this limitation and scale
read commands by triggering READONLY mode.

To enable READONLY mode pass read_from_replicas=True to ValkeyCluster
constructor. When set to true, read commands will be assigned between
the primary and its replications in a Round-Robin manner.

READONLY mode can be set at runtime by calling the readonly() method
with target_nodes=‘replicas’, and read-write access can be restored by
calling the readwrite() method.

.. code:: python

   >>> from cluster import ValkeyCluster as Valkey
   # Use 'debug' log level to print the node that the command is executed on
   >>> rc_readonly = Valkey(startup_nodes=startup_nodes,
   ...                     read_from_replicas=True)
   >>> rc_readonly.set('{foo}1', 'bar1')
   >>> for i in range(0, 4):
   ...     # Assigns read command to the slot's hosts in a Round-Robin manner
   ...     rc_readonly.get('{foo}1')
   # set command would be directed only to the slot's primary node
   >>> rc_readonly.set('{foo}2', 'bar2')
   # reset READONLY flag
   >>> rc_readonly.readwrite(target_nodes='replicas')
   # now the get command would be directed only to the slot's primary node
   >>> rc_readonly.get('{foo}1')
