"""Durable logout propagation state."""

from __future__ import annotations

import datetime as dt
import uuid
from datetime import timezone
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
    op_ctx,
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


def _items(result: Any) -> list[Any]:
    if isinstance(result, dict) and isinstance(result.get("items"), list):
        return result["items"]
    if isinstance(result, list):
        return result
    if isinstance(result, tuple):
        return list(result)
    return [] if result is None else [result]


def _created(result: Any) -> Any:
    if isinstance(result, dict):
        for key in ("item", "result", "data"):
            if key in result:
                return result[key]
    return result


def _field(row: Any, key: str, default: Any = None) -> Any:
    if row is None:
        return default
    if isinstance(row, dict):
        return row.get(key, default)
    return getattr(row, key, default)


def _record_id(row: Any) -> Any:
    return _field(row, "id")


def _latest(rows: list[Any]) -> Any:
    if not rows:
        return None
    return sorted(rows, key=lambda item: str(_field(item, "created_at", "") or _field(item, "id", "")), reverse=True)[0]


@op_ctx(
    bind=LogoutState,
    alias="latest_for_session",
    target="custom",
    arity="collection",
    rest=False,
)
async def latest_for_session(cls: type[LogoutState], ctx: dict[str, Any]) -> LogoutState | None:
    payload = dict(ctx.get("payload") or {})
    session_id = payload.get("session_id") or dict(ctx.get("path_params") or {}).get("session_id")
    rows = _items(await cls.handlers.list.core({"payload": {"filters": {"session_id": session_id}}, "db": ctx["db"]}))
    return _latest(rows)


@op_ctx(
    bind=LogoutState,
    alias="update_metadata",
    target="custom",
    arity="member",
    rest=False,
)
async def update_metadata(cls: type[LogoutState], ctx: dict[str, Any]) -> LogoutState | None:
    payload = dict(ctx.get("payload") or {})
    logout_id = payload.get("logout_id") or payload.get("id") or dict(ctx.get("path_params") or {}).get("id")
    row = await cls.handlers.read.core({"path_params": {"id": logout_id}, "db": ctx["db"]})
    if row is None:
        return None
    current = dict(_field(row, "logout_metadata") or {})
    metadata = payload.get("metadata")
    if metadata:
        current.update(dict(metadata))
    update_payload: dict[str, Any] = {"logout_metadata": current or None}
    if payload.get("status") is not None:
        update_payload["status"] = payload["status"]
    return _created(
        await cls.handlers.update.core({"path_params": {"id": logout_id}, "payload": update_payload, "db": ctx["db"]})
    )


@op_ctx(
    bind=LogoutState,
    alias="mark_channel",
    target="custom",
    arity="member",
    rest=False,
)
async def mark_channel(cls: type[LogoutState], ctx: dict[str, Any]) -> LogoutState | None:
    payload = dict(ctx.get("payload") or {})
    logout_id = payload.get("logout_id") or payload.get("id") or dict(ctx.get("path_params") or {}).get("id")
    row = await cls.handlers.read.core({"path_params": {"id": logout_id}, "db": ctx["db"]})
    if row is None:
        return None
    channel = str(payload["channel"])
    status = str(payload.get("status") or "complete")
    now = dt.datetime.now(timezone.utc)
    now_iso = now.replace(microsecond=0).isoformat()
    current_meta = dict(_field(row, "logout_metadata") or {})
    channel_meta = dict(current_meta.get(channel) or {})
    if payload.get("metadata"):
        channel_meta.update(dict(payload["metadata"]))
    delivery = dict(channel_meta.get("delivery") or {})
    delivery["channel"] = channel
    delivery["status"] = status
    delivery["attempts"] = max(int(delivery.get("attempts", 0) or 0) + 1, 1)
    delivery["updated_at"] = now_iso
    if payload.get("reason") is not None:
        delivery["reason"] = str(payload["reason"])
    if payload.get("retry_after_seconds") is not None:
        delivery["retry_after_seconds"] = int(payload["retry_after_seconds"])
    if status == "complete":
        delivery["completed_at"] = now_iso
    channel_meta["delivery"] = delivery
    channel_meta["status"] = delivery["status"]
    current_meta[channel] = channel_meta
    current_meta[f"{channel}_delivery"] = dict(delivery)
    update_payload: dict[str, Any] = {"logout_metadata": current_meta or None}
    if channel == "frontchannel" and status == "complete":
        update_payload["frontchannel_completed_at"] = now
    elif channel == "backchannel" and status == "complete":
        update_payload["backchannel_completed_at"] = now
    front_done = update_payload.get("frontchannel_completed_at", _field(row, "frontchannel_completed_at"))
    back_done = update_payload.get("backchannel_completed_at", _field(row, "backchannel_completed_at"))
    if (not _field(row, "frontchannel_required") or front_done is not None) and (
        not _field(row, "backchannel_required") or back_done is not None
    ):
        update_payload["status"] = "complete"
        update_payload["propagated_at"] = now
    else:
        update_payload["status"] = "pending" if status != "complete" else _field(row, "status")
    return _created(
        await cls.handlers.update.core({"path_params": {"id": logout_id}, "payload": update_payload, "db": ctx["db"]})
    )


@op_ctx(
    bind=LogoutState,
    alias="ensure_for_session",
    target="custom",
    arity="collection",
    rest=False,
)
async def ensure_for_session(cls: type[LogoutState], ctx: dict[str, Any]) -> LogoutState | None:
    payload = dict(ctx.get("payload") or {})
    session_id = payload["session_id"]
    db = ctx["db"]
    existing_rows = _items(await cls.handlers.list.core({"payload": {"filters": {"session_id": session_id}}, "db": db}))
    latest = _latest(existing_rows)
    if latest is not None:
        current_meta = dict(_field(latest, "logout_metadata") or {})
        if payload.get("metadata"):
            current_meta.update(dict(payload["metadata"]))
        update_payload = {
            "logout_metadata": current_meta or None,
            "frontchannel_required": bool(_field(latest, "frontchannel_required") or payload.get("frontchannel_required")),
            "backchannel_required": bool(_field(latest, "backchannel_required") or payload.get("backchannel_required")),
        }
        return _created(
            await cls.handlers.update.core(
                {"path_params": {"id": _record_id(latest)}, "payload": update_payload, "db": db}
            )
        )
    return _created(
        await cls.handlers.create.core(
            {
                "payload": {
                    "session_id": session_id,
                    "initiated_by": payload.get("initiated_by") or "rp_logout",
                    "reason": payload.get("reason") or "logout",
                    "frontchannel_required": bool(payload.get("frontchannel_required")),
                    "backchannel_required": bool(payload.get("backchannel_required")),
                    "logout_metadata": payload.get("metadata"),
                    "status": "pending",
                },
                "db": db,
            }
        )
    )


__all__ = ["LogoutIn", "LogoutOut", "LogoutState"]
