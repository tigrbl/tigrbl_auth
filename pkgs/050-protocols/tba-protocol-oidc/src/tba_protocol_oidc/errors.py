"""OIDC protocol mapping errors."""


class OidcProtocolError(ValueError):
    """Base error for a versioned OIDC wire mapping failure."""


class UnsupportedOidcRevisionError(OidcProtocolError):
    """Raised when no compatibility path exists for a requested revision."""


class OidcBindingError(OidcProtocolError):
    """Raised when a wire element cannot map to its semantic capability."""


__all__ = ["OidcBindingError", "OidcProtocolError", "UnsupportedOidcRevisionError"]
