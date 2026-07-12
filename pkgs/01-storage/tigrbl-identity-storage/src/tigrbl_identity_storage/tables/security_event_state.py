"""Durable security-event, subscription, delivery, and replay state."""

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


class SecurityEvent(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "security_events"
    __table_args__ = ({"schema": "authn"},)
    event_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    issuer: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    event_type: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    subject_identifier: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    token_digest: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    artifact_locator: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    issued_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    expires_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


class SecurityEventSubscription(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "security_event_subscriptions"
    __table_args__ = ({"schema": "authn"},)
    subscription_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    receiver: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    delivery_method: Mapped[str] = acol(
        storage=S(String(32), nullable=False, index=True)
    )
    endpoint: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    event_types: Mapped[list] = acol(storage=S(JSON, nullable=False))
    active: Mapped[bool] = acol(
        storage=S(Boolean, nullable=False, default=True, index=True)
    )


class SecurityEventDelivery(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "security_event_deliveries"
    __table_args__ = ({"schema": "authn"},)
    event_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    subscription_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, index=True)
    )
    attempt_id: Mapped[str] = acol(
        storage=S(String(255), nullable=False, unique=True, index=True)
    )
    status: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="pending", index=True)
    )
    error_code: Mapped[str | None] = acol(
        storage=S(String(128), nullable=True, index=True)
    )
    acknowledged_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    next_attempt_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )


class SecurityEventReplay(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "security_event_replays"
    __table_args__ = ({"schema": "authn"},)
    issuer: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    jti: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    replay_key_digest: Mapped[str] = acol(
        storage=S(String(128), nullable=False, unique=True, index=True)
    )
    expires_at: Mapped[dt.datetime] = acol(
        storage=S(TZDateTime, nullable=False, index=True)
    )
    consumed: Mapped[bool] = acol(
        storage=S(Boolean, nullable=False, default=True, index=True)
    )


__all__ = [
    "SecurityEvent",
    "SecurityEventSubscription",
    "SecurityEventDelivery",
    "SecurityEventReplay",
]
