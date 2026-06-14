"""Canonical persisted DelegationGrant lifecycle tables."""

from __future__ import annotations

import datetime as dt
import uuid

from tigrbl_identity_server.framework import (
    Base,
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


class DelegationGrantRecord(Base, GUIDPk, Timestamped):
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


class DelegationGrantScope(Base, GUIDPk, Timestamped):
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


class DelegationGrantProof(Base, GUIDPk, Timestamped):
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


class DelegationGrantEdge(Base, GUIDPk, Timestamped):
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


class DelegationGrantTokenLink(Base, GUIDPk, Timestamped):
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


__all__ = [
    "DelegationGrantEdge",
    "DelegationGrantProof",
    "DelegationGrantRecord",
    "DelegationGrantScope",
    "DelegationGrantTokenLink",
]
