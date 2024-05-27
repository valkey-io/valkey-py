Valkey Commands
##############

Core Commands
*************

The following functions can be used to replicate their equivalent `Valkey command <https://valkey.io/commands>`_.  Generally they can be used as functions on your valkey connection.  For the simplest example, see below:

Getting and settings data in valkey::

   import valkey
   r = valkey.Valkey(decode_responses=True)
   r.set('mykey', 'thevalueofmykey')
   r.get('mykey')

.. autoclass:: valkey.commands.core.CoreCommands
   :inherited-members:

Sentinel Commands
*****************
.. autoclass:: valkey.commands.sentinel.SentinelCommands
   :inherited-members:

Valkey Cluster Commands
**********************

The following `Valkey commands <https://valkey.io/commands>`_ are available within a `Valkey Cluster <https://valkey.io/topics/cluster-tutorial>`_.  Generally they can be used as functions on your valkey connection.

.. autoclass:: valkey.commands.cluster.ValkeyClusterCommands
   :inherited-members:
