"""Compatibility facade for shared REST helper imports."""

from tigrbl_identity_server.rest.shared import (
    _jwt,
    _require_tls,
    _front_channel_logout,
    _back_channel_logout,
    allowed_grant_types,
)

__all__ = [
    "_jwt",
    "_require_tls",
    "_front_channel_logout",
    "_back_channel_logout",
    "allowed_grant_types",
]
