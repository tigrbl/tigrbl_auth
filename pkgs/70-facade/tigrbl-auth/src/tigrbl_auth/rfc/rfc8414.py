"""Compatibility facade for RFC 8414 semantics and runtime publication."""

from tigrbl_auth_protocol_oauth.standards.authorization_server_metadata import (
    ISSUER,
    JWKS_PATH,
    OWNER,
    RFC8414_METADATA_PATH,
    RFC8414_SPEC_URL,
    describe,
)

__all__ = [
    "ISSUER",
    "JWKS_PATH",
    "OWNER",
    "RFC8414_METADATA_PATH",
    "RFC8414_SPEC_URL",
    "describe",
]
