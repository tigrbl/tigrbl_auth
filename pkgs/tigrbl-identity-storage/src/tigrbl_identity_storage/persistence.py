"""Durable persistence helpers for token, session, consent, audit, and logout lifecycle state."""

from __future__ import annotations

import asyncio
import hashlib
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from threading import Thread
from typing import Any, AsyncIterator, Iterable
from uuid import UUID

from tigrbl_auth.framework import delete, select
from tigrbl_auth.runtime.engine_resolver import resolve_api_provider
from tigrbl_identity_storage.tables import (
    AuditEvent,
    AuthSession,
    ClientRegistration,
    Consent,
    LogoutState,
    RevokedToken,
    Tenant,
    TokenRecord,
)
from tigrbl_identity_storage.tables.engine import ENGINE


def _run(coro):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    result = None
    error: BaseException | None = None

    def runner() -> None:
        nonlocal result, error
        try:
            result = asyncio.run(coro)
        except BaseException as exc:  # pragma: no cover - surfaced to caller
            error = exc

    thread = Thread(target=runner)
    thread.start()
    thread.join()
    if error is not None:
        raise error
    return result


def _resolve_provider():
    try:
        from tigrbl_auth.api.surfaces import surface_api

        provider = resolve_api_provider(surface_api)
        if provider is not None:
            return provider
    except Exception:
        pass
    return ENGINE.provider


@asynccontextmanager
async def _session() -> AsyncIterator[Any]:
    provider = _resolve_provider()
    _, maker = provider.ensure()
    async with maker() as session:
        yield session


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _to_uuid(value: Any) -> UUID | None:
    if value in {None, "", False}:
        return None
    if isinstance(value, UUID):
        return value
    try:
        return UUID(str(value))
    except Exception:
        return None


def _to_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
    try:
        return datetime.fromtimestamp(int(value), tz=timezone.utc)
    except Exception:
        return None


def _normalize_audience(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (str, dict, list)):
        return value
    if isinstance(value, tuple):
        return list(value)
    return str(value)


async def upsert_token_record_async(
    token: str,
    claims: dict[str, Any] | None = None,
    *,
    token_kind: str | None = None,
    token_type_hint: str | None = None,
    refresh_family_id: str | None = None,
    refresh_parent_hash: str | None = None,
    refresh_successor_hash: str | None = None,
    used_at: datetime | None = None,
    reuse_detected_at: datetime | None = None,
) -> str:
    claims = dict(claims or {})
    digest = token_hash(token)
    token_kind = token_kind or str(claims.get("kind") or claims.get("typ") or "access")
    try:
        async with _session() as session:
            record = await session.scalar(select(TokenRecord).where(TokenRecord.token_hash == digest))
            now = datetime.now(timezone.utc)
            if record is None:
                record = TokenRecord(token_hash=digest, token_kind=token_kind, subject=str(claims.get("sub") or ""))
                session.add(record)
            record.token_kind = token_kind
            record.token_type_hint = token_type_hint or record.token_type_hint or token_kind
            record.refresh_family_id = refresh_family_id or record.refresh_family_id
            record.refresh_parent_hash = refresh_parent_hash or record.refresh_parent_hash
            record.refresh_successor_hash = refresh_successor_hash or record.refresh_successor_hash
            record.active = True
            record.subject = str(claims.get("sub") or record.subject or "")
            record.tenant_id = _to_uuid(claims.get("tid") or record.tenant_id)
            record.client_id = _to_uuid(claims.get("client_id") or claims.get("azp") or record.client_id)
            record.scope = claims.get("scope") or record.scope
            record.issuer = claims.get("iss") or record.issuer
            record.audience = _normalize_audience(claims.get("aud") or record.audience)
            record.claims = claims
            record.issued_at = _to_datetime(claims.get("iat")) or record.issued_at or now
            record.expires_at = _to_datetime(claims.get("exp")) or record.expires_at
            record.used_at = used_at or record.used_at
            record.reuse_detected_at = reuse_detected_at or record.reuse_detected_at
            record.revoked_at = None
            record.revoked_reason = None
            await session.commit()
    except Exception:
        return digest
    return digest


async def remove_token_record_async(token: str) -> None:
    digest = token_hash(token)
    try:
        async with _session() as session:
            record = await session.scalar(select(TokenRecord).where(TokenRecord.token_hash == digest))
            if record is not None:
                await session.delete(record)
                await session.commit()
    except Exception:
        return None


async def get_token_record_async(token: str) -> TokenRecord | None:
    digest = token_hash(token)
    try:
        async with _session() as session:
            return await session.scalar(select(TokenRecord).where(TokenRecord.token_hash == digest))
    except Exception:
        return None


async def revoke_token_async(
    token: str,
    *,
    token_type_hint: str | None = None,
    reason: str | None = None,
) -> str:
    digest = token_hash(token)
    now = datetime.now(timezone.utc)
    try:
        async with _session() as session:
            record = await session.scalar(select(TokenRecord).where(TokenRecord.token_hash == digest))
            revoked = await session.scalar(select(RevokedToken).where(RevokedToken.token_hash == digest))
            if revoked is None:
                revoked = RevokedToken(token_hash=digest)
                session.add(revoked)
            if record is not None:
                record.active = False
                record.revoked_at = now
                record.revoked_reason = reason or record.revoked_reason or "revoked"
                revoked.subject = record.subject
                revoked.tenant_id = record.tenant_id
                revoked.client_id = record.client_id
                revoked.expires_at = record.expires_at
                revoked.token_type_hint = token_type_hint or record.token_type_hint
            revoked.revoked_reason = reason or revoked.revoked_reason or "revoked"
            revoked.token_type_hint = token_type_hint or revoked.token_type_hint
            await session.commit()
    except Exception:
        return digest
    return digest


async def mark_token_used_async(
    token: str,
    *,
    successor_token: str | None = None,
    reason: str = "refresh_rotated",
) -> str:
    digest = token_hash(token)
    successor_hash = token_hash(successor_token) if successor_token else None
    now = datetime.now(timezone.utc)
    try:
        async with _session() as session:
            record = await session.scalar(select(TokenRecord).where(TokenRecord.token_hash == digest))
            if record is None:
                return digest
            record.used_at = now
            record.active = False
            record.revoked_at = now
            record.revoked_reason = reason
            if successor_hash:
                record.refresh_successor_hash = successor_hash
            await session.commit()
    except Exception:
        return digest
    return digest


async def revoke_refresh_family_async(
    family_id: str,
    *,
    reason: str = "refresh_token_reuse_detected",
    reuse_token: str | None = None,
) -> int:
    if not family_id:
        return 0
    now = datetime.now(timezone.utc)
    reuse_hash = token_hash(reuse_token) if reuse_token else None
    revoked_count = 0
    try:
        async with _session() as session:
            rows = (
                await session.execute(select(TokenRecord).where(TokenRecord.refresh_family_id == family_id))
            ).scalars().all()
            for row in rows:
                row.active = False
                row.revoked_at = row.revoked_at or now
                row.revoked_reason = reason
                if reuse_hash and row.token_hash == reuse_hash:
                    row.reuse_detected_at = now
                revoked = await session.scalar(select(RevokedToken).where(RevokedToken.token_hash == row.token_hash))
                if revoked is None:
                    revoked = RevokedToken(token_hash=row.token_hash)
                    session.add(revoked)
                revoked.subject = row.subject
                revoked.tenant_id = row.tenant_id
                revoked.client_id = row.client_id
                revoked.expires_at = row.expires_at
                revoked.token_type_hint = row.token_type_hint
                revoked.revoked_reason = reason
                revoked_count += 1
            await session.commit()
    except Exception:
        return 0
    return revoked_count


async def is_token_revoked_async(token: str) -> bool:
    digest = token_hash(token)
    try:
        async with _session() as session:
            revoked = await session.scalar(select(RevokedToken).where(RevokedToken.token_hash == digest))
            if revoked is not None:
                return True
            record = await session.scalar(select(TokenRecord).where(TokenRecord.token_hash == digest))
            if record is None:
                return False
            if record.revoked_at is not None:
                return True
            if record.expires_at is not None:
                expiry = record.expires_at if record.expires_at.tzinfo is not None else record.expires_at.replace(tzinfo=timezone.utc)
                if expiry <= datetime.now(timezone.utc):
                    return True
            return not bool(record.active)
    except Exception:
        return False


async def introspect_token_async(token: str) -> dict[str, Any]:
    digest = token_hash(token)
    now = datetime.now(timezone.utc)
    try:
        async with _session() as session:
            record = await session.scalar(select(TokenRecord).where(TokenRecord.token_hash == digest))
            if record is None:
                return {"active": False}
            if record.expires_at is not None:
                expiry = record.expires_at if record.expires_at.tzinfo is not None else record.expires_at.replace(tzinfo=timezone.utc)
                if expiry <= now:
                    record.active = False
                    record.revoked_reason = record.revoked_reason or "expired"
                    await session.commit()
                    return {"active": False}
            revoked = await session.scalar(select(RevokedToken).where(RevokedToken.token_hash == digest))
            if revoked is not None or record.revoked_at is not None or not record.active:
                record.active = False
                record.last_introspected_at = now
                await session.commit()
                return {"active": False}
            record.last_introspected_at = now
            payload = dict(record.claims or {})
            payload.setdefault("sub", record.subject)
            if record.scope:
                payload.setdefault("scope", record.scope)
            if record.client_id is not None:
                payload.setdefault("client_id", str(record.client_id))
            if record.issuer:
                payload.setdefault("iss", record.issuer)
            if record.expires_at is not None:
                payload.setdefault("exp", int(record.expires_at.timestamp()))
            payload["active"] = True
            await session.commit()
            return payload
    except Exception:
        return {"active": False}


async def reset_token_state_async() -> None:
    try:
        async with _session() as session:
            await session.execute(delete(RevokedToken))
            await session.execute(delete(TokenRecord))
            await session.commit()
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
    async with _session() as session:
        now = datetime.now(timezone.utc)
        row = AuthSession(
            user_id=user_id,
            tenant_id=tenant_id,
            username=username,
            client_id=client_id,
            auth_time=now,
            session_state="active",
            session_state_salt=session_state_salt,
            cookie_secret_hash=cookie_secret_hash,
            cookie_issued_at=now if cookie_secret_hash else None,
            cookie_rotated_at=now if cookie_secret_hash else None,
            expires_at=expires_at,
            last_seen_at=now,
        )
        session.add(row)
        await session.commit()
        try:
            await session.refresh(row)
        except Exception:
            pass
        return row


async def touch_session_async(session_id: UUID) -> AuthSession | None:
    async with _session() as session:
        row = await session.scalar(select(AuthSession).where(AuthSession.id == session_id))
        if row is None:
            return None
        row.last_seen_at = datetime.now(timezone.utc)
        await session.commit()
        return row


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
    async with _session() as session:
        row = await session.scalar(select(AuthSession).where(AuthSession.id == session_id))
        if row is None:
            return None

        existing_rows = (await session.execute(select(LogoutState).where(LogoutState.session_id == session_id))).scalars().all()
        if existing_rows:
            existing_rows = sorted(existing_rows, key=lambda item: str(getattr(item, 'created_at', '') or getattr(item, 'id', '')), reverse=True)
            latest = existing_rows[0]
            current_meta = dict(getattr(latest, 'logout_metadata', {}) or {})
            if metadata:
                current_meta.update(metadata)
            latest.logout_metadata = current_meta or None
            latest.frontchannel_required = bool(latest.frontchannel_required or frontchannel_required)
            latest.backchannel_required = bool(latest.backchannel_required or backchannel_required)
            await session.commit()
            return latest

        row.session_state = "terminated"
        row.ended_at = now
        row.logout_reason = reason
        logout = LogoutState(
            session_id=row.id,
            sid=str(row.id),
            status="pending" if frontchannel_required or backchannel_required else "complete",
            initiated_by=initiated_by,
            reason=reason,
            frontchannel_required=frontchannel_required,
            backchannel_required=backchannel_required,
            propagated_at=None if frontchannel_required or backchannel_required else now,
            logout_metadata=metadata,
        )
        session.add(logout)
        await session.commit()
        try:
            await session.refresh(logout)
        except Exception:
            pass
        return logout


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
    async with _session() as session:
        row = await session.scalar(select(LogoutState).where(LogoutState.id == logout_id))
        if row is None:
            return None
        current_meta = dict(row.logout_metadata or {})
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
        row.logout_metadata = current_meta or None
        if channel == "frontchannel" and status == "complete":
            row.frontchannel_completed_at = now
        elif channel == "backchannel" and status == "complete":
            row.backchannel_completed_at = now
        if (not row.frontchannel_required or row.frontchannel_completed_at is not None) and (
            not row.backchannel_required or row.backchannel_completed_at is not None
        ):
            row.status = "complete"
            row.propagated_at = now
        else:
            row.status = "pending" if status != "complete" else row.status
        await session.commit()
        return row


async def get_session_async(session_id: UUID) -> AuthSession | None:
    async with _session() as session:
        return await session.scalar(select(AuthSession).where(AuthSession.id == session_id))


async def get_active_session_async(session_id: UUID) -> AuthSession | None:
    async with _session() as session:
        row = await session.scalar(select(AuthSession).where(AuthSession.id == session_id))
        if row is None:
            return None
        if row.ended_at is not None or str(row.session_state).lower() in {"terminated", "ended", "revoked"}:
            return None
        if row.expires_at is not None:
            expiry = row.expires_at if row.expires_at.tzinfo is not None else row.expires_at.replace(tzinfo=timezone.utc)
            if expiry <= datetime.now(timezone.utc):
                row.session_state = "expired"
                row.ended_at = row.ended_at or datetime.now(timezone.utc)
                await session.commit()
                return None
        return row


async def rotate_session_cookie_secret_async(session_id: UUID, *, cookie_secret_hash: str) -> AuthSession | None:
    async with _session() as session:
        row = await session.scalar(select(AuthSession).where(AuthSession.id == session_id))
        if row is None:
            return None
        now = datetime.now(timezone.utc)
        row.cookie_secret_hash = cookie_secret_hash
        row.cookie_rotated_at = now
        row.cookie_issued_at = row.cookie_issued_at or now
        row.last_seen_at = now
        await session.commit()
        return row


async def bind_session_client_async(session_id: UUID, *, client_id: UUID | None) -> AuthSession | None:
    async with _session() as session:
        row = await session.scalar(select(AuthSession).where(AuthSession.id == session_id))
        if row is None:
            return None
        row.client_id = client_id
        row.last_seen_at = datetime.now(timezone.utc)
        await session.commit()
        return row


async def get_latest_logout_for_session_async(session_id: UUID) -> LogoutState | None:
    async with _session() as session:
        rows = (await session.execute(select(LogoutState).where(LogoutState.session_id == session_id))).scalars().all()
        if not rows:
            return None
        rows = sorted(rows, key=lambda item: str(getattr(item, 'created_at', '') or getattr(item, 'id', '')), reverse=True)
        return rows[0]


async def update_logout_metadata_async(logout_id: UUID, *, metadata: dict[str, Any] | None = None, status: str | None = None) -> LogoutState | None:
    async with _session() as session:
        row = await session.scalar(select(LogoutState).where(LogoutState.id == logout_id))
        if row is None:
            return None
        current = dict(row.logout_metadata or {})
        if metadata:
            current.update(metadata)
        row.logout_metadata = current or None
        if status is not None:
            row.status = status
        await session.commit()
        return row


async def get_client_registration_async(client_id: UUID) -> ClientRegistration | None:
    async with _session() as session:
        return await session.scalar(select(ClientRegistration).where(ClientRegistration.client_id == client_id))


async def record_consent_async(
    *,
    user_id: UUID,
    tenant_id: UUID,
    client_id: UUID,
    scope: str,
    claims: dict[str, Any] | None = None,
    expires_at: datetime | None = None,
) -> Consent:
    async with _session() as session:
        row = Consent(
            user_id=user_id,
            tenant_id=tenant_id,
            client_id=client_id,
            scope=scope,
            claims=claims,
            granted_at=datetime.now(timezone.utc),
            expires_at=expires_at,
            state="active",
        )
        session.add(row)
        await session.commit()
        try:
            await session.refresh(row)
        except Exception:
            pass
        return row


async def revoke_consent_async(consent_id: UUID) -> Consent | None:
    async with _session() as session:
        row = await session.scalar(select(Consent).where(Consent.id == consent_id))
        if row is None:
            return None
        row.state = "revoked"
        row.revoked_at = datetime.now(timezone.utc)
        await session.commit()
        return row


async def upsert_client_registration_async(
    *,
    client_id: UUID,
    tenant_id: UUID | None = None,
    metadata: dict[str, Any] | None = None,
    contacts: Iterable[str] | None = None,
    software_id: str | None = None,
    software_version: str | None = None,
    registration_access_token_hash: str | None = None,
    registration_client_uri: str | None = None,
) -> ClientRegistration:
    async with _session() as session:
        row = await session.scalar(select(ClientRegistration).where(ClientRegistration.client_id == client_id))
        if row is None:
            row = ClientRegistration(client_id=client_id, tenant_id=tenant_id)
            session.add(row)
        row.tenant_id = tenant_id or row.tenant_id
        row.registration_metadata = metadata or row.registration_metadata
        row.contacts = list(contacts) if contacts is not None else row.contacts
        row.software_id = software_id or row.software_id
        row.software_version = software_version or row.software_version
        row.registration_access_token_hash = registration_access_token_hash or row.registration_access_token_hash
        row.registration_client_uri = registration_client_uri or row.registration_client_uri
        row.issued_at = row.issued_at or datetime.now(timezone.utc)
        await session.commit()
        try:
            await session.refresh(row)
        except Exception:
            pass
        return row


async def append_audit_event_async(
    *,
    tenant_id: UUID | None = None,
    actor_user_id: UUID | None = None,
    actor_client_id: UUID | None = None,
    session_id: UUID | None = None,
    event_type: str,
    target_type: str | None = None,
    target_id: str | None = None,
    outcome: str = "success",
    request_id: str | None = None,
    details: dict[str, Any] | None = None,
) -> AuditEvent:
    async with _session() as session:
        effective_tenant_id = tenant_id
        if effective_tenant_id is None:
            effective_tenant_id = await session.scalar(select(Tenant.id))
        row = AuditEvent(
            tenant_id=effective_tenant_id,
            actor_user_id=actor_user_id,
            actor_client_id=actor_client_id,
            session_id=session_id,
            event_type=event_type,
            target_type=target_type,
            target_id=target_id,
            outcome=outcome,
            request_id=request_id,
            details=details,
            occurred_at=datetime.now(timezone.utc),
        )
        session.add(row)
        await session.commit()
        try:
            await session.refresh(row)
        except Exception:
            pass
        return row


# Sync wrappers used by existing helper/test surfaces.
record_token = upsert_token_record = lambda token, claims=None, token_kind=None, token_type_hint=None: _run(
    upsert_token_record_async(token, claims, token_kind=token_kind, token_type_hint=token_type_hint)
)
get_token_record = lambda token: _run(get_token_record_async(token))
unregister_token = lambda token: _run(remove_token_record_async(token))
revoke_token = lambda token, token_type_hint=None, reason=None: _run(
    revoke_token_async(token, token_type_hint=token_type_hint, reason=reason)
)
mark_token_used = lambda token, successor_token=None, reason="refresh_rotated": _run(
    mark_token_used_async(token, successor_token=successor_token, reason=reason)
)
revoke_refresh_family = lambda family_id, reason="refresh_token_reuse_detected", reuse_token=None: _run(
    revoke_refresh_family_async(family_id, reason=reason, reuse_token=reuse_token)
)
is_token_revoked = lambda token: bool(_run(is_token_revoked_async(token)))
introspect_token = lambda token: _run(introspect_token_async(token))
reset_token_state = lambda: _run(reset_token_state_async())
create_session = lambda **kwargs: _run(create_session_async(**kwargs))
touch_session = lambda session_id: _run(touch_session_async(session_id))
get_session = lambda session_id: _run(get_session_async(session_id))
get_active_session = lambda session_id: _run(get_active_session_async(session_id))
rotate_session_cookie_secret = lambda session_id, **kwargs: _run(rotate_session_cookie_secret_async(session_id, **kwargs))
bind_session_client = lambda session_id, **kwargs: _run(bind_session_client_async(session_id, **kwargs))
terminate_session = lambda session_id, **kwargs: _run(terminate_session_async(session_id, **kwargs))
get_latest_logout_for_session = lambda session_id: _run(get_latest_logout_for_session_async(session_id))
update_logout_metadata = lambda logout_id, **kwargs: _run(update_logout_metadata_async(logout_id, **kwargs))
mark_logout_channel = lambda logout_id, **kwargs: _run(mark_logout_channel_async(logout_id, **kwargs))
get_client_registration = lambda client_id: _run(get_client_registration_async(client_id))
record_consent = lambda **kwargs: _run(record_consent_async(**kwargs))
revoke_consent = lambda consent_id: _run(revoke_consent_async(consent_id))
upsert_client_registration = lambda **kwargs: _run(upsert_client_registration_async(**kwargs))
append_audit_event = lambda **kwargs: _run(append_audit_event_async(**kwargs))


# -----------------------------------------------------------------------------
# Operator-plane checkpoint helpers
# -----------------------------------------------------------------------------


def load_operator_records(resource: str, *, repo_root=None):
    from pathlib import Path
    from tigrbl_auth.services._operator_store import load_records

    root = Path(repo_root) if repo_root is not None else Path.cwd()
    return load_records(root, resource)


def operator_state_root(*, repo_root=None):
    from pathlib import Path
    from tigrbl_auth.services._operator_store import operator_state_root as _root

    root = Path(repo_root) if repo_root is not None else Path.cwd()
    return _root(root)


def append_operator_audit(event, *, repo_root=None):
    from pathlib import Path
    from tigrbl_auth.services._operator_store import append_jsonl, audit_log_path

    root = Path(repo_root) if repo_root is not None else Path.cwd()
    append_jsonl(audit_log_path(root), event)
    return event


__all__ = [
    "operator_state_root",
    "load_operator_records",
    "append_operator_audit",
    "append_audit_event",
    "append_audit_event_async",
    "create_session",
    "create_session_async",
    "get_token_record",
    "get_token_record_async",
    "get_session",
    "get_session_async",
    "get_active_session",
    "get_active_session_async",
    "introspect_token",
    "introspect_token_async",
    "is_token_revoked",
    "is_token_revoked_async",
    "mark_logout_channel",
    "mark_logout_channel_async",
    "record_consent",
    "record_consent_async",
    "record_token",
    "reset_token_state",
    "reset_token_state_async",
    "mark_token_used",
    "mark_token_used_async",
    "revoke_consent",
    "revoke_consent_async",
    "revoke_refresh_family",
    "revoke_refresh_family_async",
    "revoke_token",
    "revoke_token_async",
    "rotate_session_cookie_secret",
    "rotate_session_cookie_secret_async",
    "bind_session_client",
    "bind_session_client_async",
    "terminate_session",
    "terminate_session_async",
    "token_hash",
    "touch_session",
    "touch_session_async",
    "get_latest_logout_for_session",
    "get_latest_logout_for_session_async",
    "update_logout_metadata",
    "update_logout_metadata_async",
    "get_client_registration",
    "get_client_registration_async",
    "unregister_token",
    "upsert_client_registration",
    "upsert_client_registration_async",
    "upsert_token_record",
    "upsert_token_record_async",
]
