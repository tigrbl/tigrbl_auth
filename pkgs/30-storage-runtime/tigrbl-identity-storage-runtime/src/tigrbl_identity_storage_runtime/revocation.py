"""Carrier-neutral durable token-revocation compatibility adapters."""

from .token_lifecycle import (
    is_revoked,
    is_revoked_async,
    is_token_revoked,
    is_token_revoked_async,
    reset_revocations,
    reset_revocations_async,
    reset_token_state,
    reset_token_state_async,
    revoke_token,
    revoke_token_async,
)

__all__ = [
    "is_revoked",
    "is_revoked_async",
    "is_token_revoked",
    "is_token_revoked_async",
    "reset_revocations",
    "reset_revocations_async",
    "reset_token_state",
    "reset_token_state_async",
    "revoke_token",
    "revoke_token_async",
]
