"""Durable revoked token registry."""

from __future__ import annotations

import datetime as dt
import uuid
from typing import Any

from tigrbl_identity_storage.framework import (
    Base,
    BaseModel,
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
from .._ops import create_record, first_record, record_id, update_record


class RevocationIn(BaseModel):
    token: str
    token_type_hint: str | None = None


class RevocationOut(BaseModel):
    revoked: bool = True


class RevokedToken(Base, GUIDPk, Timestamped):
    __tablename__ = "revoked_tokens"
    __table_args__ = ({"schema": "authn"},)

    token_hash: Mapped[str] = acol(storage=S(String(128), nullable=False, unique=True, index=True, default=lambda: uuid.uuid4().hex))
    token_type_hint: Mapped[str | None] = acol(storage=S(String(64), nullable=True))
    refresh_family_id: Mapped[str | None] = acol(storage=S(String(64), nullable=True, index=True))
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
        refresh_family_id: str | None = None,
        **metadata: Any,
    ) -> "RevokedToken":
        existing = await first_record(cls, db, {"token_hash": token_hash})
        payload = {
            "token_hash": token_hash,
            "token_type_hint": token_type_hint,
            "refresh_family_id": refresh_family_id,
            "revoked_reason": reason or "revoked",
        }
        payload.update(metadata)
        if existing is None:
            return await create_record(cls, db, payload)
        return await update_record(cls, db, record_id(existing), payload)

    @classmethod
    async def is_revoked(cls, db: Any, *, token_hash: str) -> bool:
        return await first_record(cls, db, {"token_hash": token_hash}) is not None

    @classmethod
    async def revoke_family(
        cls,
        db: Any,
        *,
        refresh_family_id: str,
        token_hashes: list[str],
        reason: str = "refresh_token_family_revoked",
        **metadata: Any,
    ) -> list["RevokedToken"]:
        revoked = []
        token_type_hint = metadata.pop("token_type_hint", None)
        for token_hash in token_hashes:
            revoked.append(
                await cls.revoke_token(
                    db,
                    token_hash=token_hash,
                    token_type_hint=token_type_hint,
                    reason=reason,
                    refresh_family_id=refresh_family_id,
                    **metadata,
                )
            )
        return revoked


api = router = TigrblRouter()


@api.route("/revoke", methods=["POST"], response_model=RevocationOut)
async def revoke(request: Any) -> Any:
    from ._route import revoke_request

    return await revoke_request(request=request)


RevokedToken.revoke = staticmethod(revoke)  # type: ignore[attr-defined]


__all__ = ["RevocationIn", "RevocationOut", "RevokedToken", "api", "router", "revoke"]
