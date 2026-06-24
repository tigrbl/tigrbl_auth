"""Durable logout propagation state."""

from __future__ import annotations

import datetime as dt
import uuid
from typing import Any

from tigrbl_identity_storage.framework import (
    RestOltpTable,
    BaseModel,
    Timestamped,
    S,
    acol,
    JSON,
    Boolean,
    Mapped,
    String,
    TZDateTime,
    GUIDPk,
    ForeignKeySpec,
    PgUUID,
)


class LogoutIn(BaseModel):
    id_token_hint: str | None = None
    post_logout_redirect_uri: str | None = None
    state: str | None = None
    sid: str | None = None
    client_id: str | None = None


class LogoutOut(BaseModel):
    status: str
    session_id: str | None = None
    logout_id: str | None = None
    post_logout_redirect_uri: str | None = None
    state: str | None = None
    cookie_cleared: bool = True
    cookie_policy: dict[str, Any] | None = None
    frontchannel_logout: dict[str, Any] | None = None
    backchannel_logout: dict[str, Any] | None = None
    replay_protected: bool = True


class LogoutState(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "logout_state"
    __table_args__ = ({"schema": "authn"},)

    session_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.sessions.id"), nullable=True, index=True)
    )
    sid: Mapped[str | None] = acol(storage=S(String(128), nullable=True, index=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="pending"))
    initiated_by: Mapped[str | None] = acol(storage=S(String(64), nullable=True))
    reason: Mapped[str | None] = acol(storage=S(String(128), nullable=True))
    frontchannel_required: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=False))
    backchannel_required: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=False))
    frontchannel_completed_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True))
    backchannel_completed_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True))
    propagated_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True))
    expires_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    logout_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


__all__ = ["LogoutIn", "LogoutOut", "LogoutState"]
