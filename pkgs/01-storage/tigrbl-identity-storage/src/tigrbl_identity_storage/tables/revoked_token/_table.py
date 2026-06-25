"""Durable revoked token registry."""

from __future__ import annotations

import datetime as dt
import uuid
from typing import Any

from tigrbl_identity_storage.framework import (
    RestOltpTable,
    BaseModel,
    Timestamped,
    S,
    acol,
    Mapped,
    String,
    GUIDPk,
    TZDateTime,
    PgUUID,
    ForeignKeySpec,
    op_ctx,
)


class RevocationIn(BaseModel):
    token: str
    token_type_hint: str | None = None


class RevocationOut(BaseModel):
    revoked: bool = True


class RevokedToken(RestOltpTable, GUIDPk, Timestamped):
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


def _items(result: Any) -> list[Any]:
    if isinstance(result, dict) and isinstance(result.get("items"), list):
        return result["items"]
    if isinstance(result, list):
        return result
    if isinstance(result, tuple):
        return list(result)
    return [] if result is None else [result]


def _created(result: Any) -> Any:
    if isinstance(result, dict):
        for key in ("item", "result", "data"):
            if key in result:
                return result[key]
    return result


def _field(row: Any, key: str, default: Any = None) -> Any:
    if row is None:
        return default
    if isinstance(row, dict):
        return row.get(key, default)
    return getattr(row, key, default)


@op_ctx(bind=RevokedToken, alias="record_hash", target="custom", arity="collection", rest=False)
async def record_hash(cls: type[RevokedToken], ctx: dict[str, Any]) -> RevokedToken:
    payload = dict(ctx.get("payload") or {})
    digest = payload["token_hash"]
    rows = _items(await cls.handlers.list.core({"payload": {"filters": {"token_hash": digest}}, "db": ctx["db"]}))
    row = rows[0] if rows else None
    record_payload = {
        "token_hash": digest,
        "token_type_hint": payload.get("token_type_hint") or _field(row, "token_type_hint"),
        "refresh_family_id": payload.get("refresh_family_id") or _field(row, "refresh_family_id"),
        "subject": payload.get("subject") or _field(row, "subject"),
        "tenant_id": payload.get("tenant_id") or _field(row, "tenant_id"),
        "client_id": payload.get("client_id") or _field(row, "client_id"),
        "revoked_reason": payload.get("reason") or payload.get("revoked_reason") or _field(row, "revoked_reason") or "revoked",
        "expires_at": payload.get("expires_at") or _field(row, "expires_at"),
    }
    if row is None:
        return _created(await cls.handlers.create.core({"payload": record_payload, "db": ctx["db"]}))
    return _created(
        await cls.handlers.update.core({"path_params": {"id": _field(row, "id")}, "payload": record_payload, "db": ctx["db"]})
    )


@op_ctx(bind=RevokedToken, alias="is_hash_revoked", target="custom", arity="collection", rest=False)
async def is_hash_revoked(cls: type[RevokedToken], ctx: dict[str, Any]) -> bool:
    payload = dict(ctx.get("payload") or {})
    rows = _items(await cls.handlers.list.core({"payload": {"filters": {"token_hash": payload["token_hash"]}}, "db": ctx["db"]}))
    return bool(rows)


__all__ = ["RevocationIn", "RevocationOut", "RevokedToken"]
