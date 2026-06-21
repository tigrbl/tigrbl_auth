from __future__ import annotations

from typing import TypedDict

from tigrbl_identity_core.typing import StrUUID


class JWTPayload(TypedDict, total=False):
    sub: StrUUID
    tid: StrUUID
    typ: str
    iat: int
    exp: int
    jti: str


class RefreshTokenError(Exception):
    """Base class for refresh token lifecycle errors."""


class InvalidRefreshTokenError(RefreshTokenError):
    """Raised when a refresh token is unknown, expired, revoked, or inactive."""


class RefreshTokenReuseError(RefreshTokenError):
    """Raised when refresh token reuse is detected."""


__all__ = [
    "InvalidRefreshTokenError",
    "JWTPayload",
    "RefreshTokenError",
    "RefreshTokenReuseError",
]
