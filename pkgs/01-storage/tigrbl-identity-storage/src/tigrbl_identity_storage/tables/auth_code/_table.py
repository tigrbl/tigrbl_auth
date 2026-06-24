"""Authorization code durable table."""

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

from .._ops import create_record


class AuthCode(RestOltpTable, GUIDPk, Timestamped, UserColumn, TenantColumn):
    __tablename__ = "auth_codes"
    __table_args__ = ({"schema": "authn"},)

    client_id: Mapped[UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=False)
    )
    session_id: Mapped[UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.sessions.id"), nullable=True, index=True)
    )
    redirect_uri: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    code_challenge: Mapped[str | None] = acol(storage=S(String, nullable=True))
    nonce: Mapped[str | None] = acol(storage=S(String, nullable=True))
    scope: Mapped[str | None] = acol(storage=S(String, nullable=True))
    expires_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False))
    claims: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


def _payload(ctx: dict[str, Any]) -> dict[str, Any]:
    value = ctx.get("payload") or ctx.get("p") or {}
    return dict(value) if isinstance(value, dict) else {}


def _db(ctx: dict[str, Any]) -> Any:
    return ctx.get("db") or ctx.get("session")


def _create_response_schema(table: type) -> type:
    return table.schemas.create.out


@op_ctx(
    bind=AuthCode,
    alias="authorize",
    target="custom",
    arity="collection",
    rest=False,
    response_schema=_create_response_schema,
)
async def authorize(cls: type[AuthCode], ctx: dict[str, Any]) -> AuthCode:
    return await create_record(cls, _db(ctx), _payload(ctx))


__all__ = ["AuthCode"]
