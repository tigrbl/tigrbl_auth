"""Durable logout propagation state."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
import uuid
from typing import Any

from tigrbl_identity_storage.framework import (
    Base,
    BaseModel,
    Depends,
    Timestamped,
    TigrblRouter,
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
from .._ops import create_record, first_record, record_id, update_record, utc_now
from ..engine import get_db


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


class LogoutState(Base, GUIDPk, Timestamped):
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

    @classmethod
    async def create_logout(
        cls,
        db: Any,
        *,
        session_id: uuid.UUID | None,
        initiated_by: str = "rp_logout",
        reason: str = "logout",
        frontchannel_required: bool = False,
        backchannel_required: bool = False,
        metadata: dict | None = None,
    ) -> "LogoutState":
        now = utc_now()
        return await create_record(
            cls,
            db,
            {
                "session_id": session_id,
                "sid": str(session_id) if session_id is not None else None,
                "status": "pending" if frontchannel_required or backchannel_required else "complete",
                "initiated_by": initiated_by,
                "reason": reason,
                "frontchannel_required": frontchannel_required,
                "backchannel_required": backchannel_required,
                "propagated_at": None if frontchannel_required or backchannel_required else now,
                "logout_metadata": metadata,
            },
        )

    @classmethod
    async def consume_logout(cls, db: Any, *, logout_id: uuid.UUID) -> "LogoutState | None":
        row = await first_record(cls, db, {"id": logout_id})
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "complete", "propagated_at": utc_now()})

    @classmethod
    async def expire(cls, db: Any, *, logout_id: uuid.UUID) -> "LogoutState | None":
        row = await first_record(cls, db, {"id": logout_id})
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "expired", "expires_at": utc_now()})


api = router = TigrblRouter()


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


@api.route("/logout", methods=["GET", "POST"], response_model=None)
async def logout(request: Any, db: Any = Depends(get_db)) -> Any:
    from ._op import logout_request

    result = await logout_request(request=request, db=db)
    from tigrbl_authn_credentials.session_service import observe_logout_response

    payload: dict[str, object] = {}
    body = getattr(result, "body", None)
    if body:
        try:
            payload = json.loads(body.decode("utf-8"))
        except Exception:
            payload = {}
    if not payload:
        headers = getattr(result, "headers", {}) or {}
        payload = {
            "status": headers.get("x-tigrbl-auth-logout-status"),
            "logout_id": headers.get("x-tigrbl-auth-logout-id"),
            "session_id": headers.get("x-tigrbl-auth-session-id"),
        }
    observe_logout_response(_repo_root(), session_id=payload.get("session_id"), details=payload)
    return result


LogoutState.logout = staticmethod(logout)  # type: ignore[attr-defined]


__all__ = ["LogoutIn", "LogoutOut", "LogoutState", "api", "router", "logout"]
