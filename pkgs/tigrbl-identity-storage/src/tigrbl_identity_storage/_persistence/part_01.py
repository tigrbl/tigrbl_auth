"""Durable persistence helpers for token, session, consent, audit, and logout lifecycle state."""

from __future__ import annotations

import asyncio
import hashlib
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from threading import Thread
from typing import Any, AsyncIterator, Iterable
from uuid import UUID

from tigrbl_identity_server.framework import delete, select
from tigrbl_identity_runtime.engine_resolver import resolve_api_provider
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
        from tigrbl_identity_server.api.surfaces import surface_api

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


