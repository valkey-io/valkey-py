# valkey-py

The Python interface to the Valkey key-value store.

[![CI](https://github.com/valkey-io/valkey-py/workflows/CI/badge.svg)](https://github.com/valkey-io/valkey-py/actions?query=workflow%3ACI+branch%3Amain)
[![docs](https://readthedocs.org/projects/valkey-py/badge/?version=latest&style=flat)](https://valkey-py.readthedocs.io/en/latest/)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![pypi](https://badge.fury.io/py/valkey.svg)](https://pypi.org/project/valkey/)
[![pre-release](https://img.shields.io/github/v/release/valkey-io/valkey-py?include_prereleases&label=latest-prerelease)](https://github.com/valkey-io/valkey-py/releases)
[![codecov](https://codecov.io/gh/valkey-io/valkey-py/branch/main/graph/badge.svg?token=yenl5fzxxr)](https://codecov.io/gh/valkey-io/valkey-py)

[Installation](#installation) |  [Usage](#usage) | [Documentation](#documentation) | [Advanced Topics](#advanced-topics) | [Contributing](https://github.com/valkey-io/valkey-py/blob/main/CONTRIBUTING.md)

---------------------------------------------

## Installation

Start a valkey via docker:

``` bash
docker run -p 6379:6379 -it valkey/valkey:latest
```

To install valkey-py, simply:

``` bash
$ pip install valkey
```

For faster performance, install valkey with libvalkey support, this provides a compiled response parser, and *for most cases* requires zero code changes.
By default, if libvalkey >= 2.3.2 is available, valkey-py will attempt to use it for response parsing.

``` bash
$ pip install "valkey[libvalkey]"
```

## Usage

### Basic Example

``` python
>>> import valkey
>>> r = valkey.Valkey(host='localhost', port=6379, db=0)
>>> r.set('foo', 'bar')
True
>>> r.get('foo')
b'bar'
```

The above code connects to localhost on port 6379, sets a value in Redis, and retrieves it. All responses are returned as bytes in Python, to receive decoded strings, set *decode_responses=True*.  For this, and more connection options, see [these examples](https://valkey-py.readthedocs.io/en/latest/examples.html).

### Migration from redis-py

You are encouraged to use the new class names, but to allow for a smooth transition alias are available:

``` python
>>> import valkey as redis
>>> r = redis.Redis(host='localhost', port=6379, db=0)
>>> r.set('foo', 'bar')
True
>>> r.get('foo')
b'bar'
```

#### RESP3 Support
To enable support for RESP3 change your connection object to include *protocol=3*

``` python
>>> import valkey
>>> r = valkey.Valkey(host='localhost', port=6379, db=0, protocol=3)
```

### Connection Pools

By default, valkey-py uses a connection pool to manage connections. Each instance of a Valkey class receives its own connection pool. You can however define your own [valkey.ConnectionPool](https://valkey-py.readthedocs.io/en/latest/connections.html#connection-pools).

``` python
>>> pool = valkey.ConnectionPool(host='localhost', port=6379, db=0)
>>> r = valkey.Valkey(connection_pool=pool)
```

Alternatively, you might want to look at [Async connections](https://valkey-py.readthedocs.io/en/latest/examples/asyncio_examples.html), or [Cluster connections](https://valkey-py.readthedocs.io/en/latest/connections.html#cluster-client), or even [Async Cluster connections](https://valkey-py.readthedocs.io/en/latest/connections.html#async-cluster-client).

### Valkey Commands

There is built-in support for all of the [out-of-the-box Valkey commands](https://valkey.io/commands). They are exposed using the raw Redis command names (`HSET`, `HGETALL`, etc.) except where a word (i.e. del) is reserved by the language. The complete set of commands can be found [here](https://github.com/valkey-io/valkey-py/tree/main/valkey/commands), or [the documentation](https://valkey-py.readthedocs.io/en/latest/commands.html).

## Documentation

Check out the [documentation](https://valkey-py.readthedocs.io/en/latest/index.html)

## Advanced Topics

The [official Valkey command documentation](https://valkey.io/commands)
does a great job of explaining each command in detail. valkey-py attempts
to adhere to the official command syntax. There are a few exceptions:

-   **MULTI/EXEC**: These are implemented as part of the Pipeline class.
    The pipeline is wrapped with the MULTI and EXEC statements by
    default when it is executed, which can be disabled by specifying
    transaction=False. See more about Pipelines below.

-   **SUBSCRIBE/LISTEN**: Similar to pipelines, PubSub is implemented as
    a separate class as it places the underlying connection in a state
    where it can\'t execute non-pubsub commands. Calling the pubsub
    method from the Valkey client will return a PubSub instance where you
    can subscribe to channels and listen for messages. You can only call
    PUBLISH from the Valkey client (see [this comment on issue
    #151](https://github.com/redis/redis-py/issues/151#issuecomment-1545015)
    for details).

For more details, please see the documentation on [advanced topics page](https://valkey-py.readthedocs.io/en/latest/advanced_features.html).

### Pipelines

The following is a basic example of a [Valkey pipeline](https://valkey.io/topics/pipelining/), a method to optimize round-trip calls, by batching Valkey commands, and receiving their results as a list.


``` python
>>> pipe = r.pipeline()
>>> pipe.set('foo', 5)
>>> pipe.set('bar', 18.5)
>>> pipe.set('blee', "hello world!")
>>> pipe.execute()
[True, True, True]
```

### PubSub

The following example shows how to utilize [Valkey Pub/Sub](https://valkey.io/topics/pubsub/) to subscribe to specific channels.

``` python
>>> r = valkey.Valkey(...)
>>> p = r.pubsub()
>>> p.subscribe('my-first-channel', 'my-second-channel', ...)
>>> p.get_message()
{'pattern': None, 'type': 'subscribe', 'channel': b'my-second-channel', 'data': 1}
```


--------------------------

### Author

valkey-py can be found [here](
https://github.com/valkey-io/valkey-py), or downloaded from [pypi](https://pypi.org/project/valkey/).
It was created as a fork of [redis-py](https://github.com/redis/redis-py)

Special thanks to:

-   Andy McCurdy (<sedrik@gmail.com>) the original author of redis-py.
-   Ludovico Magnocavallo, author of the original Python Redis client,
    from which some of the socket code is still used.
-   Alexander Solovyov for ideas on the generic response callback
    system.
-   Paul Hubbard for initial packaging support in redis-py.

[![Valkey](./docs/logo-valkey.png)](https://valkey.io/)
