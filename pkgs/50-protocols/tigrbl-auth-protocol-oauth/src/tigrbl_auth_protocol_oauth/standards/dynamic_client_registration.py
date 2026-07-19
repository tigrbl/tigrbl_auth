"""OAuth 2.0 Dynamic Client Registration Protocol owner module."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from tigrbl_client_registration_capability import ClientRegistrationCapability
from tigrbl_identity_contracts.oauth import (
    ClientRegistrationCreateRequest,
    ClientRegistrationRecord,
)
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


class DynamicClientRegistrationDisabledError(RuntimeError):
    """Raised when composition disables RFC 7591 registration."""


@dataclass(frozen=True, slots=True)
class RFC7591DynamicClientRegistrationService:
    """Map normalized RFC 7591 input to client-registration capability calls."""

    capability: ClientRegistrationCapability
    enabled: bool = True

    async def register(
        self,
        request: ClientRegistrationCreateRequest,
    ) -> ClientRegistrationRecord:
        if not self.enabled:
            raise DynamicClientRegistrationDisabledError(
                f"RFC 7591 support is disabled: {RFC7591_SPEC_URL}"
            )
        call = await self.capability.call("register_client", request)
        if not isinstance(call.value, ClientRegistrationRecord):
            raise TypeError("client.registration must return ClientRegistrationRecord")
        return call.value


def describe() -> dict[str, object]:
    return describe_owner(
        OWNER,
        spec_url=RFC7591_SPEC_URL,
    )


__all__ = [
    "STATUS",
    "RFC7591_SPEC_URL",
    "DynamicClientRegistrationDisabledError",
    "RFC7591DynamicClientRegistrationService",
    "StandardOwner",
    "OWNER",
    "describe",
]
