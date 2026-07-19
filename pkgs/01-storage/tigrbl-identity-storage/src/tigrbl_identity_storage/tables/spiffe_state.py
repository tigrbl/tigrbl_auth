"""Durable SPIFFE SVID, trust-bundle, and federation metadata."""

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


class SvidRecord(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "svid_records"
    __table_args__ = ({"schema": "authn"},)
    spiffe_id: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    svid_type: Mapped[str] = acol(storage=S(String(32), nullable=False, index=True))
    serial_or_jti: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    key_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    proof_key_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    confirmation_key_thumbprint: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    profile_revision: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    bundle_version: Mapped[str | None] = acol(
        storage=S(String(128), nullable=True, index=True)
    )
    artifact_locator: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    artifact_digest: Mapped[str] = acol(
        storage=S(String(128), nullable=False, index=True)
    )
    valid_from: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    valid_until: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    revoked: Mapped[bool] = acol(
        storage=S(Boolean, nullable=False, default=False, index=True)
    )


class SpiffeTrustBundle(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "spiffe_trust_bundles"
    __table_args__ = ({"schema": "authn"},)
    trust_domain: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    version: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    artifact_locator: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    artifact_digest: Mapped[str] = acol(
        storage=S(String(128), nullable=False, index=True)
    )
    valid_until: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    active: Mapped[bool] = acol(
        storage=S(Boolean, nullable=False, default=True, index=True)
    )


class TrustDomainFederation(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "trust_domain_federations"
    __table_args__ = ({"schema": "authn"},)
    local_trust_domain: Mapped[str] = acol(
        storage=S(String(255), nullable=False, index=True)
    )
    remote_trust_domain: Mapped[str] = acol(
        storage=S(String(255), nullable=False, index=True)
    )
    bundle_endpoint: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    profile: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    status: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="active", index=True)
    )
    federation_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


__all__ = ["SvidRecord", "SpiffeTrustBundle", "TrustDomainFederation"]
