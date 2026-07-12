"""Durable certificate metadata, trust anchors, and status snapshots."""

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
    Timestamped,
    acol,
)


class CertificateRecord(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "certificate_records"
    __table_args__ = ({"schema": "authn"},)
    certificate_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    profile: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    subject: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    issuer: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    serial_number: Mapped[str] = acol(
        storage=S(String(255), nullable=False, index=True)
    )
    thumbprint_sha256: Mapped[str] = acol(
        storage=S(String(128), nullable=False, unique=True, index=True)
    )
    artifact_locator: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    valid_from: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    valid_until: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    key_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))


class TrustAnchor(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "trust_anchors"
    __table_args__ = ({"schema": "authn"},)
    anchor_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    profile: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    subject: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    thumbprint_sha256: Mapped[str] = acol(
        storage=S(String(128), nullable=False, index=True)
    )
    artifact_locator: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    constraints: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    active: Mapped[bool] = acol(
        storage=S(Boolean, nullable=False, default=True, index=True)
    )


class CertificateStatusSnapshot(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "certificate_status_snapshots"
    __table_args__ = ({"schema": "authn"},)
    certificate_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, index=True)
    )
    source: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, index=True))
    this_update: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    next_update: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    response_digest: Mapped[str] = acol(
        storage=S(String(128), nullable=False, index=True)
    )
    artifact_locator: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))


__all__ = ["CertificateRecord", "TrustAnchor", "CertificateStatusSnapshot"]
