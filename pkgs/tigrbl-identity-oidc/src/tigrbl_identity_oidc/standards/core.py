"""OIDC Core certified-core aggregator.

This module provides a named, non-wrapper aggregation point for the OIDC Core
release path. It intentionally re-exports selected discovery, ID Token, and
UserInfo helpers without depending on star-import shims.
"""

from __future__ import annotations

from tigrbl_auth.standards.oidc.discovery import include_oidc_discovery
from tigrbl_auth.standards.oidc.id_token import mint_id_token, oidc_hash, rotate_rsa_jwt_key, verify_id_token
from tigrbl_auth.standards.oidc.userinfo import include_oidc_userinfo

OIDC_CORE_COMPONENTS = (
    "discovery",
    "id_token",
    "userinfo",
)

__all__ = [
    "OIDC_CORE_COMPONENTS",
    "include_oidc_discovery",
    "include_oidc_userinfo",
    "mint_id_token",
    "oidc_hash",
    "rotate_rsa_jwt_key",
    "verify_id_token",
]
