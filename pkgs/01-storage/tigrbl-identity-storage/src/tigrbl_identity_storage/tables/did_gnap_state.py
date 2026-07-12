"""Optional durable DID authority/cache and GNAP transaction state."""

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


class DidDocument(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "did_documents"
    __table_args__ = ({"schema": "authn"},)
    did: Mapped[str] = acol(
        storage=S(String(1000), nullable=False, unique=True, index=True)
    )
    method: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    authoritative: Mapped[bool] = acol(
        storage=S(Boolean, nullable=False, default=False, index=True)
    )
    current_version: Mapped[str | None] = acol(
        storage=S(String(128), nullable=True, index=True)
    )


class DidDocumentVersion(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "did_document_versions"
    __table_args__ = ({"schema": "authn"},)
    did: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    version: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    document: Mapped[dict] = acol(storage=S(JSON, nullable=False))
    document_digest: Mapped[str] = acol(
        storage=S(String(128), nullable=False, index=True)
    )
    valid_until: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


class DidVerificationMethod(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "did_verification_methods"
    __table_args__ = ({"schema": "authn"},)
    did: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    method_id: Mapped[str] = acol(
        storage=S(String(1000), nullable=False, unique=True, index=True)
    )
    method_type: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    controller: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    public_key: Mapped[dict] = acol(storage=S(JSON, nullable=False))
    relationships: Mapped[list | None] = acol(storage=S(JSON, nullable=True))


class DidService(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "did_services"
    __table_args__ = ({"schema": "authn"},)
    did: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    service_id: Mapped[str] = acol(
        storage=S(String(1000), nullable=False, unique=True, index=True)
    )
    service_type: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    endpoint: Mapped[dict | list | str] = acol(storage=S(JSON, nullable=False))


class DidResolutionCache(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "did_resolution_cache"
    __table_args__ = ({"schema": "authn"},)
    did_url: Mapped[str] = acol(
        storage=S(String(1000), nullable=False, unique=True, index=True)
    )
    result_digest: Mapped[str] = acol(
        storage=S(String(128), nullable=False, index=True)
    )
    result: Mapped[dict] = acol(storage=S(JSON, nullable=False))
    resolved_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    expires_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


class GnapGrant(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "gnap_grants"
    __table_args__ = ({"schema": "authn"},)
    grant_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    client_instance_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, index=True)
    )
    access_request: Mapped[dict | list] = acol(storage=S(JSON, nullable=False))
    status: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="pending", index=True)
    )
    subject_id: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    expires_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


class GnapContinuation(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "gnap_continuations"
    __table_args__ = ({"schema": "authn"},)
    grant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    continuation_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    token_digest: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    wait_seconds: Mapped[str | None] = acol(storage=S(String(16), nullable=True))
    expires_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


class GnapClientInstance(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "gnap_client_instances"
    __table_args__ = ({"schema": "authn"},)
    instance_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    key_reference: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    client_display: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    status: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="active", index=True)
    )


class GnapInteraction(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "gnap_interactions"
    __table_args__ = ({"schema": "authn"},)
    grant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    interaction_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    mode: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    finish_nonce_digest: Mapped[str | None] = acol(
        storage=S(String(128), nullable=True, index=True)
    )
    status: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="pending", index=True)
    )
    completed_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


__all__ = [
    "DidDocument",
    "DidDocumentVersion",
    "DidVerificationMethod",
    "DidService",
    "DidResolutionCache",
    "GnapGrant",
    "GnapContinuation",
    "GnapClientInstance",
    "GnapInteraction",
]
