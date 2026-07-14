"""Composable pushed-authorization persistence capability."""

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
    PushedAuthorizationPersistenceRequest,
    PushedAuthorizationResult,
)


PersistenceTarget: TypeAlias = Callable[
    [PushedAuthorizationPersistenceRequest],
    PushedAuthorizationResult
    | Mapping[str, object]
    | Awaitable[PushedAuthorizationResult | Mapping[str, object]],
]
AuditTarget: TypeAlias = Callable[
    [Mapping[str, object]], None | Awaitable[None]
]


class PushedAuthorizationCapability(Capability):
    """Coordinate durable pushed-request creation and optional audit."""

    def __init__(
        self,
        persist_request: PersistenceTarget | None,
        record_audit_event: AuditTarget | None = None,
    ) -> None:
        self._persist_request = persist_request
        self._record_audit_event = record_audit_event
        super().__init__(
            CapabilityDefinition("oauth.pushed-authorization", "1.0"),
            operations={
                "push_authorization_request": CapabilityOperation(
                    target=self.push if persist_request is not None else None,
                    delegated=True,
                ),
                "record_audit_event": CapabilityOperation(
                    target=record_audit_event,
                    required=False,
                    delegated=True,
                ),
            },
            state=lambda: CapabilityState(
                ready=self._persist_request is not None,
                status="ready" if self._persist_request is not None else "unbound",
                details={"audit_bound": self._record_audit_event is not None},
            ),
        )

    async def push(
        self,
        request: PushedAuthorizationPersistenceRequest,
    ) -> PushedAuthorizationResult:
        if not isinstance(request, PushedAuthorizationPersistenceRequest):
            raise TypeError(
                "request must be a PushedAuthorizationPersistenceRequest"
            )
        if self._persist_request is None:  # construction rejects this path
            raise NotImplementedError("pushed authorization target is not bound")

        value = self._persist_request(request)
        if inspect.isawaitable(value):
            value = await value
        if isinstance(value, PushedAuthorizationResult):
            result = value
        elif isinstance(value, Mapping):
            result = PushedAuthorizationResult(
                request_uri=str(value.get("request_uri") or ""),
                expires_in=int(value.get("expires_in") or 0),
                record_id=(
                    str(value["record_id"])
                    if value.get("record_id") is not None
                    else None
                ),
            )
        else:
            raise TypeError(
                "pushed authorization target must return a typed result or mapping"
            )

        if self._record_audit_event is not None:
            event = self._record_audit_event(
                {
                    "event_type": "authorization.par.created",
                    "target_type": "par_request",
                    "target_id": result.record_id or result.request_uri,
                    "client_id": request.client_id,
                    "tenant_id": request.tenant_id,
                    "details": {"request_uri": result.request_uri},
                }
            )
            if inspect.isawaitable(event):
                await event
        return result


__all__ = [
    "AuditTarget",
    "PersistenceTarget",
    "PushedAuthorizationCapability",
    "PushedAuthorizationPersistenceRequest",
    "PushedAuthorizationResult",
]
