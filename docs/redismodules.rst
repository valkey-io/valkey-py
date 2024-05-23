Valkey Modules Commands
######################

Accessing valkey module commands requires the installation of the supported `Valkey module <https://docs.valkey.com/latest/modules/>`_. For a quick start with valkey modules, try the `Valkeymod docker <https://hub.docker.com/r/valkeylabs/valkeymod>`_.


RedisBloom Commands
*******************

These are the commands for interacting with the `RedisBloom module <https://valkeybloom.io>`_. Below is a brief example, as well as documentation on the commands themselves.

**Create and add to a bloom filter**

.. code-block:: python

    import valkey
    r = valkey.Valkey()
    r.bf().create("bloom", 0.01, 1000)
    r.bf().add("bloom", "foo")

**Create and add to a cuckoo filter**

.. code-block:: python

    import valkey
    r = valkey.Valkey()
    r.cf().create("cuckoo", 1000)
    r.cf().add("cuckoo", "filter")

**Create Count-Min Sketch and get information**

.. code-block:: python

    import valkey
    r = valkey.Valkey()
    r.cms().initbydim("dim", 1000, 5)
    r.cms().incrby("dim", ["foo"], [5])
    r.cms().info("dim")

**Create a topk list, and access the results**

.. code-block:: python

    import valkey
    r = valkey.Valkey()
    r.topk().reserve("mytopk", 3, 50, 4, 0.9)
    r.topk().info("mytopk")

.. automodule:: valkey.commands.bf.commands
    :members: BFCommands, CFCommands, CMSCommands, TOPKCommands

------

RedisGraph Commands
*******************

These are the commands for interacting with the `RedisGraph module <https://valkeygraph.io>`_. Below is a brief example, as well as documentation on the commands themselves.

**Create a graph, adding two nodes**

.. code-block:: python

    import valkey
    from valkey.graph.node import Node

    john = Node(label="person", properties={"name": "John Doe", "age": 33}
    jane = Node(label="person", properties={"name": "Jane Doe", "age": 34}

    r = valkey.Valkey()
    graph = r.graph()
    graph.add_node(john)
    graph.add_node(jane)
    graph.add_node(pat)
    graph.commit()

.. automodule:: valkey.commands.graph.node
    :members: Node

.. automodule:: valkey.commands.graph.edge
    :members: Edge

.. automodule:: valkey.commands.graph.commands
    :members: GraphCommands

------

RedisJSON Commands
******************

These are the commands for interacting with the `RedisJSON module <https://valkeyjson.io>`_. Below is a brief example, as well as documentation on the commands themselves.

**Create a json object**

.. code-block:: python

    import valkey
    r = valkey.Valkey()
    r.json().set("mykey", ".", {"hello": "world", "i am": ["a", "json", "object!"]})

Examples of how to combine search and json can be found `here <examples/search_json_examples.html>`_.

.. automodule:: valkey.commands.json.commands
    :members: JSONCommands

-----

RediSearch Commands
*******************

These are the commands for interacting with the `RediSearch module <https://valkeyearch.io>`_. Below is a brief example, as well as documentation on the commands themselves. In the example
below, an index named *my_index* is being created. When an index name is not specified, an index named *idx* is created.

**Create a search index, and display its information**

.. code-block:: python

    import valkey
    from valkey.commands.search.field import TextField

    r = valkey.Valkey()
    index_name = "my_index"
    schema = (
        TextField("play", weight=5.0),
        TextField("ball"),
    )
    r.ft(index_name).create_index(schema)
    print(r.ft(index_name).info())


.. automodule:: valkey.commands.search.commands
    :members: SearchCommands

-----

RedisTimeSeries Commands
************************

These are the commands for interacting with the `RedisTimeSeries module <https://valkeytimeseries.io>`_. Below is a brief example, as well as documentation on the commands themselves.


**Create a timeseries object with 5 second retention**

.. code-block:: python

    import valkey
    r = valkey.Valkey()
    r.ts().create(2, retention_msecs=5000)

.. automodule:: valkey.commands.timeseries.commands
    :members: TimeSeriesCommands


