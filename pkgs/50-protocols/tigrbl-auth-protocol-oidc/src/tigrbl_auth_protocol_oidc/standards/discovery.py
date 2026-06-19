"""OIDC discovery compatibility exports.

Discovery and JWKS routes are owned by
``tigrbl_identity_storage.tables.realm._oidc_discovery``.
"""

from __future__ import annotations

from tigrbl_identity_storage.tables.realm._oidc_discovery import (
    _build_openid_config,
    include_jwks,
    include_oidc_discovery,
    include_openid_configuration,
    refresh_discovery_cache,
)

__all__ = [
    "_build_openid_config",
    "refresh_discovery_cache",
    "include_openid_configuration",
    "include_jwks",
    "include_oidc_discovery",
]
