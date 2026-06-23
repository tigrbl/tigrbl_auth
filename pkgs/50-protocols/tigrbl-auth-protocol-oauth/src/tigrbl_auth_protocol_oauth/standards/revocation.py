"""OAuth token revocation compatibility exports.

Route publishers are owned by ``tigrbl_identity_storage_runtime.revocation``.
"""

from __future__ import annotations

from tigrbl_identity_storage_runtime.revocation import (
    CANONICAL_REVOCATION_PATH,
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
    "CANONICAL_REVOCATION_PATH",
    "include_revocation_endpoint",
    "include_rfc7009",
    "revoke_token",
    "revoke_token_async",
    "is_revoked",
    "is_revoked_async",
    "reset_revocations",
    "reset_revocations_async",
]
