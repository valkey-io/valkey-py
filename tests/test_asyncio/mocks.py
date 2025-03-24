import anyio

# Helper Mocking classes for the tests.


class MockStream:
    """
    A class simulating an anyio input buffer, optionally raising a
    special exception every other read.
    """

    class TestError(BaseException):
        pass

    def __init__(self, data, interrupt_every=0):
        self.data = data
        self.counter = 0
        self.pos = 0
        self.interrupt_every = interrupt_every

    def tick(self):
        self.counter += 1
        if not self.interrupt_every:
            return
        if (self.counter % self.interrupt_every) == 0:
            raise self.TestError()

    async def receive(self, want):
        self.tick()
        want = 5
        result = self.data[self.pos : self.pos + want]
        if not result:
            raise anyio.EndOfStream()
        self.pos += len(result)
        return result

    async def receive_until(self, delimiter, maxsize):
        self.tick()
        find = self.data.find(delimiter, self.pos)
        if find < 0:
            # If we can't find delimiter, check if we have enough data to return
            available = len(self.data) - self.pos
            if available == 0:
                raise anyio.IncompleteRead()
            if available > maxsize:
                raise anyio.DelimiterNotFound()
            # Return all available data if we can't find delimiter
            result = self.data[self.pos :]
            self.pos = len(self.data)
            return result

        chunk_size = find - self.pos
        if chunk_size > maxsize:
            raise anyio.DelimiterNotFound()

        # Found delimiter within maxsize, return up to delimiter
        result = self.data[self.pos : find]
        self.pos = find + len(delimiter)
        return result

    async def receive_exactly(self, length):
        self.tick()
        result = self.data[self.pos : self.pos + length]
        if len(result) < length:
            raise anyio.IncompleteRead()
        elif not result:
            raise anyio.EndOfStream()
        self.pos += len(result)
        return result
