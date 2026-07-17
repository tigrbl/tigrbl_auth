"""JOSE suite mapping and selection errors."""


class JoseProtocolError(ValueError):
    """Base error for a JOSE protocol-family mapping failure."""


class UnsupportedJoseMediaTypeError(JoseProtocolError):
    """Raised when no supported JOSE artifact matches a media type."""


class UnsupportedJoseMigrationError(JoseProtocolError):
    """Raised when no deterministic suite migration is defined."""


__all__ = [
    "JoseProtocolError",
    "UnsupportedJoseMediaTypeError",
    "UnsupportedJoseMigrationError",
]
