"""OAuth 2.0 Dynamic Client Registration Management Protocol owner module."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from tigrbl_client_registration_capability import ClientRegistrationCapability
from tigrbl_identity_contracts.oauth import (
    ClientRegistrationRecord,
    ClientRegistrationUpdateRequest,
)
from tigrbl_identity_core.standards import StandardOwner, describe_owner

STATUS: Final[str] = "persistence-backed-client-management-runtime"
RFC7592_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc7592"


OWNER = StandardOwner(
    label="RFC 7592",
    title="OAuth 2.0 Dynamic Client Registration Management Protocol",
    runtime_status=STATUS,
    public_surface=("/register/{client_id}",),
    notes="Authoritative standards-tree owner module. Registration management is mounted on the public release path with bearer-authenticated GET/PUT/DELETE semantics, durable client-registration metadata persistence, and audit-observable update/delete behavior.",
)


class ClientRegistrationManagementDisabledError(RuntimeError):
    """Raised when composition disables RFC 7592 management."""


@dataclass(frozen=True, slots=True)
class RFC7592ClientRegistrationManagementService:
    """Map RFC 7592 lifecycle operations to the registration capability."""

    capability: ClientRegistrationCapability
    enabled: bool = True

    def _require_enabled(self) -> None:
        if not self.enabled:
            raise ClientRegistrationManagementDisabledError(
                f"RFC 7592 support is disabled: {RFC7592_SPEC_URL}"
            )

    async def get(self, client_id: str) -> ClientRegistrationRecord | None:
        self._require_enabled()
        call = await self.capability.call("get_registration", client_id)
        if call.value is not None and not isinstance(
            call.value, ClientRegistrationRecord
        ):
            raise TypeError(
                "client.registration must return ClientRegistrationRecord or None"
            )
        return call.value

    async def update(
        self,
        request: ClientRegistrationUpdateRequest,
    ) -> ClientRegistrationRecord:
        self._require_enabled()
        call = await self.capability.call("update_registration", request)
        if not isinstance(call.value, ClientRegistrationRecord):
            raise TypeError("client.registration must return ClientRegistrationRecord")
        return call.value

    async def delete(self, client_id: str) -> ClientRegistrationRecord:
        self._require_enabled()
        call = await self.capability.call("disable_registration", client_id)
        if not isinstance(call.value, ClientRegistrationRecord):
            raise TypeError("client.registration must return ClientRegistrationRecord")
        return call.value


def describe() -> dict[str, object]:
    return describe_owner(
        OWNER,
        spec_url=RFC7592_SPEC_URL,
    )


__all__ = [
    "STATUS",
    "RFC7592_SPEC_URL",
    "ClientRegistrationManagementDisabledError",
    "RFC7592ClientRegistrationManagementService",
    "StandardOwner",
    "OWNER",
    "describe",
]
