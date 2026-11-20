"""Legacy RFC 7662 convenience surface over split owners."""

from __future__ import annotations

from typing import Any

from tba_protocol_oauth.standards._introspection_activity import (
    apply_introspection_activity_constraints,
)
from tba_protocol_oauth.standards.introspection import RFC7662_SPEC_URL
from tba_runtime_identity.settings import settings
from tba_runtime_identity_storage.introspection import (
    introspect_token as _introspect_token,
    introspect_token_async as _introspect_token_async,
    register_token,
    register_token_async,
    reset_tokens,
    reset_tokens_async,
    unregister_token,
)


def introspect_token(token: str) -> dict[str, Any]:
    if not settings.enable_rfc7662:
        raise RuntimeError(f"RFC 7662 support is disabled: {RFC7662_SPEC_URL}")
    return apply_introspection_activity_constraints(_introspect_token(token))


async def introspect_token_async(token: str) -> dict[str, Any]:
    if not settings.enable_rfc7662:
        raise RuntimeError(f"RFC 7662 support is disabled: {RFC7662_SPEC_URL}")
    payload = await _introspect_token_async(token)
    return apply_introspection_activity_constraints(payload)


__all__ = [
    "RFC7662_SPEC_URL",
    "introspect_token",
    "introspect_token_async",
    "register_token",
    "register_token_async",
    "reset_tokens",
    "reset_tokens_async",
    "unregister_token",
]
