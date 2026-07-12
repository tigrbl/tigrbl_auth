"""Durable credential issuer, configuration, and wallet registry state."""

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


class CredentialIssuer(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "credential_issuers"
    __table_args__ = ({"schema": "authn"},)
    issuer: Mapped[str] = acol(
        storage=S(String(1000), nullable=False, unique=True, index=True)
    )
    status: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="active", index=True)
    )
    metadata_document: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


class CredentialConfiguration(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "credential_configurations"
    __table_args__ = ({"schema": "authn"},)
    issuer_id: Mapped[str] = acol(storage=S(String(36), nullable=False, index=True))
    configuration_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, index=True)
    )
    format: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    credential_type: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    configuration: Mapped[dict] = acol(storage=S(JSON, nullable=False))
    enabled: Mapped[bool] = acol(
        storage=S(Boolean, nullable=False, default=True, index=True)
    )


class WalletRegistration(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "wallet_registrations"
    __table_args__ = ({"schema": "authn"},)
    wallet_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    subject_id: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    status: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="active", index=True)
    )
    wallet_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


class WalletInstance(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "wallet_instances"
    __table_args__ = ({"schema": "authn"},)
    wallet_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    instance_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    key_reference: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    status: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="active", index=True)
    )


class WalletAttestation(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "wallet_attestations"
    __table_args__ = ({"schema": "authn"},)
    wallet_instance_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, index=True)
    )
    profile: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    evidence_digest: Mapped[str] = acol(
        storage=S(String(128), nullable=False, index=True)
    )
    verification_result: Mapped[str] = acol(
        storage=S(String(64), nullable=False, index=True)
    )
    valid_until: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


class WalletKeyBinding(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "wallet_key_bindings"
    __table_args__ = ({"schema": "authn"},)
    wallet_instance_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, index=True)
    )
    key_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    binding_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    valid_from: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    valid_until: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


__all__ = [
    "CredentialIssuer",
    "CredentialConfiguration",
    "WalletRegistration",
    "WalletInstance",
    "WalletAttestation",
    "WalletKeyBinding",
]
