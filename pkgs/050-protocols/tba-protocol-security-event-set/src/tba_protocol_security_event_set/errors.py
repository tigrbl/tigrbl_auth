"""SET protocol mapping errors."""


class SetProtocolError(ValueError):
    """Base error for an RFC 8417 mapping failure."""


class UnsupportedSetMediaTypeError(SetProtocolError):
    """Raised for a carrier other than `application/secevent+jwt`."""


class SetUsageError(SetProtocolError):
    """Raised when a SET is used as an ID or access token."""


__all__ = ["SetProtocolError", "SetUsageError", "UnsupportedSetMediaTypeError"]
