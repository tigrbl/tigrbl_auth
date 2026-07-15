"""CWT protocol mapping errors."""


class CwtProtocolError(ValueError):
    """Base error for an RFC 8392 mapping failure."""


class UnsupportedCwtMediaTypeError(CwtProtocolError):
    """Raised when the selected carrier is not `application/cwt`."""


__all__ = ["CwtProtocolError", "UnsupportedCwtMediaTypeError"]
