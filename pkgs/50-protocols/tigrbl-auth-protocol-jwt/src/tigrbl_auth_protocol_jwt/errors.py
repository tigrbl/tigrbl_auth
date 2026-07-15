"""JWT protocol mapping errors."""


class JwtProtocolError(ValueError):
    """Base error for an RFC 7519 mapping failure."""


class UnsupportedJwtMediaTypeError(JwtProtocolError):
    """Raised when the selected artifact is not an application/JWT carrier."""


class JwtProfileRequiredError(JwtProtocolError):
    """Raised when a trust/use decision is attempted without a token profile."""


__all__ = ["JwtProfileRequiredError", "JwtProtocolError", "UnsupportedJwtMediaTypeError"]
