"""Durable credential lifecycle records."""

from __future__ import annotations

import datetime as dt

from tigrbl_identity_storage.framework import (
    RestOltpTable,
    GUIDPk,
    Integer,
    JSON,
    Mapped,
    S,
    String,
    TZDateTime,
    Timestamped,
    acol,
)


class Credential(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "credentials"
    __table_args__ = ({"schema": "authn"},)

    principal_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    credential_kind: Mapped[str] = acol(
        storage=S(String(64), nullable=False, index=True)
    )
    format: Mapped[str | None] = acol(storage=S(String(64), nullable=True, index=True))
    credential_type: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    issuer_id: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    subject_id: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    holder_binding_kind: Mapped[str | None] = acol(
        storage=S(String(64), nullable=True, index=True)
    )
    status_reference: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    payload_digest: Mapped[str | None] = acol(
        storage=S(String(128), nullable=True, index=True)
    )
    issued_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    valid_from: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    valid_until: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    secret_digest: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    public_id: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    status: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="active", index=True)
    )
    version: Mapped[int] = acol(storage=S(Integer, nullable=False, default=1))
    rotated_from: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    expires_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    credential_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


__all__ = ["Credential"]
