from __future__ import annotations

import sys
from typing import Any, Literal, overload

from ..exceptions import DataError

if sys.version_info >= (3, 11):
    from typing import Never
else:
    from typing_extensions import Never


class Encoder:
    "Encode strings to bytes-like and decode bytes-like to strings"

    __slots__ = "encoding", "encoding_errors", "decode_responses"

    def __init__(
        self,
        encoding: str,
        encoding_errors: (
            Literal["ignore", "replace", "strict", "xmlcharrefreplace"] | str
        ),
        decode_responses: bool,
    ) -> None:
        self.encoding = encoding
        self.encoding_errors = encoding_errors
        self.decode_responses = decode_responses

    @overload
    def encode(self, value: memoryview[bytes]) -> memoryview[bytes]: ...

    @overload
    def encode(self, value: bool) -> Never: ...

    @overload
    def encode(self, value: bytes | int | float | str) -> bytes: ...

    @overload
    def encode(self, value: Any) -> Never: ...

    def encode(
        self, value: bytes | memoryview[bytes] | int | float | str
    ) -> bytes | memoryview[bytes]:
        "Return a bytestring or bytes-like representation of the value"
        if isinstance(value, (bytes, memoryview)):
            return value
        elif isinstance(value, bool):
            # special case bool since it is a subclass of int
            raise DataError(
                "Invalid input of type: 'bool'. Convert to a "
                "bytes, string, int or float first."
            )
        elif isinstance(value, (int, float)):
            value = repr(value).encode()
        elif not isinstance(value, str):
            # a value we don't know how to deal with. throw an error
            typename = type(value).__name__
            raise DataError(
                f"Invalid input of type: '{typename}'. "
                f"Convert to a bytes, string, int or float first."
            )
        if isinstance(value, str):
            value = value.encode(self.encoding, self.encoding_errors)
        return value

    @overload
    def decode(
        self,
        value: bytes | memoryview[bytes] | str,
        force: Literal[True],
    ) -> str: ...

    @overload
    def decode(
        self,
        value: bytes | memoryview[bytes] | str,
        force: Literal[False],
    ) -> bytes | memoryview[bytes] | str: ...

    def decode(
        self,
        value: bytes | memoryview[bytes] | str,
        force: bool = False,
    ) -> Any:
        "Return a unicode string from the bytes-like representation"
        if self.decode_responses or force:
            if isinstance(value, memoryview):
                value = value.tobytes()
            if isinstance(value, bytes):
                value = value.decode(self.encoding, self.encoding_errors)
        return value
