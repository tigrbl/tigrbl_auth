"""Protocol-neutral consent lifecycle contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Mapping, Protocol


@dataclass(frozen=True, slots=True)
class ConsentGrantRequest:
    user_id: str
    client_id: str
    scopes: tuple[str, ...]
    tenant_id: str | None = None
    claims: Mapping[str, Any] = field(default_factory=dict)
    expires_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class ConsentRevocationRequest:
    consent_id: str
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class ConsentRecord:
    consent_id: str
    user_id: str
    client_id: str
    scopes: tuple[str, ...]
    tenant_id: str | None = None
    claims: Mapping[str, Any] = field(default_factory=dict)
    granted_at: datetime | None = None
    expires_at: datetime | None = None
    revoked_at: datetime | None = None


class ConsentServicePort(Protocol):
    async def grant(self, request: ConsentGrantRequest, /) -> ConsentRecord: ...

    async def list_for_user(
        self,
        *,
        user_id: str,
        tenant_id: str | None = None,
    ) -> tuple[ConsentRecord, ...]: ...

    async def revoke(self, request: ConsentRevocationRequest, /) -> ConsentRecord | None: ...

    async def revoke_for_client(
        self,
        *,
        client_id: str,
        user_id: str | None = None,
        tenant_id: str | None = None,
    ) -> tuple[ConsentRecord, ...]: ...


__all__ = [
    "ConsentGrantRequest",
    "ConsentRecord",
    "ConsentRevocationRequest",
    "ConsentServicePort",
]
