"""Durable consent records for scopes and claims grants."""

from __future__ import annotations

import datetime as dt
from typing import Any
import uuid

from tigrbl_identity_storage.framework import (
    ForeignKeySpec,
    GUIDPk,
    JSON,
    Mapped,
    PgUUID,
    RestOltpTable,
    S,
    String,
    TZDateTime,
    TenantColumn,
    Timestamped,
    UUID,
    UserColumn,
    acol,
    op_ctx,
)


class Consent(RestOltpTable, GUIDPk, Timestamped, UserColumn, TenantColumn):
    __tablename__ = "consents"
    __table_args__ = ({"schema": "authn"},)

    client_id: Mapped[UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=False, index=True)
    )
    scope: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    claims: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    state: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active"))
    granted_at: Mapped[dt.datetime] = acol(
        storage=S(TZDateTime, nullable=False, default=lambda: dt.datetime.now(dt.timezone.utc))
    )
    expires_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    revoked_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))


def _payload(ctx: dict[str, Any]) -> dict[str, Any]:
    value = ctx.get("payload") or {}
    return dict(value) if isinstance(value, dict) else {}


def _path_params(ctx: dict[str, Any]) -> dict[str, Any]:
    value = ctx.get("path_params") or {}
    return dict(value) if isinstance(value, dict) else {}


def _db(ctx: dict[str, Any]) -> Any:
    return ctx.get("db") or ctx.get("session")


def _items(result: Any) -> list[Any]:
    if isinstance(result, dict) and isinstance(result.get("items"), list):
        return result["items"]
    if isinstance(result, list):
        return result
    if isinstance(result, tuple):
        return list(result)
    return [] if result is None else [result]


def _to_uuid(value: Any) -> uuid.UUID | None:
    if value in {None, ""}:
        return None
    if isinstance(value, uuid.UUID):
        return value
    try:
        return uuid.UUID(str(value))
    except (TypeError, ValueError):
        return None


def _utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _principal_filters(ctx: dict[str, Any]) -> dict[str, Any]:
    payload = _payload(ctx)
    filters: dict[str, Any] = {}
    user_id = _to_uuid(payload.get("user_id"))
    tenant_id = _to_uuid(payload.get("tenant_id"))
    if user_id is not None:
        filters["user_id"] = user_id
    if tenant_id is not None:
        filters["tenant_id"] = tenant_id
    return filters


def _list_response_schema(table: type) -> type:
    return table.schemas.list.out


def _update_response_schema(table: type) -> type:
    return table.schemas.update.out


@op_ctx(
    bind=Consent,
    alias="list_for_user",
    target="custom",
    arity="collection",
    rest=False,
    response_schema=_list_response_schema,
)
async def list_for_user(cls: type[Consent], ctx: dict[str, Any]) -> list[Consent]:
    return _items(
        await cls.handlers.list.core(
            {"payload": {"filters": _principal_filters(ctx)}, "db": _db(ctx)}
        )
    )


@op_ctx(
    bind=Consent,
    alias="revoke_for_user",
    target="custom",
    arity="member",
    rest=False,
    response_schema=_update_response_schema,
)
async def revoke_for_user(cls: type[Consent], ctx: dict[str, Any]) -> Consent | None:
    filters = _principal_filters(ctx)
    consent_id = _to_uuid(_path_params(ctx).get("id") or _path_params(ctx).get("consent_id") or _payload(ctx).get("id"))
    if consent_id is None:
        return None
    filters["id"] = consent_id
    rows = _items(
        await cls.handlers.list.core(
            {"payload": {"filters": filters}, "db": _db(ctx)}
        )
    )
    if not rows:
        return None
    row = rows[0]
    return await cls.handlers.update.core(
        {
            "path_params": {"id": row.id},
            "payload": {"state": "revoked", "revoked_at": row.revoked_at or _utc_now()},
            "db": _db(ctx),
        }
    )


@op_ctx(
    bind=Consent,
    alias="revoke_for_client",
    target="custom",
    arity="collection",
    rest=False,
    response_schema=_update_response_schema,
)
async def revoke_for_client(cls: type[Consent], ctx: dict[str, Any]) -> list[Consent]:
    filters = _principal_filters(ctx)
    client_id = _to_uuid(
        _path_params(ctx).get("client_id")
        or _path_params(ctx).get("id")
        or _payload(ctx).get("client_id")
    )
    if client_id is None:
        return []
    filters["client_id"] = client_id
    rows = _items(
        await cls.handlers.list.core(
            {"payload": {"filters": filters}, "db": _db(ctx)}
        )
    )
    now = _utc_now()
    updated: list[Consent] = []
    for row in rows:
        updated.append(
            await cls.handlers.update.core(
                {
                    "path_params": {"id": row.id},
                    "payload": {"state": "revoked", "revoked_at": row.revoked_at or now},
                    "db": _db(ctx),
                }
            )
        )
    return updated


__all__ = [
    "Consent",
]
