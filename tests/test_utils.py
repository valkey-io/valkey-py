import pytest
from valkey.utils import pipeline


class _FakePipeline:
    def __init__(self):
        self.executed = False
        self.reset_calls = 0

    def execute(self):
        self.executed = True

    def reset(self):
        self.reset_calls += 1


class _FakeValkey:
    def __init__(self, fake_pipeline):
        self._fake_pipeline = fake_pipeline

    def pipeline(self):
        return self._fake_pipeline


class TestPipelineContextManager:
    def test_executes_and_resets_on_success(self):
        fake_pipeline = _FakePipeline()
        with pipeline(_FakeValkey(fake_pipeline)) as p:
            assert p is fake_pipeline
        assert fake_pipeline.executed is True
        assert fake_pipeline.reset_calls == 1

    def test_resets_but_does_not_execute_on_exception(self):
        # watch() checks a connection out of the pool right away, and the
        # pipeline only hands it back in reset(). Without reset() on this
        # path the connection stayed checked out until garbage collection.
        fake_pipeline = _FakePipeline()
        with pytest.raises(ValueError):
            with pipeline(_FakeValkey(fake_pipeline)):
                raise ValueError("boom")
        assert fake_pipeline.executed is False
        assert fake_pipeline.reset_calls == 1
