from __future__ import annotations

from datetime import timedelta
from typing import Final


DEFAULT_ACCESS_TOKEN_TTL: Final[timedelta] = timedelta(minutes=60)
DEFAULT_REFRESH_TOKEN_TTL: Final[timedelta] = timedelta(days=7)


class RefreshTokenError(Exception):
    """Base class for refresh token lifecycle errors."""


class InvalidRefreshTokenError(RefreshTokenError):
    """Raised when a refresh token is unknown, expired, revoked, or inactive."""


class RefreshTokenReuseError(RefreshTokenError):
    """Raised when refresh token reuse is detected."""


__all__ = [
    "DEFAULT_ACCESS_TOKEN_TTL",
    "DEFAULT_REFRESH_TOKEN_TTL",
    "InvalidRefreshTokenError",
    "RefreshTokenError",
    "RefreshTokenReuseError",
]
