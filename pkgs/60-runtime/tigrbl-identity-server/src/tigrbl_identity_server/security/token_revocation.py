"""Runtime composition for durable token revocation."""

from __future__ import annotations

from collections.abc import Mapping

from tigrbl_auth_protocol_oauth.standards.revocation import (
    RFC7009RevocationService,
)
from tigrbl_identity_storage_runtime.ops.audit import append_audit_event_async
from tigrbl_identity_storage_runtime.token_lifecycle import revoke_token_async
from tigrbl_token_revocation_capability import TokenRevocationCapability


async def _record_audit_event(event: Mapping[str, object]) -> None:
    details = event.get("details")
    await append_audit_event_async(
        event_type=str(event.get("event_type") or "token.revoked"),
        target_type=str(event.get("target_type") or "token"),
        target_id=str(event.get("target_id") or ""),
        details=dict(details) if isinstance(details, Mapping) else {},
    )


token_revocation = TokenRevocationCapability(
    revoke_token_async,
    _record_audit_event,
)


def build_rfc7009_revocation_service(
    settings_obj: object,
) -> RFC7009RevocationService:
    """Bind deployment feature state to the composed revocation capability."""

    return RFC7009RevocationService(
        token_revocation,
        enabled=bool(getattr(settings_obj, "enable_rfc7009", False)),
    )


__all__ = [
    "build_rfc7009_revocation_service",
    "token_revocation",
]
