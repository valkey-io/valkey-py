Connecting to Valkey
####################


Generic Client
**************

This is the client used to connect directly to a standard Valkey node.

Standalone replica redirect capability
=====================================

Valkey 8.0 adds ``CLIENT CAPA redirect`` for standalone primary/replica
deployments. In valkey-py, this is exposed as the opt-in
``client_capa_redirect`` connection argument.

.. code-block:: python

   >>> import valkey
   >>> replica = valkey.Valkey(host="localhost", port=6380,
   ...                         client_capa_redirect=True)
   >>> replica = valkey.from_url(
   ...     "valkey://localhost:6380?client_capa_redirect=true"
   ... )

When enabled, commands sent to a standalone replica raise
``valkey.exceptions.RedirectError`` until ``READONLY`` is enabled for that
connection. For more details, see :doc:`advanced_features`.

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
=============
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
=====================
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
