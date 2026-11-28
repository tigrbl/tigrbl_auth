"""Runtime composition for durable pushed authorization requests."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from tba_protocol_oauth.standards.pushed_authorization_requests import (
    RFC9126PushedAuthorizationService,
)
from tba_contracts_identity.oauth import (
    PushedAuthorizationPersistenceRequest,
    PushedAuthorizationResult,
)
from tba_runtime_identity_storage.ops.audit import append_audit_event_record
from tigrbl import field_value
from tba_runtime_identity_storage.ops.oauth_state import (
    persist_pushed_authorization_request,
)
from tba_capability_authorization_request_staging import PushedAuthorizationCapability


def build_pushed_authorization_capability(db: Any) -> PushedAuthorizationCapability:
    """Bind carrier-neutral PAR and audit operations to one durable session."""

    async def persist(
        request: PushedAuthorizationPersistenceRequest,
    ) -> PushedAuthorizationResult:
        row = await persist_pushed_authorization_request(
            {
                "payload": {
                    "client_id": request.client_id,
                    "tenant_id": request.tenant_id,
                    "params": dict(request.params),
                },
                "db": db,
            }
        )
        return PushedAuthorizationResult(
            request_uri=str(field_value(row, "request_uri") or ""),
            expires_in=int(field_value(row, "expires_in") or 0),
            record_id=(
                str(field_value(row, "id"))
                if field_value(row, "id") is not None
                else None
            ),
        )

    async def audit(event: Mapping[str, object]) -> None:
        payload = dict(event)
        payload["actor_client_id"] = payload.pop("client_id", None)
        await append_audit_event_record({"payload": payload, "db": db})

    return PushedAuthorizationCapability(persist, audit)


def build_rfc9126_pushed_authorization_service(
    db: Any,
    settings_obj: object,
) -> RFC9126PushedAuthorizationService:
    """Bind deployment feature state to the composed RFC 9126 service."""

    return RFC9126PushedAuthorizationService(
        build_pushed_authorization_capability(db),
        enabled=bool(getattr(settings_obj, "enable_rfc9126", False)),
    )


__all__ = [
    "build_pushed_authorization_capability",
    "build_rfc9126_pushed_authorization_service",
]
