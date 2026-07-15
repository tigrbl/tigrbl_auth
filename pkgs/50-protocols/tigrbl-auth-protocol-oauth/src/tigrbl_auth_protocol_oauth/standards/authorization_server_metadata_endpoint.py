"""OAuth authorization server metadata endpoint exports."""

from __future__ import annotations

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
