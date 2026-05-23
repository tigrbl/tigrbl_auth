"""Custom JWT-related exceptions for tigrbl_auth.

The tigrbl_auth package relies on swarmauri token services and avoids direct
use of external libraries such as PyJWT.  These lightweight exception classes
provide a small surface that mirrors the errors previously exposed by PyJWT
without requiring a dependency on that package.
"""

from __future__ import annotations


class InvalidTokenError(Exception):
    """Raised when a JWT cannot be decoded or fails validation."""


class InvalidKeyError(Exception):
    """Raised when a suitable key for JWT processing cannot be found."""


class IdentityError(Exception):
    """Base error for identity package primitives."""


class IdentityValidationError(IdentityError):
    """Raised when an identity primitive or contract fails validation."""


class IdentityConfigurationError(IdentityError):
    """Raised when package/runtime configuration is invalid."""


class IdentityAuthorizationError(IdentityError):
    """Raised when a principal is not authorized for an operation."""


__all__ = [
    "IdentityAuthorizationError",
    "IdentityConfigurationError",
    "IdentityError",
    "IdentityValidationError",
    "InvalidKeyError",
    "InvalidTokenError",
]
