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
)
from .._ops import create_record, field, first_record, list_records, record_id, update_record, utc_now


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

    @classmethod
    async def create_grant(cls, db: Any, **payload: Any) -> "DelegationGrant":
        payload.setdefault("status", "active")
        payload.setdefault("effective_at", utc_now())
        return await create_record(cls, db, payload)

    @classmethod
    async def inspect_grant(cls, db: Any, *, grant_id: uuid.UUID) -> "DelegationGrant | None":
        return await first_record(cls, db, {"id": grant_id})

    @classmethod
    async def activate_grant(
        cls,
        db: Any,
        *,
        grant_id: uuid.UUID,
        effective_at: dt.datetime | None = None,
    ) -> "DelegationGrant | None":
        row = await cls.inspect_grant(db, grant_id=grant_id)
        if row is None:
            return None
        return await update_record(
            cls,
            db,
            record_id(row),
            {"status": "active", "effective_at": effective_at or utc_now()},
        )

    @classmethod
    async def revoke_grant(
        cls,
        db: Any,
        *,
        grant_id: uuid.UUID,
        revoked_by: str | None = None,
        reason: str | None = None,
        collapse_descendants: bool = False,
    ) -> "DelegationGrant | None":
        row = await cls.inspect_grant(db, grant_id=grant_id)
        if row is None:
            return None
        revoked = await update_record(
            cls,
            db,
            record_id(row),
            {"status": "revoked", "revoked_at": utc_now(), "revoked_by": revoked_by, "revoked_reason": reason},
        )
        if collapse_descendants:
            children = await cls.list_grants(db, parent_grant_id=record_id(row))
            for child in children:
                if field(child, "status") not in TERMINAL_GRANT_STATUSES:
                    await cls.revoke_grant(
                        db,
                        grant_id=record_id(child),
                        revoked_by=revoked_by,
                        reason="ancestor-revoked",
                        collapse_descendants=True,
                    )
            await DelegationGrantEdge.deactivate_children(db, parent_grant_id=record_id(row))
        return revoked

    @classmethod
    async def expire_grant(
        cls,
        db: Any,
        *,
        grant_id: uuid.UUID,
        expires_at: dt.datetime | None = None,
    ) -> "DelegationGrant | None":
        row = await cls.inspect_grant(db, grant_id=grant_id)
        if row is None:
            return None
        return await update_record(
            cls,
            db,
            record_id(row),
            {"status": "expired", "expires_at": expires_at or utc_now()},
        )

    @classmethod
    async def replace_grant(
        cls,
        db: Any,
        *,
        grant_id: uuid.UUID,
        replaced_by: str | None = None,
        reason: str = "replaced",
        **payload: Any,
    ) -> "DelegationGrant | None":
        current = await cls.inspect_grant(db, grant_id=grant_id)
        if current is None:
            return None
        replacement_payload = {
            "tenant_id": field(current, "tenant_id"),
            "realm": field(current, "realm", ""),
            "delegator_subject": field(current, "delegator_subject"),
            "delegate_subject": field(current, "delegate_subject"),
            "delegate_type": field(current, "delegate_type", "subject"),
            "parent_grant_id": record_id(current),
            "source_authority_ref": field(current, "source_authority_ref"),
            "policy_version": field(current, "policy_version"),
            "provenance_id": field(current, "provenance_id"),
            "constraints": field(current, "constraints"),
            "expires_at": field(current, "expires_at"),
        }
        replacement_payload.update(payload)
        replacement = await cls.create_grant(db, **replacement_payload)
        await update_record(
            cls,
            db,
            record_id(current),
            {
                "status": "replaced",
                "revoked_at": utc_now(),
                "revoked_by": replaced_by,
                "revoked_reason": reason,
                "replaced_by_grant_id": record_id(replacement),
            },
        )
        return replacement

    @classmethod
    async def list_grants(
        cls,
        db: Any,
        *,
        tenant_id: uuid.UUID | None = None,
        delegator_subject: str | None = None,
        delegate_subject: str | None = None,
        parent_grant_id: uuid.UUID | None = None,
        status: str | None = None,
    ) -> list["DelegationGrant"]:
        filters = {
            key: value
            for key, value in {
                "tenant_id": tenant_id,
                "delegator_subject": delegator_subject,
                "delegate_subject": delegate_subject,
                "parent_grant_id": parent_grant_id,
                "status": status,
            }.items()
            if value is not None
        }
        return await list_records(cls, db, filters)


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

    @classmethod
    async def list_for_grant(cls, db: Any, *, grant_id: uuid.UUID) -> list["DelegationGrantScope"]:
        return await list_records(cls, db, {"grant_id": grant_id})


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

    @classmethod
    async def persist_provenance(cls, db: Any, **payload: Any) -> "DelegationGrantProof":
        payload.setdefault("evaluated_at", utc_now())
        return await create_record(cls, db, payload)


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

    @classmethod
    async def link_edge(cls, db: Any, **payload: Any) -> "DelegationGrantEdge":
        payload.setdefault("active", True)
        return await create_record(cls, db, payload)

    @classmethod
    async def list_children(cls, db: Any, *, parent_grant_id: uuid.UUID) -> list["DelegationGrantEdge"]:
        return await list_records(cls, db, {"parent_grant_id": parent_grant_id})

    @classmethod
    async def deactivate_children(cls, db: Any, *, parent_grant_id: uuid.UUID) -> list["DelegationGrantEdge"]:
        updated: list["DelegationGrantEdge"] = []
        for edge in await cls.list_children(db, parent_grant_id=parent_grant_id):
            updated.append(await update_record(cls, db, record_id(edge), {"active": False}))
        return updated


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

    @classmethod
    async def link_token(cls, db: Any, **payload: Any) -> "DelegationGrantTokenLink":
        return await create_record(cls, db, payload)

    @classmethod
    async def list_for_grant(cls, db: Any, *, grant_id: uuid.UUID) -> list["DelegationGrantTokenLink"]:
        return await list_records(cls, db, {"grant_id": grant_id})


DelegationGrantRecord = DelegationGrant


__all__ = [
    "DelegationGrant",
    "DelegationGrantEdge",
    "DelegationGrantProof",
    "DelegationGrantRecord",
    "DelegationGrantScope",
    "DelegationGrantTokenLink",
]
