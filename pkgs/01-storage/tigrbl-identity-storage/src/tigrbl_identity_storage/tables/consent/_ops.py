"""Consent-owned lifecycle helpers formerly exposed by storage persistence."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from .._ops import create_record
from .._sync import run_async
from ..engine import storage_session
from ._table import Consent


async def record_consent_async(
    *,
    user_id: UUID,
    tenant_id: UUID,
    client_id: UUID,
    scope: str,
    claims: dict[str, Any] | None = None,
    expires_at: datetime | None = None,
) -> Consent:
    async with storage_session() as db:
        return await create_record(
            Consent,
            db,
            {
                "user_id": user_id,
                "tenant_id": tenant_id,
                "client_id": client_id,
                "scope": scope,
                "claims": claims,
                "expires_at": expires_at,
                "state": "active",
            },
        )


async def revoke_consent_async(consent_id: UUID) -> Consent | None:
    async with storage_session() as db:
        return await Consent.revoke_for_user(db, consent_id=consent_id)


def record_consent(**kwargs):
    return run_async(record_consent_async(**kwargs))
def revoke_consent(consent_id):
    return run_async(revoke_consent_async(consent_id))


__all__ = ["record_consent", "record_consent_async", "revoke_consent", "revoke_consent_async"]
