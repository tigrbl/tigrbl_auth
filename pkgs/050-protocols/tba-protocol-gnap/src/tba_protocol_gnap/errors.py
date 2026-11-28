"""RFC 9635 protocol mapping errors."""


class GnapProtocolError(ValueError):
    """Base error for invalid GNAP protocol material."""


class GnapSchemaError(GnapProtocolError):
    """Raised when a GNAP request or response has an invalid shape."""


class GnapOperationUnavailableError(GnapProtocolError):
    """Raised when an optional grant lifecycle operation is unavailable."""


__all__ = [
    "GnapOperationUnavailableError",
    "GnapProtocolError",
    "GnapSchemaError",
]
