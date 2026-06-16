"""Legacy RFC 7009 import surface backed by the durable standards implementation."""

from __future__ import annotations

from tigrbl_auth.standards.oauth2.revocation import (
    RFC7009_SPEC_URL,
    api,
    include_rfc7009,
    is_revoked,
    is_revoked_async,
    reset_revocations,
    reset_revocations_async,
    revoke,
    revoke_token,
    revoke_token_async,
    router,
)

__all__ = [
    "revoke_token",
    "revoke_token_async",
    "is_revoked",
    "is_revoked_async",
    "reset_revocations",
    "reset_revocations_async",
    "include_rfc7009",
    "revoke",
    "api",
    "router",
    "RFC7009_SPEC_URL",
]
