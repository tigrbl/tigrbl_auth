"""Durable verifier, presentation transaction, consent, and replay metadata."""

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


class VerifierRegistration(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "verifier_registrations"
    __table_args__ = ({"schema": "authn"},)
    verifier_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    client_id: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    client_id_scheme: Mapped[str] = acol(
        storage=S(String(64), nullable=False, index=True)
    )
    metadata_document: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    status: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="active", index=True)
    )


class PresentationTransaction(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "presentation_transactions"
    __table_args__ = ({"schema": "authn"},)
    transaction_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    verifier_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    wallet_instance_id: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    request_digest: Mapped[str] = acol(
        storage=S(String(128), nullable=False, index=True)
    )
    nonce_digest: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    response_digest: Mapped[str | None] = acol(
        storage=S(String(128), nullable=True, index=True)
    )
    status: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="pending", index=True)
    )
    expires_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


class PresentationConsent(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "presentation_consents"
    __table_args__ = ({"schema": "authn"},)
    transaction_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    subject_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    selection_digest: Mapped[str] = acol(
        storage=S(String(128), nullable=False, index=True)
    )
    granted: Mapped[bool] = acol(storage=S(Boolean, nullable=False, index=True))
    decided_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


class PresentationReplay(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "presentation_replays"
    __table_args__ = ({"schema": "authn"},)
    replay_key_digest: Mapped[str] = acol(
        storage=S(String(128), nullable=False, unique=True, index=True)
    )
    transaction_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, index=True)
    )
    expires_at: Mapped[dt.datetime] = acol(
        storage=S(TZDateTime, nullable=False, index=True)
    )
    consumed_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


__all__ = [
    "VerifierRegistration",
    "PresentationTransaction",
    "PresentationConsent",
    "PresentationReplay",
]
