"""Compatibility facade for canonical RFC 7662 introspection helpers."""

from tigrbl_auth.standards.oauth2.introspection import (
    RFC7662_SPEC_URL,
    api,
    include_introspection_endpoint,
    include_rfc7662,
    introspect,
    introspect_token,
    register_token,
    reset_tokens,
    router,
    unregister_token,
)

__all__ = [
    "RFC7662_SPEC_URL",
    "api",
    "router",
    "register_token",
    "unregister_token",
    "introspect_token",
    "reset_tokens",
    "introspect",
    "include_introspection_endpoint",
    "include_rfc7662",
]
