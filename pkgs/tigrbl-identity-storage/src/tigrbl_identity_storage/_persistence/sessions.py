from __future__ import annotations

from .token_records import *
from .token_records import (
    _clear_handler_records,
    _create_handler_record,
    _field,
    _first_handler_record,
    _list_handler_records,
    _read_handler_record,
    _record_id,
    _update_handler_record,
    _session,
)

async def introspect_token_async(token: str) -> dict[str, Any]:
    digest = token_hash(token)
    now = datetime.now(timezone.utc)
    try:
        async with _session() as db:
            record = await _first_handler_record(TokenRecord, db, {"token_hash": digest})
            if record is None:
                return {"active": False}
            expires_at = _field(record, "expires_at")
            if expires_at is not None:
                expiry = expires_at if expires_at.tzinfo is not None else expires_at.replace(tzinfo=timezone.utc)
                if expiry <= now:
                    await _update_handler_record(
                        TokenRecord,
                        db,
                        _record_id(record),
                        {"active": False, "revoked_reason": _field(record, "revoked_reason") or "expired"},
                    )
                    return {"active": False}
            revoked = await _first_handler_record(RevokedToken, db, {"token_hash": digest})
            if revoked is not None or _field(record, "revoked_at") is not None or not _field(record, "active"):
                await _update_handler_record(
                    TokenRecord,
                    db,
                    _record_id(record),
                    {"active": False, "last_introspected_at": now},
                )
                return {"active": False}
            await _update_handler_record(TokenRecord, db, _record_id(record), {"last_introspected_at": now})
            payload = dict(_field(record, "claims") or {})
            payload.setdefault("sub", _field(record, "subject"))
            if _field(record, "scope"):
                payload.setdefault("scope", _field(record, "scope"))
            if _field(record, "client_id") is not None:
                payload.setdefault("client_id", str(_field(record, "client_id")))
            if _field(record, "issuer"):
                payload.setdefault("iss", _field(record, "issuer"))
            if expires_at is not None:
                payload.setdefault("exp", int(expires_at.timestamp()))
            payload["active"] = True
            return payload
    except Exception:
        return {"active": False}


async def reset_token_state_async() -> None:
    try:
        async with _session() as db:
            await _clear_handler_records(RevokedToken, db)
            await _clear_handler_records(TokenRecord, db)
    except Exception:
        return None


async def create_session_async(
    *,
    user_id: UUID,
    tenant_id: UUID,
    username: str,
    client_id: UUID | None = None,
    expires_at: datetime | None = None,
    cookie_secret_hash: str | None = None,
    session_state_salt: str | None = None,
) -> AuthSession:
    async with _session() as db:
        return await AuthSession.create_for_user(
            db,
            user_id=user_id,
            tenant_id=tenant_id,
            username=username,
            client_id=client_id,
            expires_at=expires_at,
            cookie_secret_hash=cookie_secret_hash,
            session_state_salt=session_state_salt,
        )


async def touch_session_async(session_id: UUID) -> AuthSession | None:
    async with _session() as db:
        return await AuthSession.touch(db, session_id=session_id)


async def terminate_session_async(
    session_id: UUID,
    *,
    initiated_by: str = "rp_logout",
    reason: str = "logout",
    frontchannel_required: bool = False,
    backchannel_required: bool = False,
    metadata: dict[str, Any] | None = None,
) -> LogoutState | None:
    now = datetime.now(timezone.utc)
    async with _session() as db:
        row = await _read_handler_record(AuthSession, db, session_id)
        if row is None:
            return None

        existing_rows = await _list_handler_records(LogoutState, db, {"session_id": session_id})
        if existing_rows:
            existing_rows = sorted(existing_rows, key=lambda item: str(_field(item, "created_at", "") or _field(item, "id", "")), reverse=True)
            latest = existing_rows[0]
            current_meta = dict(_field(latest, "logout_metadata", {}) or {})
            if metadata:
                current_meta.update(metadata)
            return await _update_handler_record(
                LogoutState,
                db,
                _record_id(latest),
                {
                    "logout_metadata": current_meta or None,
                    "frontchannel_required": bool(_field(latest, "frontchannel_required") or frontchannel_required),
                    "backchannel_required": bool(_field(latest, "backchannel_required") or backchannel_required),
                },
            )

        await AuthSession.revoke_for_user(
            db,
            session_id=session_id,
            reason=reason,
        )
        return await LogoutState.create_logout(
            db,
            session_id=_record_id(row),
            initiated_by=initiated_by,
            reason=reason,
            frontchannel_required=frontchannel_required,
            backchannel_required=backchannel_required,
            metadata=metadata,
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
    async with _session() as db:
        row = await _read_handler_record(LogoutState, db, logout_id)
        if row is None:
            return None
        current_meta = dict(_field(row, "logout_metadata") or {})
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
        frontchannel_completed_at = payload.get("frontchannel_completed_at", _field(row, "frontchannel_completed_at"))
        backchannel_completed_at = payload.get("backchannel_completed_at", _field(row, "backchannel_completed_at"))
        if (not _field(row, "frontchannel_required") or frontchannel_completed_at is not None) and (
            not _field(row, "backchannel_required") or backchannel_completed_at is not None
        ):
            payload["status"] = "complete"
            payload["propagated_at"] = now
        else:
            payload["status"] = "pending" if status != "complete" else _field(row, "status")
        return await _update_handler_record(LogoutState, db, logout_id, payload)


async def get_session_async(session_id: UUID) -> AuthSession | None:
    async with _session() as db:
        return await _read_handler_record(AuthSession, db, session_id)


async def get_active_session_async(session_id: UUID) -> AuthSession | None:
    async with _session() as db:
        row = await _read_handler_record(AuthSession, db, session_id)
        if row is None:
            return None
        if _field(row, "ended_at") is not None or str(_field(row, "session_state")).lower() in {"terminated", "ended", "revoked"}:
            return None
        expires_at = _field(row, "expires_at")
        if expires_at is not None:
            expiry = expires_at if expires_at.tzinfo is not None else expires_at.replace(tzinfo=timezone.utc)
            if expiry <= datetime.now(timezone.utc):
                await _update_handler_record(
                    AuthSession,
                    db,
                    session_id,
                    {"session_state": "expired", "ended_at": _field(row, "ended_at") or datetime.now(timezone.utc)},
                )
                return None
        return row


async def rotate_session_cookie_secret_async(session_id: UUID, *, cookie_secret_hash: str) -> AuthSession | None:
    async with _session() as db:
        row = await _read_handler_record(AuthSession, db, session_id)
        if row is None:
            return None
        now = datetime.now(timezone.utc)
        return await _update_handler_record(
            AuthSession,
            db,
            session_id,
            {
                "cookie_secret_hash": cookie_secret_hash,
                "cookie_rotated_at": now,
                "cookie_issued_at": _field(row, "cookie_issued_at") or now,
                "last_seen_at": now,
            },
        )


async def bind_session_client_async(session_id: UUID, *, client_id: UUID | None) -> AuthSession | None:
    async with _session() as db:
        row = await _read_handler_record(AuthSession, db, session_id)
        if row is None:
            return None
        return await _update_handler_record(
            AuthSession,
            db,
            session_id,
            {"client_id": client_id, "last_seen_at": datetime.now(timezone.utc)},
        )


async def get_latest_logout_for_session_async(session_id: UUID) -> LogoutState | None:
    async with _session() as db:
        rows = await _list_handler_records(LogoutState, db, {"session_id": session_id})
        if not rows:
            return None
        rows = sorted(rows, key=lambda item: str(_field(item, "created_at", "") or _field(item, "id", "")), reverse=True)
        return rows[0]


async def update_logout_metadata_async(logout_id: UUID, *, metadata: dict[str, Any] | None = None, status: str | None = None) -> LogoutState | None:
    async with _session() as db:
        row = await _read_handler_record(LogoutState, db, logout_id)
        if row is None:
            return None
        current = dict(_field(row, "logout_metadata") or {})
        if metadata:
            current.update(metadata)
        payload: dict[str, Any] = {"logout_metadata": current or None}
        if status is not None:
            payload["status"] = status
        return await _update_handler_record(LogoutState, db, logout_id, payload)


async def get_client_registration_async(client_id: UUID) -> ClientRegistration | None:
    async with _session() as db:
        return await _first_handler_record(ClientRegistration, db, {"client_id": client_id})


async def record_consent_async(
    *,
    user_id: UUID,
    tenant_id: UUID,
    client_id: UUID,
    scope: str,
    claims: dict[str, Any] | None = None,
    expires_at: datetime | None = None,
) -> Consent:
    async with _session() as db:
        return await Consent.grant(
            db,
            user_id=user_id,
            tenant_id=tenant_id,
            client_id=client_id,
            scope=scope,
            claims=claims,
            expires_at=expires_at,
        )


async def revoke_consent_async(consent_id: UUID) -> Consent | None:
    async with _session() as db:
        return await Consent.revoke_for_user(db, consent_id=consent_id)
