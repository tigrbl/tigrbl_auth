"""OIDC Core certified-core aggregator.

This module provides a named, non-wrapper aggregation point for the OIDC Core
release path. It intentionally re-exports selected discovery and ID Token
helpers plus descriptive UserInfo protocol ownership.
"""

from __future__ import annotations

from tigrbl_auth_protocol_oidc.standards.id_token import (
    mint_id_token,
    oidc_hash,
    rotate_rsa_jwt_key,
    verify_id_token,
)
from tigrbl_auth_protocol_oidc.standards.userinfo import (
    OWNER as USERINFO_OWNER,
    describe as describe_userinfo,
)

OIDC_CORE_COMPONENTS = (
    "discovery",
    "id_token",
    "userinfo",
)

__all__ = [
    "OIDC_CORE_COMPONENTS",
    "USERINFO_OWNER",
    "describe_userinfo",
    "mint_id_token",
    "oidc_hash",
    "rotate_rsa_jwt_key",
    "verify_id_token",
]
