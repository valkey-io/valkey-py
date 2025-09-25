.. valkey-py documentation master file, created by
   sphinx-quickstart on Thu Jul 28 13:55:57 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

valkey-py - Python Client for Valkey
====================================

Getting Started
****************

`valkey-py <https://pypi.org/project/valkey>`_ requires a running Valkey server, and Python 3.10+. See the `Valkey
quickstart <https://valkey.io/topics/quickstart>`_ for Valkey installation instructions.

valkey-py can be installed using pip via ``pip install valkey``.


Quickly connecting to valkey
***************************

There are two quick ways to connect to Valkey.

**Assuming you run Valkey on localhost:6379 (the default)**

.. code-block:: python

   import valkey
   r = valkey.Valkey()
   r.ping()

**Running valkey on foo.bar.com, port 12345**

.. code-block:: python

   import valkey
   r = valkey.Valkey(host='foo.bar.com', port=12345)
   r.ping()

**Another example with foo.bar.com, port 12345**

.. code-block:: python

   import valkey
   r = valkey.from_url('valkey://foo.bar.com:12345')
   r.ping()

After that, you probably want to `run valkey commands <commands.html>`_.

.. toctree::
   :hidden:

   genindex

Valkey Command Functions
***********************
.. toctree::
   :maxdepth: 2

   commands
   valkeymodules

Module Documentation
********************
.. toctree::
   :maxdepth: 1

   connections
   clustering
   exceptions
   backoff
   lock
   retry
   lua_scripting
   opentelemetry
   resp3_features
   advanced_features
   examples

Contributing
*************

- `How to contribute <https://github.com/valkey-io/valkey-py/blob/master/CONTRIBUTING.md>`_
- `Issue Tracker <https://github.com/valkey-io/valkey-py/issues>`_
- `Source Code <https://github.com/valkey-io/valkey-py/>`_
- `Release History <https://github.com/valkey-io/valkey-py/releases/>`_
- `Valkey Slack <https://valkey.io/slack/>`_

License
*******

This project is licensed under the `MIT license <https://github.com/valkey-io/valkey-py/blob/master/LICENSE>`_.
