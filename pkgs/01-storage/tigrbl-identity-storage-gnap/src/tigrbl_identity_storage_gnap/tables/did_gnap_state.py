# ruff: noqa: F401
"""Optional durable DID authority/cache and GNAP transaction state."""
from __future__ import annotations
import datetime as dt
from tigrbl_identity_storage_core.framework import Boolean, GUIDPk, JSON, Mapped, RestOltpTable, S, String, TZDateTime, Timestamped, acol

class GnapGrant(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = 'gnap_grants'
    __table_args__ = ({'schema': 'authn'},)
    grant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    client_instance_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    access_request: Mapped[dict | list] = acol(storage=S(JSON, nullable=False))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default='pending', index=True))
    subject_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    expires_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))

class GnapContinuation(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = 'gnap_continuations'
    __table_args__ = ({'schema': 'authn'},)
    grant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    continuation_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    token_digest: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    wait_seconds: Mapped[str | None] = acol(storage=S(String(16), nullable=True))
    expires_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))

class GnapClientInstance(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = 'gnap_client_instances'
    __table_args__ = ({'schema': 'authn'},)
    instance_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    key_reference: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    client_display: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default='active', index=True))

class GnapInteraction(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = 'gnap_interactions'
    __table_args__ = ({'schema': 'authn'},)
    grant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    interaction_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    mode: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    finish_nonce_digest: Mapped[str | None] = acol(storage=S(String(128), nullable=True, index=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default='pending', index=True))
    completed_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
