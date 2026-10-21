from __future__ import annotations

import pytest
import valkey.exceptions

exceptions = []
for name in dir(valkey.exceptions):
    cls_ = getattr(valkey.exceptions, name)
    try:
        if issubclass(cls_, BaseException):
            exceptions.append(pytest.param(cls_, id=name))
    except TypeError:
        pass


@pytest.mark.parametrize("cls", exceptions)
def test_exception_inheritance(cls: type[Exception]) -> None:
    """Verify all exceptions inherit from ValkeyError."""

    msg = f"{cls.__name__} is not a subclass of ValkeyError"
    assert issubclass(cls, valkey.exceptions.ValkeyError), msg
