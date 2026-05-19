"""Compatibility facade for canonical RFC 7009 revocation helpers."""

from tigrbl_auth.standards.oauth2.revocation import (
    RFC7009_SPEC_URL,
    api,
    include_revocation_endpoint,
    include_rfc7009,
    is_revoked,
    reset_revocations,
    revoke,
    revoke_token,
    router,
)

__all__ = [
    "RFC7009_SPEC_URL",
    "api",
    "router",
    "revoke_token",
    "is_revoked",
    "reset_revocations",
    "revoke",
    "include_revocation_endpoint",
    "include_rfc7009",
]
