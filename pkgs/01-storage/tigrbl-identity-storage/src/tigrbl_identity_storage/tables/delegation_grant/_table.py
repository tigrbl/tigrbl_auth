"""Canonical persisted DelegationGrant lifecycle tables."""

from __future__ import annotations

import datetime as dt
import uuid
from typing import Any

from tigrbl_identity_storage.framework import (
    RestOltpTable,
    Boolean,
    ForeignKeySpec,
    GUIDPk,
    JSON,
    Mapped,
    PgUUID,
    S,
    String,
    TZDateTime,
    Timestamped,
    acol,
    op_ctx,
)


TERMINAL_GRANT_STATUSES = {"revoked", "expired", "replaced"}


class DelegationGrant(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "delegation_grants"
    __table_args__ = ({"schema": "authn"},)

    tenant_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.tenants.id"), nullable=True, index=True)
    )
    realm: Mapped[str] = acol(storage=S(String(120), nullable=False, default=""))
    delegator_subject: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    delegate_subject: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    delegate_type: Mapped[str] = acol(storage=S(String(64), nullable=False, default="subject"))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, index=True, default="draft"))
    parent_grant_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.delegation_grants.id"), nullable=True, index=True)
    )
    source_authority_ref: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    policy_version: Mapped[str | None] = acol(storage=S(String(128), nullable=True))
    provenance_id: Mapped[str | None] = acol(storage=S(String(128), nullable=True, index=True))
    constraints: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    effective_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    expires_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    revoked_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    revoked_by: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    revoked_reason: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    replaced_by_grant_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.delegation_grants.id"), nullable=True)
    )


class DelegationGrantScope(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "delegation_grant_scopes"
    __table_args__ = ({"schema": "authn"},)

    grant_id: Mapped[uuid.UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.delegation_grants.id"), nullable=False, index=True)
    )
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    realm: Mapped[str] = acol(storage=S(String(120), nullable=False, default=""))
    resource_type: Mapped[str | None] = acol(storage=S(String(120), nullable=True))
    resource_id: Mapped[str] = acol(storage=S(String(255), nullable=False, default="*"))
    action: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    scope: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    audience: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    resource_indicator: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    constraints: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


class DelegationGrantProof(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "delegation_grant_proofs"
    __table_args__ = ({"schema": "authn"},)

    grant_id: Mapped[uuid.UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.delegation_grants.id"), nullable=False, index=True)
    )
    source_scope_hash: Mapped[str] = acol(storage=S(String(128), nullable=False))
    delegated_scope_hash: Mapped[str] = acol(storage=S(String(128), nullable=False))
    attenuation_result: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=False))
    uncovered_scopes: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    proof_version: Mapped[str] = acol(storage=S(String(32), nullable=False, default="v1"))
    proof_hash: Mapped[str] = acol(storage=S(String(128), nullable=False, unique=True, index=True))
    evaluated_at: Mapped[dt.datetime] = acol(
        storage=S(TZDateTime, nullable=False, default=lambda: dt.datetime.now(dt.timezone.utc))
    )


class DelegationGrantEdge(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "delegation_grant_edges"
    __table_args__ = ({"schema": "authn"},)

    parent_grant_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.delegation_grants.id"), nullable=True, index=True)
    )
    child_grant_id: Mapped[uuid.UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.delegation_grants.id"), nullable=False, index=True)
    )
    delegator_subject: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    delegate_subject: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    edge_type: Mapped[str] = acol(storage=S(String(64), nullable=False, default="grant"))
    provenance_id: Mapped[str | None] = acol(storage=S(String(128), nullable=True))
    active: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=True))


class DelegationGrantTokenLink(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "delegation_grant_token_links"
    __table_args__ = ({"schema": "authn"},)

    grant_id: Mapped[uuid.UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.delegation_grants.id"), nullable=False, index=True)
    )
    token_hash: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    token_kind: Mapped[str] = acol(storage=S(String(32), nullable=False, default="access"))
    authorization_trace_id: Mapped[str | None] = acol(storage=S(String(128), nullable=True, index=True))
    delegation_provenance_id: Mapped[str | None] = acol(storage=S(String(128), nullable=True, index=True))
    actor_subject: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    subject: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    exchange_mode: Mapped[str] = acol(storage=S(String(32), nullable=False, default="delegation"))
    source_token_hash: Mapped[str | None] = acol(storage=S(String(128), nullable=True))
    actor_token_hash: Mapped[str | None] = acol(storage=S(String(128), nullable=True))


def _items(value: Any) -> list[Any]:
    return list(value.get("items") or ()) if isinstance(value, dict) else list(value or ())


def _field(row: Any, name: str, default: Any = None) -> Any:
    return row.get(name, default) if isinstance(row, dict) else getattr(row, name, default)


def _record_id(row: Any) -> Any:
    return _field(row, "id")


async def _create(model, db, payload):
    value = await model.handlers.create.core({"payload": dict(payload), "db": db})
    if isinstance(value, dict):
        return value.get("item", value.get("result", value))
    return value


async def _list(model, db, filters=None):
    normalized = dict(filters or {})
    value = await model.handlers.list.core({"payload": {"filters": normalized}, "db": db})
    rows = _items(value)
    return [row for row in rows if all(_field(row, key) == expected for key, expected in normalized.items())]


async def _read(model, db, identifier):
    return await model.handlers.read.core({"path_params": {"id": identifier}, "db": db})


async def _update(model, db, identifier, payload):
    return await model.handlers.update.core(
        {"path_params": {"id": identifier}, "payload": dict(payload), "db": db}
    )


async def _create_grant(cls, db, payload):
    values = dict(payload)
    values.setdefault("status", "active")
    values.setdefault("effective_at", dt.datetime.now(dt.timezone.utc))
    return await _create(cls, db, values)


@op_ctx(bind=DelegationGrant, alias="create_grant", target="custom", arity="collection", rest=False)
async def create_grant(cls, ctx):
    return await _create_grant(cls, ctx["db"], ctx.get("payload") or {})


@op_ctx(bind=DelegationGrant, alias="inspect_grant", target="custom", arity="collection", rest=False)
async def inspect_grant(cls, ctx):
    return await _read(cls, ctx["db"], (ctx.get("payload") or {})["grant_id"])


@op_ctx(bind=DelegationGrant, alias="list_grants", target="custom", arity="collection", rest=False)
async def list_grants(cls, ctx):
    filters = {key: value for key, value in dict(ctx.get("payload") or {}).items() if value is not None}
    return await _list(cls, ctx["db"], filters)


async def _transition(cls, ctx, status, timestamp_field):
    values = dict(ctx.get("payload") or {})
    row = await _read(cls, ctx["db"], values["grant_id"])
    if row is None:
        return None
    return await _update(
        cls, ctx["db"], _record_id(row),
        {"status": status, timestamp_field: values.get(timestamp_field) or dt.datetime.now(dt.timezone.utc)},
    )


@op_ctx(bind=DelegationGrant, alias="activate_grant", target="custom", arity="collection", rest=False)
async def activate_grant(cls, ctx):
    return await _transition(cls, ctx, "active", "effective_at")


@op_ctx(bind=DelegationGrant, alias="expire_grant", target="custom", arity="collection", rest=False)
async def expire_grant(cls, ctx):
    return await _transition(cls, ctx, "expired", "expires_at")


@op_ctx(bind=DelegationGrant, alias="replace_grant", target="custom", arity="collection", rest=False)
async def replace_grant(cls, ctx):
    values = dict(ctx.get("payload") or {})
    current = await _read(cls, ctx["db"], values.pop("grant_id"))
    if current is None:
        return None
    replacement = await _create_grant(
        cls, ctx["db"],
        {"tenant_id": _field(current, "tenant_id"), "realm": _field(current, "realm", ""),
         "delegator_subject": _field(current, "delegator_subject"),
         "delegate_subject": _field(current, "delegate_subject"),
         "delegate_type": _field(current, "delegate_type", "subject"),
         "parent_grant_id": _record_id(current), "source_authority_ref": _field(current, "source_authority_ref"),
         "policy_version": _field(current, "policy_version"), "provenance_id": _field(current, "provenance_id"),
         "constraints": _field(current, "constraints"), "expires_at": _field(current, "expires_at"), **values},
    )
    await _update(cls, ctx["db"], _record_id(current), {
        "status": "replaced", "revoked_at": dt.datetime.now(dt.timezone.utc),
        "revoked_reason": "replaced", "replaced_by_grant_id": _record_id(replacement),
    })
    return replacement


@op_ctx(bind=DelegationGrantEdge, alias="link_edge", target="custom", arity="collection", rest=False)
async def link_edge(cls, ctx):
    return await _create(cls, ctx["db"], {"active": True, **dict(ctx.get("payload") or {})})


@op_ctx(bind=DelegationGrantEdge, alias="deactivate_children", target="custom", arity="collection", rest=False)
async def deactivate_children(cls, ctx):
    parent = (ctx.get("payload") or {})["parent_grant_id"]
    return [await _update(cls, ctx["db"], _record_id(row), {"active": False}) for row in await _list(cls, ctx["db"], {"parent_grant_id": parent})]


@op_ctx(bind=DelegationGrant, alias="revoke_grant", target="custom", arity="collection", rest=False)
async def revoke_grant(cls, ctx):
    values = dict(ctx.get("payload") or {})
    row = await _read(cls, ctx["db"], values["grant_id"])
    if row is None:
        return None
    revoked = await _update(cls, ctx["db"], _record_id(row), {
        "status": "revoked", "revoked_at": dt.datetime.now(dt.timezone.utc),
        "revoked_by": values.get("revoked_by"), "revoked_reason": values.get("reason"),
    })
    if values.get("collapse_descendants"):
        children = await _list(cls, ctx["db"], {"parent_grant_id": _record_id(row)})
        for child in children:
            if _field(child, "status") not in TERMINAL_GRANT_STATUSES:
                await cls.revoke_grant({"payload": {"grant_id": _record_id(child), "revoked_by": values.get("revoked_by"), "reason": "ancestor-revoked", "collapse_descendants": True}, "db": ctx["db"]})
        await DelegationGrantEdge.deactivate_children(
            {"payload": {"parent_grant_id": _record_id(row)}, "db": ctx["db"]}
        )
    return revoked


@op_ctx(bind=DelegationGrantProof, alias="persist_provenance", target="custom", arity="collection", rest=False)
async def persist_provenance(cls, ctx):
    return await _create(cls, ctx["db"], ctx.get("payload") or {})


@op_ctx(bind=DelegationGrantTokenLink, alias="link_token", target="custom", arity="collection", rest=False)
async def link_token(cls, ctx):
    return await _create(cls, ctx["db"], ctx.get("payload") or {})


@op_ctx(bind=DelegationGrantTokenLink, alias="list_for_grant", target="custom", arity="collection", rest=False)
async def list_for_grant(cls, ctx):
    return await _list(cls, ctx["db"], {"grant_id": (ctx.get("payload") or {})["grant_id"]})


DelegationGrantRecord = DelegationGrant


__all__ = [
    "DelegationGrant",
    "DelegationGrantEdge",
    "DelegationGrantProof",
    "DelegationGrantRecord",
    "DelegationGrantScope",
    "DelegationGrantTokenLink",
]
