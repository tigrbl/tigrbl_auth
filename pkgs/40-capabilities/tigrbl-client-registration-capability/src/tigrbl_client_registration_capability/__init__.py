"""Composable protocol-neutral client registration lifecycle capability."""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable, Mapping
from typing import TypeAlias

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
    CapabilityState,
)
from tigrbl_identity_contracts.oauth import (
    ClientRegistrationCreateRequest,
    ClientRegistrationRecord,
    ClientRegistrationUpdateRequest,
)


CreateTarget: TypeAlias = Callable[
    [ClientRegistrationCreateRequest],
    ClientRegistrationRecord | Awaitable[ClientRegistrationRecord],
]
GetTarget: TypeAlias = Callable[
    [str],
    ClientRegistrationRecord
    | None
    | Awaitable[ClientRegistrationRecord | None],
]
UpdateTarget: TypeAlias = Callable[
    [ClientRegistrationUpdateRequest],
    ClientRegistrationRecord | Awaitable[ClientRegistrationRecord],
]
DisableTarget: TypeAlias = Callable[
    [str], ClientRegistrationRecord | Awaitable[ClientRegistrationRecord]
]
AuditTarget: TypeAlias = Callable[
    [Mapping[str, object]], None | Awaitable[None]
]


async def _await_record(value: object, *, operation: str) -> ClientRegistrationRecord:
    if inspect.isawaitable(value):
        value = await value
    if not isinstance(value, ClientRegistrationRecord):
        raise TypeError(f"{operation} must return ClientRegistrationRecord")
    return value


class ClientRegistrationCapability(Capability):
    """Coordinate registered-client durability and lifecycle observation."""

    def __init__(
        self,
        create_registration: CreateTarget | None,
        get_registration: GetTarget | None,
        update_registration: UpdateTarget | None,
        disable_registration: DisableTarget | None,
        record_audit_event: AuditTarget | None = None,
    ) -> None:
        self._create_registration = create_registration
        self._get_registration = get_registration
        self._update_registration = update_registration
        self._disable_registration = disable_registration
        self._record_audit_event = record_audit_event
        required_bound = all(
            target is not None
            for target in (
                create_registration,
                get_registration,
                update_registration,
                disable_registration,
            )
        )
        super().__init__(
            CapabilityDefinition("client.registration", "1.0"),
            operations={
                "register_client": CapabilityOperation(
                    target=self.register if create_registration is not None else None,
                    delegated=True,
                ),
                "get_registration": CapabilityOperation(
                    target=self.get if get_registration is not None else None,
                    delegated=True,
                ),
                "update_registration": CapabilityOperation(
                    target=self.update if update_registration is not None else None,
                    delegated=True,
                ),
                "disable_registration": CapabilityOperation(
                    target=self.disable if disable_registration is not None else None,
                    delegated=True,
                ),
                "record_audit_event": CapabilityOperation(
                    target=record_audit_event,
                    required=False,
                    delegated=True,
                ),
            },
            state=lambda: CapabilityState(
                ready=required_bound,
                status="ready" if required_bound else "unbound",
                details={"audit_bound": self._record_audit_event is not None},
            ),
        )

    async def _audit(self, payload: Mapping[str, object]) -> None:
        if self._record_audit_event is None:
            return
        value = self._record_audit_event(payload)
        if inspect.isawaitable(value):
            await value

    async def register(
        self, request: ClientRegistrationCreateRequest
    ) -> ClientRegistrationRecord:
        if not isinstance(request, ClientRegistrationCreateRequest):
            raise TypeError("request must be a ClientRegistrationCreateRequest")
        if self._create_registration is None:
            raise NotImplementedError("client registration create target is not bound")
        record = await _await_record(
            self._create_registration(request),
            operation="register_client",
        )
        await self._audit(
            {
                "event_type": "client.registration.created",
                "target_type": "client",
                "target_id": record.client_id,
                "tenant_id": record.tenant_id,
                "actor_client_id": record.client_id,
                "details": {
                    "redirect_uris": list(record.redirect_uris),
                    "grant_types": list(record.grant_types),
                    "response_types": list(record.response_types),
                    "token_endpoint_auth_method": record.metadata.get(
                        "token_endpoint_auth_method"
                    ),
                },
            }
        )
        return record

    async def get(self, client_id: str) -> ClientRegistrationRecord | None:
        if not client_id:
            raise ValueError("client_id is required")
        if self._get_registration is None:
            raise NotImplementedError("client registration read target is not bound")
        value = self._get_registration(client_id)
        if inspect.isawaitable(value):
            value = await value
        if value is not None and not isinstance(value, ClientRegistrationRecord):
            raise TypeError("get_registration must return ClientRegistrationRecord or None")
        return value

    async def update(
        self, request: ClientRegistrationUpdateRequest
    ) -> ClientRegistrationRecord:
        if not isinstance(request, ClientRegistrationUpdateRequest):
            raise TypeError("request must be a ClientRegistrationUpdateRequest")
        if self._update_registration is None:
            raise NotImplementedError("client registration update target is not bound")
        record = await _await_record(
            self._update_registration(request),
            operation="update_registration",
        )
        await self._audit(
            {
                "event_type": "client.registration.updated",
                "target_type": "client",
                "target_id": record.client_id,
                "tenant_id": record.tenant_id,
                "actor_client_id": record.client_id,
                "details": {"updated_fields": list(request.updated_fields)},
            }
        )
        return record

    async def disable(self, client_id: str) -> ClientRegistrationRecord:
        if not client_id:
            raise ValueError("client_id is required")
        if self._disable_registration is None:
            raise NotImplementedError("client registration disable target is not bound")
        record = await _await_record(
            self._disable_registration(client_id),
            operation="disable_registration",
        )
        await self._audit(
            {
                "event_type": "client.registration.deleted",
                "target_type": "client",
                "target_id": record.client_id,
                "tenant_id": record.tenant_id,
                "actor_client_id": None,
                "details": {
                    "registration_client_uri": record.registration_client_uri
                },
            }
        )
        return record


__all__ = [
    "AuditTarget",
    "ClientRegistrationCapability",
    "CreateTarget",
    "DisableTarget",
    "GetTarget",
    "UpdateTarget",
]
