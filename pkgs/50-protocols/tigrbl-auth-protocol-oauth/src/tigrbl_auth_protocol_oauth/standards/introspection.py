"""OAuth token introspection compatibility exports.

Endpoint routes are owned by ``tigrbl_identity_storage_runtime.introspection``.
"""

from __future__ import annotations

from tigrbl_identity_storage_runtime.introspection import (
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
    _protected_resource_verifier_contract,
)

__all__ = [
    "RFC7662_SPEC_URL",
    "include_introspection_endpoint",
    "include_rfc7662",
    "_protected_resource_verifier_contract",
    "register_token",
    "register_token_async",
    "unregister_token",
    "introspect_token",
    "introspect_token_async",
    "reset_tokens",
    "reset_tokens_async",
]
