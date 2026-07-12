"""Durable credential offer, issuance, notification, and status state."""

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


class CredentialOffer(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "credential_offers"
    __table_args__ = ({"schema": "authn"},)
    offer_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    issuer_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    configuration_ids: Mapped[list] = acol(storage=S(JSON, nullable=False))
    grant_types: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    expires_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    consumed_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


class CredentialIssuanceTransaction(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "credential_issuance_transactions"
    __table_args__ = ({"schema": "authn"},)
    transaction_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    issuer_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    subject_id: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    wallet_instance_id: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    configuration_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, index=True)
    )
    status: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="pending", index=True)
    )
    request_digest: Mapped[str | None] = acol(
        storage=S(String(128), nullable=True, index=True)
    )
    result_reference: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    expires_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


class CredentialDeferredTransaction(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "credential_deferred_transactions"
    __table_args__ = ({"schema": "authn"},)
    transaction_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    issuance_transaction_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, index=True)
    )
    status: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="pending", index=True)
    )
    interval_seconds: Mapped[str | None] = acol(storage=S(String(16), nullable=True))
    expires_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


class CredentialNotification(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "credential_notifications"
    __table_args__ = ({"schema": "authn"},)
    notification_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    issuance_transaction_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, index=True)
    )
    event: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    description: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    acknowledged: Mapped[bool] = acol(
        storage=S(Boolean, nullable=False, default=False, index=True)
    )


class CredentialStatusList(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "credential_status_lists"
    __table_args__ = ({"schema": "authn"},)
    status_list_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    issuer_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    purpose: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    size: Mapped[str] = acol(storage=S(String(32), nullable=False))
    current_version: Mapped[str] = acol(
        storage=S(String(64), nullable=False, default="1", index=True)
    )


class CredentialStatusEntry(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "credential_status_entries"
    __table_args__ = ({"schema": "authn"},)
    status_list_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, index=True)
    )
    credential_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    status_index: Mapped[str] = acol(storage=S(String(32), nullable=False, index=True))
    status: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="valid", index=True)
    )
    changed_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


class CredentialStatusPublication(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "credential_status_publications"
    __table_args__ = ({"schema": "authn"},)
    status_list_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, index=True)
    )
    version: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    artifact_locator: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    artifact_digest: Mapped[str] = acol(
        storage=S(String(128), nullable=False, index=True)
    )
    published_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


__all__ = [
    "CredentialOffer",
    "CredentialIssuanceTransaction",
    "CredentialDeferredTransaction",
    "CredentialNotification",
    "CredentialStatusList",
    "CredentialStatusEntry",
    "CredentialStatusPublication",
]
