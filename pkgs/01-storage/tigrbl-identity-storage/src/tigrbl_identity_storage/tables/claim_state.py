"""Durable tenant-defined claim metadata, policy, and provenance.

Standard claim semantics remain code-owned. These tables exist for private
claim registration, source binding, release policy, and protected snapshots.
"""

from __future__ import annotations

import datetime as dt

from tigrbl_identity_storage.framework import (
    Boolean,
    GUIDPk,
    JSON,
    Mapped,
    RestOltpTable,
    S,
    String,
    TZDateTime,
    TenantColumn,
    Timestamped,
    acol,
)


class ClaimDefinition(RestOltpTable, GUIDPk, Timestamped, TenantColumn):
    __tablename__ = "claim_definitions"
    __table_args__ = ({"schema": "authn"},)

    label: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    label_kind: Mapped[str] = acol(storage=S(String(32), nullable=False, index=True))
    namespace: Mapped[str | None] = acol(storage=S(String(1000), nullable=True, index=True))
    registry: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    semantic_type: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    value_type: Mapped[str] = acol(storage=S(String(64), nullable=False))
    standards: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    active: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=True, index=True))


class ClaimSourceBinding(RestOltpTable, GUIDPk, Timestamped, TenantColumn):
    __tablename__ = "claim_source_bindings"
    __table_args__ = ({"schema": "authn"},)

    claim_definition_id: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    source_kind: Mapped[str] = acol(storage=S(String(32), nullable=False, index=True))
    provider_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    source_path: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    transformation: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    active: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=True, index=True))


class ClaimReleasePolicy(RestOltpTable, GUIDPk, Timestamped, TenantColumn):
    __tablename__ = "claim_release_policies"
    __table_args__ = ({"schema": "authn"},)

    claim_definition_id: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    audience_pattern: Mapped[str | None] = acol(storage=S(String(1000), nullable=True, index=True))
    protocol_tag: Mapped[str | None] = acol(storage=S(String(64), nullable=True, index=True))
    disclosure_mode: Mapped[str] = acol(storage=S(String(32), nullable=False, index=True))
    purpose: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    conditions: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    active: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=True, index=True))


class ClaimProvenanceRecord(RestOltpTable, GUIDPk, Timestamped, TenantColumn):
    __tablename__ = "claim_provenance_records"
    __table_args__ = ({"schema": "authn"},)

    claim_label: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    namespace: Mapped[str | None] = acol(storage=S(String(1000), nullable=True, index=True))
    subject_reference: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    source_kind: Mapped[str] = acol(storage=S(String(32), nullable=False, index=True))
    source_reference: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    evidence_reference: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    value_digest: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    verified_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    assurance_framework: Mapped[str | None] = acol(storage=S(String(255), nullable=True))


class ClaimSnapshot(RestOltpTable, GUIDPk, Timestamped, TenantColumn):
    __tablename__ = "claim_snapshots"
    __table_args__ = ({"schema": "authn"},)

    claim_set_reference: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    protocol_tag: Mapped[str | None] = acol(storage=S(String(64), nullable=True, index=True))
    specification_version: Mapped[str | None] = acol(storage=S(String(128), nullable=True))
    payload_digest: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    protected_artifact_locator: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    retention_expires_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))


__all__ = [
    "ClaimDefinition",
    "ClaimProvenanceRecord",
    "ClaimReleasePolicy",
    "ClaimSnapshot",
    "ClaimSourceBinding",
]
