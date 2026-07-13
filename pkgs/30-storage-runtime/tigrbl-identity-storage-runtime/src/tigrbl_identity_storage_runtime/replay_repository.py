"""Durable atomic replay reservation repository."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy.exc import IntegrityError

from tigrbl_identity_contracts.replay import ReplayReservationRequest, ReplayReservationResult, ReplayStoreDescriptor
from tigrbl_identity_storage.tables.replay_reservation import ReplayReservation
from tigrbl_identity_storage.tables.engine import storage_session
from tigrbl_replay_bases import ReplayReservationBase


def _items(value: Any) -> list[Any]:
    if isinstance(value, dict):
        return list(value.get("items") or value.get("data") or ())
    return list(value or ())


class SqlReplayReservationRepository(ReplayReservationBase):
    """SQL-backed check-and-reserve using the unique digest constraint."""

    provider_id = "replay:sql"
    persistence = "durable"
    descriptor = ReplayStoreDescriptor(
        provider_id=provider_id,
        persistence=persistence,
        atomic_reservation=True,
        namespaces=("*",),
        tenant_isolation="key-scoped optional tenant identifier",
        expiry="required timezone-aware expires_at",
        retention="until expires_at plus operator purge interval",
        purge="expired rows are replaceable; scheduled purge is operator-owned",
        audit="reservation result exposes provider and digest; database audit is deployment-owned",
        availability="database transaction and unique-constraint availability",
    )

    async def check_and_reserve(
        self, request: ReplayReservationRequest, /
    ) -> ReplayReservationResult:
        digest = self.digest_key(request.key)
        now = datetime.now(timezone.utc)
        try:
            async with storage_session() as db:
                listed = await ReplayReservation.handlers.list.core(
                    {"payload": {"filters": {"key_digest": digest}}, "db": db}
                )
                rows = _items(listed)
                if rows:
                    existing = rows[0]
                    expiry = getattr(existing, "expires_at", None)
                    if expiry is None or expiry > now:
                        return ReplayReservationResult(
                            False,
                            digest,
                            expiry or request.expires_at,
                            duplicate=True,
                            provider_id=self.provider_id,
                        )
                    await ReplayReservation.handlers.delete.core(
                        {"path_params": {"id": getattr(existing, "id")}, "db": db}
                    )
                await ReplayReservation.handlers.create.core(
                    {
                        "payload": {
                            "namespace": request.key.namespace,
                            "key_digest": digest,
                            "tenant_id": request.key.tenant_id,
                            "issuer": request.key.issuer,
                            "expires_at": request.expires_at,
                            "reservation_context": dict(request.context),
                        },
                        "db": db,
                    }
                )
        except IntegrityError:
            return ReplayReservationResult(
                False,
                digest,
                request.expires_at,
                duplicate=True,
                provider_id=self.provider_id,
            )
        return ReplayReservationResult(
            True,
            digest,
            request.expires_at,
            provider_id=self.provider_id,
        )


__all__ = ["SqlReplayReservationRepository"]
