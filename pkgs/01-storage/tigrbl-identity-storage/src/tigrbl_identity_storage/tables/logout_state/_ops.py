"""LogoutState-owned lifecycle helpers formerly exposed by storage persistence."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from .._ops import create_record, field, list_handler_records, read_handler_record, record_id, update_handler_record
from .._sync import run_async
from ..engine import storage_session
from ..auth_session._table import AuthSession
from ._table import LogoutState


async def terminate_session_async(
    session_id: UUID,
    *,
    initiated_by: str = "rp_logout",
    reason: str = "logout",
    frontchannel_required: bool = False,
    backchannel_required: bool = False,
    metadata: dict[str, Any] | None = None,
) -> LogoutState | None:
    async with storage_session() as db:
        row = await read_handler_record(AuthSession, db, session_id)
        if row is None:
            return None
        existing_rows = await list_handler_records(LogoutState, db, {"session_id": session_id})
        if existing_rows:
            existing_rows = sorted(
                existing_rows,
                key=lambda item: str(field(item, "created_at", "") or field(item, "id", "")),
                reverse=True,
            )
            latest = existing_rows[0]
            current_meta = dict(field(latest, "logout_metadata", {}) or {})
            if metadata:
                current_meta.update(metadata)
            return await update_handler_record(
                LogoutState,
                db,
                record_id(latest),
                {
                    "logout_metadata": current_meta or None,
                    "frontchannel_required": bool(field(latest, "frontchannel_required") or frontchannel_required),
                    "backchannel_required": bool(field(latest, "backchannel_required") or backchannel_required),
                },
            )
        await AuthSession.revoke_for_user(db, session_id=session_id, reason=reason)
        return await create_record(
            LogoutState,
            db,
            {
                "session_id": record_id(row),
                "initiated_by": initiated_by,
                "reason": reason,
                "frontchannel_required": frontchannel_required,
                "backchannel_required": backchannel_required,
                "logout_metadata": metadata,
                "status": "pending",
            },
        )


async def mark_logout_channel_async(
    logout_id: UUID,
    *,
    channel: str,
    status: str = "complete",
    reason: str | None = None,
    retry_after_seconds: int | None = None,
    metadata: dict[str, Any] | None = None,
) -> LogoutState | None:
    now = datetime.now(timezone.utc)
    now_iso = now.replace(microsecond=0).isoformat()
    async with storage_session() as db:
        row = await read_handler_record(LogoutState, db, logout_id)
        if row is None:
            return None
        current_meta = dict(field(row, "logout_metadata") or {})
        channel_meta = dict(current_meta.get(channel) or {})
        if metadata:
            channel_meta.update(dict(metadata))
        delivery = dict(channel_meta.get("delivery") or {})
        prior_attempts = int(delivery.get("attempts", 0) or 0)
        delivery["channel"] = channel
        delivery["status"] = str(status)
        delivery["attempts"] = max(prior_attempts + 1, 1)
        delivery["updated_at"] = now_iso
        if reason is not None:
            delivery["reason"] = str(reason)
        if retry_after_seconds is not None:
            delivery["retry_after_seconds"] = int(retry_after_seconds)
        if status == "complete":
            delivery["completed_at"] = now_iso
        channel_meta["delivery"] = delivery
        channel_meta["status"] = delivery["status"]
        current_meta[channel] = channel_meta
        current_meta[f"{channel}_delivery"] = dict(delivery)
        payload: dict[str, Any] = {"logout_metadata": current_meta or None}
        if channel == "frontchannel" and status == "complete":
            payload["frontchannel_completed_at"] = now
        elif channel == "backchannel" and status == "complete":
            payload["backchannel_completed_at"] = now
        frontchannel_completed_at = payload.get("frontchannel_completed_at", field(row, "frontchannel_completed_at"))
        backchannel_completed_at = payload.get("backchannel_completed_at", field(row, "backchannel_completed_at"))
        if (not field(row, "frontchannel_required") or frontchannel_completed_at is not None) and (
            not field(row, "backchannel_required") or backchannel_completed_at is not None
        ):
            payload["status"] = "complete"
            payload["propagated_at"] = now
        else:
            payload["status"] = "pending" if status != "complete" else field(row, "status")
        return await update_handler_record(LogoutState, db, logout_id, payload)


async def get_latest_logout_for_session_async(session_id: UUID) -> LogoutState | None:
    async with storage_session() as db:
        rows = await list_handler_records(LogoutState, db, {"session_id": session_id})
        if not rows:
            return None
        rows = sorted(rows, key=lambda item: str(field(item, "created_at", "") or field(item, "id", "")), reverse=True)
        return rows[0]


async def update_logout_metadata_async(
    logout_id: UUID,
    *,
    metadata: dict[str, Any] | None = None,
    status: str | None = None,
) -> LogoutState | None:
    async with storage_session() as db:
        row = await read_handler_record(LogoutState, db, logout_id)
        if row is None:
            return None
        current = dict(field(row, "logout_metadata") or {})
        if metadata:
            current.update(metadata)
        payload: dict[str, Any] = {"logout_metadata": current or None}
        if status is not None:
            payload["status"] = status
        return await update_handler_record(LogoutState, db, logout_id, payload)


def terminate_session(session_id, **kwargs):
    return run_async(terminate_session_async(session_id, **kwargs))
def get_latest_logout_for_session(session_id):
    return run_async(get_latest_logout_for_session_async(session_id))
def update_logout_metadata(logout_id, **kwargs):
    return run_async(update_logout_metadata_async(logout_id, **kwargs))
def mark_logout_channel(logout_id, **kwargs):
    return run_async(mark_logout_channel_async(logout_id, **kwargs))


__all__ = [
    "get_latest_logout_for_session",
    "get_latest_logout_for_session_async",
    "mark_logout_channel",
    "mark_logout_channel_async",
    "terminate_session",
    "terminate_session_async",
    "update_logout_metadata",
    "update_logout_metadata_async",
]
