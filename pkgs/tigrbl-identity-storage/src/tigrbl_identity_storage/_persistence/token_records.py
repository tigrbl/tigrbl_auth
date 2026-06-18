"""Durable persistence helpers for token, session, consent, audit, and logout lifecycle state."""

from __future__ import annotations

import hashlib
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, AsyncIterator, Iterable, Mapping
from uuid import UUID

from tigrbl_identity_runtime.engine_resolver import resolve_api_provider, resolve_default_provider
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
from .uuid_coercion import normalize_uuid_filters, normalize_uuid_identifier


def _resolve_provider():
    for module_name, attr_name in (
        ("tigrbl_auth.api.surfaces", "surface_api"),
        ("tigrbl_auth.routers.surface", "surface_api"),
        ("tigrbl_auth.app", "app"),
        ("tigrbl_identity_server.api.surfaces", "surface_api"),
    ):
        try:
            module = __import__(module_name, fromlist=[attr_name])
            api = getattr(module, attr_name)
            provider = resolve_api_provider(api)
            if provider is not None:
                return provider
        except Exception:
            pass
    try:
        provider = resolve_default_provider()
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
        try:
            yield session
            commit = getattr(session, "commit", None)
            if callable(commit):
                result = commit()
                if hasattr(result, "__await__"):
                    await result
        except Exception:
            rollback = getattr(session, "rollback", None)
            if callable(rollback):
                result = rollback()
                if hasattr(result, "__await__"):
                    await result
            raise


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


def _created_item(value: Any) -> Any:
    if isinstance(value, Mapping):
        for key in ("item", "result", "data"):
            if key in value:
                return value[key]
    return value


def _list_items(result: Any) -> list[Any]:
    if isinstance(result, Mapping) and isinstance(result.get("items"), list):
        result = result["items"]
    elif hasattr(result, "items"):
        result = result.items
    if isinstance(result, list):
        return result
    if isinstance(result, tuple):
        return list(result)
    if result is None:
        return []
    return [result]


def _field(row: Any, key: str, default: Any = None) -> Any:
    if isinstance(row, Mapping):
        return row.get(key, default)
    return getattr(row, key, default)


def _record_id(row: Any) -> Any:
    return _field(row, "id")


def _value_matches(actual: Any, expected: Any) -> bool:
    if actual == expected:
        return True
    if actual is None or expected is None:
        return False
    return str(actual) == str(expected)


def _matches_filters(row: Any, filters: Mapping[str, Any]) -> bool:
    for key, expected in filters.items():
        if not _value_matches(_field(row, key), expected):
            return False
    return True


async def _list_handler_records(model: Any, db: Any, filters: Mapping[str, Any] | None = None) -> list[Any]:
    filters = normalize_uuid_filters(filters or {})
    result = await model.handlers.list.core({"payload": {"filters": filters}, "db": db})
    return [row for row in _list_items(result) if _matches_filters(row, filters)]


async def _first_handler_record(model: Any, db: Any, filters: Mapping[str, Any]) -> Any:
    rows = await _list_handler_records(model, db, filters)
    return rows[0] if rows else None


async def _read_handler_record(model: Any, db: Any, ident: Any) -> Any:
    return await model.handlers.read.core({"path_params": {"id": normalize_uuid_identifier(ident)}, "db": db})


async def _create_handler_record(model: Any, db: Any, payload: Mapping[str, Any]) -> Any:
    return _created_item(await model.handlers.create.core({"payload": dict(payload), "db": db}))


async def _update_handler_record(model: Any, db: Any, ident: Any, payload: Mapping[str, Any]) -> Any:
    return _created_item(
        await model.handlers.update.core(
            {"path_params": {"id": normalize_uuid_identifier(ident)}, "payload": dict(payload), "db": db}
        )
    )


async def _delete_handler_record(model: Any, db: Any, ident: Any) -> Any:
    return await model.handlers.delete.core({"path_params": {"id": normalize_uuid_identifier(ident)}, "db": db})


async def _clear_handler_records(model: Any, db: Any, filters: Mapping[str, Any] | None = None) -> Any:
    return await model.handlers.clear.core({"payload": {"filters": normalize_uuid_filters(filters or {})}, "db": db})


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
        async with _session() as db:
            record = await _first_handler_record(TokenRecord, db, {"token_hash": digest})
            now = datetime.now(timezone.utc)
            payload = {
                "token_hash": digest,
                "token_kind": token_kind,
                "token_type_hint": token_type_hint or _field(record, "token_type_hint") or token_kind,
                "refresh_family_id": refresh_family_id or _field(record, "refresh_family_id"),
                "refresh_parent_hash": refresh_parent_hash or _field(record, "refresh_parent_hash"),
                "refresh_successor_hash": refresh_successor_hash or _field(record, "refresh_successor_hash"),
                "active": True,
                "subject": str(claims.get("sub") or _field(record, "subject") or ""),
                "tenant_id": _to_uuid(claims.get("tid") or _field(record, "tenant_id")),
                "client_id": _to_uuid(claims.get("client_id") or claims.get("azp") or _field(record, "client_id")),
                "scope": claims.get("scope") or _field(record, "scope"),
                "issuer": claims.get("iss") or _field(record, "issuer"),
                "audience": _normalize_audience(claims.get("aud") or _field(record, "audience")),
                "claims": claims,
                "issued_at": _to_datetime(claims.get("iat")) or _field(record, "issued_at") or now,
                "expires_at": _to_datetime(claims.get("exp")) or _field(record, "expires_at"),
                "used_at": used_at or _field(record, "used_at"),
                "reuse_detected_at": reuse_detected_at or _field(record, "reuse_detected_at"),
                "revoked_at": None,
                "revoked_reason": None,
            }
            if record is None:
                await TokenRecord.persist_issued_token(
                    db,
                    token_hash=digest,
                    claims=claims,
                    token_kind=token_kind,
                    token_type_hint=payload["token_type_hint"],
                    refresh_family_id=payload["refresh_family_id"],
                    refresh_parent_hash=payload["refresh_parent_hash"],
                    refresh_successor_hash=payload["refresh_successor_hash"],
                    issued_at=payload["issued_at"],
                    expires_at=payload["expires_at"],
                    used_at=payload["used_at"],
                    reuse_detected_at=payload["reuse_detected_at"],
                )
            else:
                await TokenRecord.persist_issued_token(
                    db,
                    token_hash=digest,
                    claims=claims,
                    token_kind=token_kind,
                    token_type_hint=payload["token_type_hint"],
                    refresh_family_id=payload["refresh_family_id"],
                    refresh_parent_hash=payload["refresh_parent_hash"],
                    refresh_successor_hash=payload["refresh_successor_hash"],
                    issued_at=payload["issued_at"],
                    expires_at=payload["expires_at"],
                    used_at=payload["used_at"],
                    reuse_detected_at=payload["reuse_detected_at"],
                )
    except Exception:
        return digest
    return digest


async def remove_token_record_async(token: str) -> None:
    digest = token_hash(token)
    try:
        async with _session() as db:
            record = await _first_handler_record(TokenRecord, db, {"token_hash": digest})
            if record is not None:
                await _delete_handler_record(TokenRecord, db, _record_id(record))
    except Exception:
        return None


async def get_token_record_async(token: str) -> TokenRecord | None:
    digest = token_hash(token)
    try:
        async with _session() as db:
            return await _first_handler_record(TokenRecord, db, {"token_hash": digest})
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
        async with _session() as db:
            record = await _first_handler_record(TokenRecord, db, {"token_hash": digest})
            revoked = await _first_handler_record(RevokedToken, db, {"token_hash": digest})
            revoked_payload = {
                "token_hash": digest,
                "revoked_reason": reason or _field(revoked, "revoked_reason") or "revoked",
                "token_type_hint": token_type_hint or _field(revoked, "token_type_hint"),
            }
            if record is not None:
                await _update_handler_record(
                    TokenRecord,
                    db,
                    _record_id(record),
                    {
                        "active": False,
                        "revoked_at": now,
                        "revoked_reason": reason or _field(record, "revoked_reason") or "revoked",
                    },
                )
                revoked_payload.update(
                    {
                        "subject": _field(record, "subject"),
                        "tenant_id": _field(record, "tenant_id"),
                        "client_id": _field(record, "client_id"),
                        "expires_at": _field(record, "expires_at"),
                        "token_type_hint": token_type_hint or _field(record, "token_type_hint"),
                    }
                )
            if revoked is None:
                await RevokedToken.revoke_token(
                    db,
                    token_hash=digest,
                    token_type_hint=revoked_payload.get("token_type_hint"),
                    reason=revoked_payload.get("revoked_reason"),
                    subject=revoked_payload.get("subject"),
                    tenant_id=revoked_payload.get("tenant_id"),
                    client_id=revoked_payload.get("client_id"),
                    expires_at=revoked_payload.get("expires_at"),
                )
            else:
                await RevokedToken.revoke_token(
                    db,
                    token_hash=digest,
                    token_type_hint=revoked_payload.get("token_type_hint"),
                    reason=revoked_payload.get("revoked_reason"),
                    subject=revoked_payload.get("subject"),
                    tenant_id=revoked_payload.get("tenant_id"),
                    client_id=revoked_payload.get("client_id"),
                    expires_at=revoked_payload.get("expires_at"),
                )
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
        async with _session() as db:
            record = await _first_handler_record(TokenRecord, db, {"token_hash": digest})
            if record is None:
                return digest
            payload = {
                "used_at": now,
                "active": False,
                "revoked_at": now,
                "revoked_reason": reason,
            }
            if successor_hash:
                payload["refresh_successor_hash"] = successor_hash
            await TokenRecord.mark_rotated(
                db,
                token_hash=digest,
                successor_hash=successor_hash,
                reason=reason,
            )
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
        async with _session() as db:
            rows = await TokenRecord.revoke_family(
                db,
                refresh_family_id=family_id,
                reason=reason,
                reuse_token_hash=reuse_hash,
            )
            for row in rows:
                token_record_hash = _field(row, "token_hash")
                revoked = await _first_handler_record(RevokedToken, db, {"token_hash": token_record_hash})
                revoked_payload = {
                    "token_hash": token_record_hash,
                    "subject": _field(row, "subject"),
                    "tenant_id": _field(row, "tenant_id"),
                    "client_id": _field(row, "client_id"),
                    "expires_at": _field(row, "expires_at"),
                    "token_type_hint": _field(row, "token_type_hint"),
                    "revoked_reason": reason,
                }
                if revoked is None:
                    await RevokedToken.revoke_token(
                        db,
                        token_hash=token_record_hash,
                        token_type_hint=revoked_payload.get("token_type_hint"),
                        reason=reason,
                        subject=revoked_payload.get("subject"),
                        tenant_id=revoked_payload.get("tenant_id"),
                        client_id=revoked_payload.get("client_id"),
                        expires_at=revoked_payload.get("expires_at"),
                    )
                else:
                    await RevokedToken.revoke_token(
                        db,
                        token_hash=token_record_hash,
                        token_type_hint=revoked_payload.get("token_type_hint"),
                        reason=reason,
                        subject=revoked_payload.get("subject"),
                        tenant_id=revoked_payload.get("tenant_id"),
                        client_id=revoked_payload.get("client_id"),
                        expires_at=revoked_payload.get("expires_at"),
                    )
                revoked_count += 1
    except Exception:
        return 0
    return revoked_count


async def is_token_revoked_async(token: str) -> bool:
    digest = token_hash(token)
    try:
        async with _session() as db:
            if await RevokedToken.is_revoked(db, token_hash=digest):
                return True
            record = await _first_handler_record(TokenRecord, db, {"token_hash": digest})
            if record is None:
                return False
            if _field(record, "revoked_at") is not None:
                return True
            expires_at = _field(record, "expires_at")
            if expires_at is not None:
                expiry = expires_at if expires_at.tzinfo is not None else expires_at.replace(tzinfo=timezone.utc)
                if expiry <= datetime.now(timezone.utc):
                    return True
            return not bool(_field(record, "active"))
    except Exception:
        return False
