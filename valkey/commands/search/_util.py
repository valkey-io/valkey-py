def to_string(s):
    if isinstance(s, str):
        return s
    elif isinstance(s, bytes):
        return s.decode("utf-8", "ignore")
    else:
        return s  # Not a string we care about


def to_string_or_bytes(s, preserve_bytes=False, binary_fields=None, field_name=None):
    """Convert value to string or preserve as bytes based on parameters."""
    if isinstance(s, str):
        return s
    elif isinstance(s, bytes):
        if preserve_bytes and (binary_fields is None or field_name in binary_fields):
            return s  # Keep as bytes
        return s.decode("utf-8", "ignore")
    else:
        return s  # Not a string we care about
