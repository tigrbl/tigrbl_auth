"""Compatibility exports for pure OIDC discovery metadata helpers."""

from tigrbl_auth_protocol_oidc.standards.discovery import (
    ISSUER,
    JWKS_PATH,
    OIDC_DISCOVERY_SPEC_URL,
    OWNER,
    _build_openid_config,
    _cached_openid_config,
    _settings_signature,
    describe,
    refresh_discovery_cache,
)

__all__ = [
    "ISSUER",
    "JWKS_PATH",
    "OIDC_DISCOVERY_SPEC_URL",
    "OWNER",
    "_build_openid_config",
    "_cached_openid_config",
    "_settings_signature",
    "describe",
    "refresh_discovery_cache",
]
