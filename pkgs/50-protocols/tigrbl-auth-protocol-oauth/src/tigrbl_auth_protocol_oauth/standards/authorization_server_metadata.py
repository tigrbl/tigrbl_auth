"""OAuth authorization server metadata constants.

These constants collect the well-known JWKS path and issuer base URL.
OIDC modules should import from here rather than redefining these defaults.
"""

from __future__ import annotations

import os
from typing import Final

from tigrbl_identity_core.standards import StandardOwner, describe_owner

JWKS_PATH: Final[str] = "/.well-known/jwks.json"
ISSUER: Final[str] = os.getenv("AUTHN_ISSUER", "https://authn.example.com")
RFC8414_METADATA_PATH: Final[str] = "/.well-known/oauth-authorization-server"
RFC8414_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc8414"
OWNER = StandardOwner(
    label="RFC 8414",
    title="OAuth 2.0 Authorization Server Metadata",
    runtime_status="profile-aware-authorization-server-metadata",
    public_surface=(RFC8414_METADATA_PATH,),
    notes=("HTTP publication is composed above the protocol layer.",),
)


def describe() -> dict[str, object]:
    return describe_owner(
        OWNER,
        specification_version="RFC 8414",
        metadata_path=RFC8414_METADATA_PATH,
        spec_url=RFC8414_SPEC_URL,
    )

__all__ = [
    "ISSUER",
    "JWKS_PATH",
    "OWNER",
    "RFC8414_METADATA_PATH",
    "RFC8414_SPEC_URL",
    "describe",
]
