"""Custom JWT-related exceptions for the JOSE package."""

from __future__ import annotations


class InvalidTokenError(Exception):
    """Raised when a JWT cannot be decoded or fails validation."""


class InvalidKeyError(Exception):
    """Raised when a suitable key for JWT processing cannot be found."""


__all__ = ["InvalidTokenError", "InvalidKeyError"]
