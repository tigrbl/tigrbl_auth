"""Compatibility facade for historical ``tigrbl_auth.routers.shared`` imports."""

from tigrbl_auth.api.rest.shared import (
    _jwt,
    _pwd_backend,
    _require_tls,
    _front_channel_logout,
    _back_channel_logout,
    allowed_grant_types,
)

__all__ = [
    "_jwt",
    "_pwd_backend",
    "_require_tls",
    "_front_channel_logout",
    "_back_channel_logout",
    "allowed_grant_types",
]
