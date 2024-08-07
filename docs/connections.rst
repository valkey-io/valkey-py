Connecting to Valkey
###################


Generic Client
**************

This is the client used to connect directly to a standard Valkey node.

.. autoclass:: valkey.Valkey
   :members:


Sentinel Client
***************

Valkey `Sentinel <https://valkey.io/topics/sentinel>`_ provides high availability for Valkey. There are commands that can only be executed against a Valkey node running in sentinel mode. Connecting to those nodes, and executing commands against them requires a Sentinel connection.

Connection example (assumes Valkey exists on the ports listed below):

   >>> from valkey import Sentinel
   >>> sentinel = Sentinel([('localhost', 26379)], socket_timeout=0.1)
   >>> sentinel.discover_master('mymaster')
   ('127.0.0.1', 6379)
   >>> sentinel.discover_slaves('mymaster')
   [('127.0.0.1', 6380)]

Sentinel
========
.. autoclass:: valkey.sentinel.Sentinel
    :members:

SentinelConnectionPool
======================
.. autoclass:: valkey.sentinel.SentinelConnectionPool
    :members:


Cluster Client
**************

This client is used for connecting to a Valkey Cluster.

ValkeyCluster
============
.. autoclass:: valkey.cluster.ValkeyCluster
    :members:

ClusterNode
===========
.. autoclass:: valkey.cluster.ClusterNode
    :members:


Async Client
************

See complete example: `here <examples/asyncio_examples.html>`__

This client is used for communicating with Valkey, asynchronously.

.. autoclass:: valkey.asyncio.client.Valkey
    :members:


Async Cluster Client
********************

ValkeyCluster (Async)
====================
.. autoclass:: valkey.asyncio.cluster.ValkeyCluster
    :members:
    :member-order: bysource

ClusterNode (Async)
===================
.. autoclass:: valkey.asyncio.cluster.ClusterNode
    :members:
    :member-order: bysource

ClusterPipeline (Async)
=======================
.. autoclass:: valkey.asyncio.cluster.ClusterPipeline
    :members: execute_command, execute
    :member-order: bysource


Connection
**********

See complete example: `here <examples/connection_examples.html>`__

Connection
==========
.. autoclass:: valkey.connection.Connection
    :members:

Connection (Async)
==================
.. autoclass:: valkey.asyncio.connection.Connection
    :members:


Connection Pools
****************

See complete example: `here <examples/connection_examples.html>`__

ConnectionPool
==============
.. autoclass:: valkey.connection.ConnectionPool
    :members:

ConnectionPool (Async)
======================
.. autoclass:: valkey.asyncio.connection.ConnectionPool
    :members:
