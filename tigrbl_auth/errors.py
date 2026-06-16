"""Compatibility facade for canonical identity errors."""

from __future__ import annotations

from tigrbl_identity_core.errors import (
    IdentityAuthorizationError,
    IdentityConfigurationError,
    IdentityError,
    IdentityValidationError,
    InvalidKeyError,
    InvalidTokenError,
)

__all__ = [
    "IdentityAuthorizationError",
    "IdentityConfigurationError",
    "IdentityError",
    "IdentityValidationError",
    "InvalidKeyError",
    "InvalidTokenError",
]
