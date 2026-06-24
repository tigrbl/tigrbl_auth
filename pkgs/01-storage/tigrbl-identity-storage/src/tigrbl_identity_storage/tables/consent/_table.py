"""Durable consent records for scopes and claims grants."""

from __future__ import annotations

import datetime as dt
from typing import Any

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

from .._ops import list_records, to_uuid, update_record, utc_now


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


def _principal_filters(ctx: dict[str, Any]) -> dict[str, Any]:
    payload = _payload(ctx)
    filters: dict[str, Any] = {}
    user_id = to_uuid(payload.get("user_id"))
    tenant_id = to_uuid(payload.get("tenant_id"))
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
    return await list_records(cls, _db(ctx), _principal_filters(ctx))


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
    consent_id = to_uuid(_path_params(ctx).get("id") or _path_params(ctx).get("consent_id") or _payload(ctx).get("id"))
    if consent_id is None:
        return None
    filters["id"] = consent_id
    rows = await list_records(cls, _db(ctx), filters)
    if not rows:
        return None
    row = rows[0]
    return await update_record(
        cls,
        _db(ctx),
        row.id,
        {"state": "revoked", "revoked_at": row.revoked_at or utc_now()},
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
    client_id = to_uuid(
        _path_params(ctx).get("client_id")
        or _path_params(ctx).get("id")
        or _payload(ctx).get("client_id")
    )
    if client_id is None:
        return []
    filters["client_id"] = client_id
    rows = await list_records(cls, _db(ctx), filters)
    now = utc_now()
    updated: list[Consent] = []
    for row in rows:
        updated.append(
            await update_record(
                cls,
                _db(ctx),
                row.id,
                {"state": "revoked", "revoked_at": row.revoked_at or now},
            )
        )
    return updated


__all__ = [
    "Consent",
]
