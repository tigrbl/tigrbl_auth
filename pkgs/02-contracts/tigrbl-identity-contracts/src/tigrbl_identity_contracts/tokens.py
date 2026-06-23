from __future__ import annotations

from datetime import timedelta
from typing import Final

from tigrbl_identity_core.errors import (
    InvalidRefreshTokenError,
    RefreshTokenError,
    RefreshTokenReuseError,
)

DEFAULT_ACCESS_TOKEN_TTL: Final[timedelta] = timedelta(minutes=60)
DEFAULT_REFRESH_TOKEN_TTL: Final[timedelta] = timedelta(days=7)


__all__ = [
    "DEFAULT_ACCESS_TOKEN_TTL",
    "DEFAULT_REFRESH_TOKEN_TTL",
    "InvalidRefreshTokenError",
    "RefreshTokenError",
    "RefreshTokenReuseError",
]
