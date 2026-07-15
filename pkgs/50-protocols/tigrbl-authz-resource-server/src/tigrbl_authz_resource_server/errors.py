"""Protected-resource profile mapping errors."""

from tigrbl_identity_contracts.resource_server import (
    ResourceServerError,
    TokenValidationError,
)


class ProtectedResourceProfileError(ResourceServerError):
    """Base error for protected-resource profile selection and mapping."""


class UnsupportedProtectedResourceProfileError(ProtectedResourceProfileError):
    """Raised when a protected-resource profile has no supported path."""


class ProtectedResourceBindingError(ProtectedResourceProfileError):
    """Raised when a wire obligation cannot map to a capability."""


__all__ = [
    "ProtectedResourceBindingError",
    "ProtectedResourceProfileError",
    "ResourceServerError",
    "TokenValidationError",
    "UnsupportedProtectedResourceProfileError",
]
