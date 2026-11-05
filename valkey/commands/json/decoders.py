import copy
import re

from ..helpers import nativestr


def bulk_of_jsons(d):
    """Replace serialized JSON values with objects in a
    bulk array response (list).
    """

    def _f(b):
        for index, item in enumerate(b):
            if item is not None:
                b[index] = d(item)
        return b

    return _f


def decode_dict_keys(obj):
    """Decode the keys of the given dictionary with utf-8."""
    newobj = copy.copy(obj)
    for k in obj.keys():
        if isinstance(k, bytes):
            newobj[k.decode("utf-8")] = newobj[k]
            newobj.pop(k)
    return newobj


def unstring(obj):
    """
    Attempt to parse string to native integer formats.
    One can't simply call int/float in a try/catch because there is a
    semantic difference between (for example) 15.0 and 15.
    """
    # The dot has to be escaped and the pattern anchored at both ends, or the
    # float pattern matches any character and a prefix is enough to convert:
    # "100" came back as the float 100.0, and "10x20" matched and then died in
    # float() with a ValueError that escaped to the caller. The integer pattern
    # is checked first so an integer stays an integer.
    if re.match(r"^\d+$", obj):
        return int(obj)
    if re.match(r"^\d+\.\d+$", obj):
        return float(obj)
    return obj


def decode_list(b):
    """
    Given a non-deserializable object, make a best effort to
    return a useful set of results.
    """
    if isinstance(b, list):
        return [nativestr(obj) for obj in b]
    elif isinstance(b, bytes):
        return unstring(nativestr(b))
    elif isinstance(b, str):
        return unstring(b)
    return b
