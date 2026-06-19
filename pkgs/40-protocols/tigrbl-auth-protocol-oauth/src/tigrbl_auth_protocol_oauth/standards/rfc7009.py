"""Compatibility facade for canonical RFC 7009 revocation helpers."""

from tigrbl_auth_protocol_oauth.standards.revocation import (
    RFC7009_SPEC_URL,
    include_rfc7009,
    include_revocation_endpoint,
    is_revoked,
    is_revoked_async,
    reset_revocations,
    reset_revocations_async,
    revoke_token,
    revoke_token_async,
)

__all__ = [
    "RFC7009_SPEC_URL",
    "include_revocation_endpoint",
    "include_rfc7009",
    "revoke_token",
    "revoke_token_async",
    "is_revoked",
    "is_revoked_async",
    "reset_revocations",
    "reset_revocations_async",
]
