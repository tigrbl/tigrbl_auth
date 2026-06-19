"""Durable revoked token registry."""

from __future__ import annotations

import datetime as dt
import uuid
from typing import Any

from tigrbl_identity_server.framework import (
    Base,
    TigrblRouter,
    Timestamped,
    S,
    acol,
    Mapped,
    String,
    GUIDPk,
    TZDateTime,
    PgUUID,
    ForeignKeySpec,
)
from tigrbl_identity_contracts.rest import RevocationOut
from ._ops import create_record, first_record, record_id, update_record


class RevokedToken(Base, GUIDPk, Timestamped):
    __tablename__ = "revoked_tokens"
    __table_args__ = ({"schema": "authn"},)

    token_hash: Mapped[str] = acol(storage=S(String(128), nullable=False, unique=True, index=True, default=lambda: uuid.uuid4().hex))
    token_type_hint: Mapped[str | None] = acol(storage=S(String(64), nullable=True))
    subject: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    tenant_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.tenants.id"), nullable=True, index=True)
    )
    client_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=True, index=True)
    )
    revoked_reason: Mapped[str | None] = acol(storage=S(String(128), nullable=True))
    expires_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))

    @classmethod
    async def revoke_token(
        cls,
        db: Any,
        *,
        token_hash: str,
        token_type_hint: str | None = None,
        reason: str | None = None,
        **metadata: Any,
    ) -> "RevokedToken":
        existing = await first_record(cls, db, {"token_hash": token_hash})
        payload = {"token_hash": token_hash, "token_type_hint": token_type_hint, "revoked_reason": reason or "revoked"}
        payload.update(metadata)
        if existing is None:
            return await create_record(cls, db, payload)
        return await update_record(cls, db, record_id(existing), payload)

    @classmethod
    async def is_revoked(cls, db: Any, *, token_hash: str) -> bool:
        return await first_record(cls, db, {"token_hash": token_hash}) is not None


api = router = TigrblRouter()


@api.route("/revoke", methods=["POST"], response_model=RevocationOut)
async def revoke(request: Any) -> Any:
    from tigrbl_auth_protocol_oauth.ops.revoke import revoke_request

    return await revoke_request(request=request)


RevokedToken.revoke = staticmethod(revoke)  # type: ignore[attr-defined]


__all__ = ["RevokedToken", "api", "router", "revoke"]
