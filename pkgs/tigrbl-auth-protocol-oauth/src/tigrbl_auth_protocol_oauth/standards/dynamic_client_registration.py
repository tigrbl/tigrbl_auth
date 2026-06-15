from __future__ import annotations

"""OAuth 2.0 Dynamic Client Registration Protocol owner module."""

from dataclasses import dataclass
from typing import Final

STATUS: Final[str] = "dynamic-client-registration-runtime"
RFC7591_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc7591"


@dataclass(frozen=True, slots=True)
class StandardOwner:
    label: str
    title: str
    runtime_status: str
    public_surface: tuple[str, ...]
    notes: str


OWNER = StandardOwner(
    label="RFC 7591",
    title="OAuth 2.0 Dynamic Client Registration Protocol",
    runtime_status=STATUS,
    public_surface=("/register",),
    notes="Authoritative standards-tree owner module. Canonical /register route is now mounted on the release path with request/response schemas, persistence backing, and OpenAPI visibility.",
)


def describe() -> dict[str, object]:
    return {
        "label": OWNER.label,
        "title": OWNER.title,
        "runtime_status": OWNER.runtime_status,
        "public_surface": list(OWNER.public_surface),
        "notes": OWNER.notes,
        "spec_url": RFC7591_SPEC_URL,
    }


__all__ = ["STATUS", "RFC7591_SPEC_URL", "StandardOwner", "OWNER", "describe"]
