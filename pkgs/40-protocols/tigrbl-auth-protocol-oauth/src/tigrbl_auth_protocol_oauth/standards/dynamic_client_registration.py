from __future__ import annotations

"""OAuth 2.0 Dynamic Client Registration Protocol owner module."""

from typing import Final

from tigrbl_identity_core.standards import StandardOwner, describe_owner

STATUS: Final[str] = "dynamic-client-registration-runtime"
RFC7591_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc7591"




OWNER = StandardOwner(
    label="RFC 7591",
    title="OAuth 2.0 Dynamic Client Registration Protocol",
    runtime_status=STATUS,
    public_surface=("/register",),
    notes="Authoritative standards-tree owner module. Canonical /register route is now mounted on the release path with request/response schemas, persistence backing, and OpenAPI visibility.",
)


def describe() -> dict[str, object]:
    return describe_owner(
        OWNER,
        spec_url=RFC7591_SPEC_URL,
    )


__all__ = ["STATUS", "RFC7591_SPEC_URL", "StandardOwner", "OWNER", "describe"]
