"""OAuth token introspection compatibility exports.

Endpoint routes are owned by ``tigrbl_identity_storage.tables._oauth_introspection``.
"""

from __future__ import annotations

from tigrbl_identity_storage.tables._oauth_introspection import (
    RFC7662_SPEC_URL,
    include_introspection_endpoint,
    include_rfc7662,
    introspect_token,
    introspect_token_async,
    register_token,
    register_token_async,
    reset_tokens,
    reset_tokens_async,
    unregister_token,
)

__all__ = [
    "RFC7662_SPEC_URL",
    "include_introspection_endpoint",
    "include_rfc7662",
    "register_token",
    "register_token_async",
    "unregister_token",
    "introspect_token",
    "introspect_token_async",
    "reset_tokens",
    "reset_tokens_async",
]
