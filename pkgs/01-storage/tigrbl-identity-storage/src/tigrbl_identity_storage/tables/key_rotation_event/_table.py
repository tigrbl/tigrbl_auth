"""Durable key rotation audit trail."""

from __future__ import annotations

import datetime as dt
import uuid
from typing import Any

from tigrbl_identity_storage.framework import (
    RestOltpTable,
    TenantColumn,
    Timestamped,
    S,
    acol,
    JSON,
    Mapped,
    String,
    TZDateTime,
    GUIDPk,
    ForeignKeySpec,
    PgUUID,
)


class KeyRotationEvent(RestOltpTable, GUIDPk, Timestamped, TenantColumn):
    __tablename__ = "key_rotation_events"
    __table_args__ = ({"schema": "authn"},)

    actor_user_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.users.id"), nullable=True, index=True)
    )
    actor_client_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=True, index=True)
    )
    key_kid: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    algorithm: Mapped[str | None] = acol(storage=S(String(64), nullable=True))
    action: Mapped[str] = acol(storage=S(String(64), nullable=False, default="rotate"))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="success"))
    details: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    occurred_at: Mapped[dt.datetime] = acol(
        storage=S(TZDateTime, nullable=False, default=lambda: dt.datetime.now(dt.timezone.utc))
    )

    @classmethod
    async def record_rotation(
        cls,
        db: Any,
        *,
        key_kid: str,
        algorithm: str | None = None,
        tenant_id: uuid.UUID | None = None,
        actor_user_id: uuid.UUID | None = None,
        actor_client_id: uuid.UUID | None = None,
        action: str = "rotate",
        status: str = "success",
        details: dict | None = None,
    ) -> "KeyRotationEvent":
        from .._ops import create_record

        return await create_record(
            cls,
            db,
            {
                "tenant_id": tenant_id,
                "actor_user_id": actor_user_id,
                "actor_client_id": actor_client_id,
                "key_kid": key_kid,
                "algorithm": algorithm,
                "action": action,
                "status": status,
                "details": details,
            },
        )


__all__ = ["KeyRotationEvent"]
