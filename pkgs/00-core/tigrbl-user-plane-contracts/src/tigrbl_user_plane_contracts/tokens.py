from __future__ import annotations


class RefreshTokenError(Exception):
    """Base class for refresh token lifecycle errors."""


class InvalidRefreshTokenError(RefreshTokenError):
    """Raised when a refresh token is unknown, expired, revoked, or inactive."""


class RefreshTokenReuseError(RefreshTokenError):
    """Raised when refresh token reuse is detected."""


__all__ = ["InvalidRefreshTokenError", "RefreshTokenError", "RefreshTokenReuseError"]
