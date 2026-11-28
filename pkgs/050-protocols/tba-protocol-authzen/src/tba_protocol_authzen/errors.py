"""Authorization API 1.0 mapping errors."""


class AuthzenProtocolError(ValueError):
    """Base error for invalid AuthZEN protocol material."""


class AuthzenSchemaError(AuthzenProtocolError):
    """Raised when an AuthZEN entity or message has the wrong shape."""


class AuthzenOperationUnavailableError(AuthzenProtocolError):
    """Raised when an optional PDP operation is not configured."""


__all__ = [
    "AuthzenOperationUnavailableError",
    "AuthzenProtocolError",
    "AuthzenSchemaError",
]
