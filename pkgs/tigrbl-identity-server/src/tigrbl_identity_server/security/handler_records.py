from __future__ import annotations

import hashlib
from collections.abc import Mapping
from copy import deepcopy
from datetime import datetime, timezone
import inspect
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy.exc import NoResultFound

from tigrbl_identity_runtime.http_standards.cookies import (
    extract_session_cookie,
    hash_cookie_secret,
    new_session_cookie_secret,
    new_session_state_salt,
    parse_session_cookie_value,
)
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_storage.tables import AuditEvent, AuthSession, TokenRecord

def _created_item(value: Any) -> Any:
    if isinstance(value, dict):
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

def _value_matches(actual: Any, expected: Any) -> bool:
    if actual == expected:
        return True
    if actual is None or expected is None:
        return False
    return str(actual) == str(expected)

def _matches_filters(row: Any, filters: Mapping[str, Any]) -> bool:
    for key, expected in filters.items():
        if not hasattr(row, key):
            continue
        if not _value_matches(getattr(row, key, None), expected):
            return False
    return True

def _utc(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)


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


async def first_handler_record(model: Any, db: Any, filters: Mapping[str, Any]) -> Any:
    rows = await model.handlers.list.core({"payload": {"filters": dict(filters)}, "db": db})
    for row in _list_items(rows):
        if _matches_filters(row, filters):
            return row
    return None


async def list_handler_records(model: Any, db: Any, filters: Mapping[str, Any] | None = None) -> list[Any]:
    filters = dict(filters or {})
    rows = await model.handlers.list.core({"payload": {"filters": filters}, "db": db})
    return [row for row in _list_items(rows) if _matches_filters(row, filters)]


async def read_handler_record(model: Any, db: Any, ident: Any) -> Any:
    get = getattr(db, "get", None)
    if callable(get):
        try:
            row = get(model, ident)
            if inspect.isawaitable(row):
                row = await row
            if row is not None:
                return row
        except Exception:
            pass
    try:
        return await model.handlers.read.core({"path_params": {"id": ident}, "db": db})
    except NoResultFound:
        return None


async def create_handler_record(model: Any, db: Any, payload: Mapping[str, Any]) -> Any:
    row = await model.handlers.create.core({"payload": dict(payload), "db": db})
    return _created_item(row)


async def update_handler_record(model: Any, db: Any, ident: Any, payload: Mapping[str, Any]) -> Any:
    get = getattr(db, "get", None)
    if callable(get):
        try:
            row = get(model, ident)
            if inspect.isawaitable(row):
                row = await row
            if row is not None:
                for key, value in payload.items():
                    if hasattr(row, key):
                        setattr(row, key, value)
                flush = getattr(db, "flush", None)
                if callable(flush):
                    flushed = flush()
                    if inspect.isawaitable(flushed):
                        await flushed
                return row
        except Exception:
            pass
    row = await model.handlers.update.core({"path_params": {"id": ident}, "payload": dict(payload), "db": db})
    return _created_item(row)


async def delete_handler_record(model: Any, db: Any, ident: Any) -> Any:
    get = getattr(db, "get", None)
    delete = getattr(db, "delete", None)
    if callable(get) and callable(delete):
        try:
            row = get(model, ident)
            if inspect.isawaitable(row):
                row = await row
            if row is not None:
                deleted = delete(row)
                if inspect.isawaitable(deleted):
                    await deleted
                flush = getattr(db, "flush", None)
                if callable(flush):
                    flushed = flush()
                    if inspect.isawaitable(flushed):
                        await flushed
                return row
        except Exception:
            pass
    return await model.handlers.delete.core({"path_params": {"id": ident}, "db": db})


def _token_record_payload(
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
) -> dict[str, Any]:
    claims = dict(claims or {})
    now = datetime.now(timezone.utc)
    effective_kind = token_kind or str(claims.get("kind") or claims.get("typ") or "access")
    return {
        "token_hash": token_hash(token),
        "token_kind": effective_kind,
        "token_type_hint": token_type_hint or effective_kind,
        "refresh_family_id": refresh_family_id,
        "refresh_parent_hash": refresh_parent_hash,
        "refresh_successor_hash": refresh_successor_hash,
        "active": True,
        "subject": str(claims.get("sub") or ""),
        "tenant_id": _to_uuid(claims.get("tid")),
        "client_id": _to_uuid(claims.get("client_id") or claims.get("azp")),
        "scope": claims.get("scope"),
        "issuer": claims.get("iss"),
        "audience": _normalize_audience(claims.get("aud")),
        "claims": claims,
        "issued_at": _to_datetime(claims.get("iat")) or now,
        "expires_at": _to_datetime(claims.get("exp")),
        "last_introspected_at": None,
        "used_at": used_at,
        "reuse_detected_at": reuse_detected_at,
        "revoked_at": None,
        "revoked_reason": None,
    }


async def create_browser_session_record(
    db: Any,
    *,
    user_id: UUID,
    tenant_id: UUID,
    username: str,
    client_id: UUID | None = None,
    expires_at: datetime | None = None,
) -> tuple[Any, str]:
    secret = new_session_cookie_secret()
    now = datetime.now(timezone.utc)
    row = await AuthSession.handlers.create.core(
        {
            "payload": {
                "user_id": user_id,
                "tenant_id": tenant_id,
                "username": username,
                "client_id": client_id,
                "auth_time": now,
                "session_state": "active",
                "session_state_salt": new_session_state_salt(),
                "cookie_secret_hash": hash_cookie_secret(secret),
                "cookie_issued_at": now,
                "cookie_rotated_at": now,
                "expires_at": expires_at,
                "last_seen_at": now,
            },
            "db": db,
        }
    )
    return _created_item(row), secret


async def resolve_browser_session_record(db: Any, request: Any, *, deployment: Any) -> Any:
    if not deployment.flag_enabled("enable_oidc_session_management"):
        return None
    parsed = parse_session_cookie_value(extract_session_cookie(request))
    if parsed is None:
        return None
    row = await read_handler_record(AuthSession, db, parsed.session_id)
    if row is None:
        return None
    if getattr(row, "ended_at", None) is not None or str(getattr(row, "session_state", "")).lower() in {
        "terminated",
        "ended",
        "revoked",
    }:
        return None
    now = datetime.now(timezone.utc)
    expires_at = _utc(getattr(row, "expires_at", None))
    if expires_at is not None and expires_at <= now:
        await update_handler_record(AuthSession, db, row.id, {"session_state": "expired", "ended_at": now})
        return None
    if parsed.secret:
        if not getattr(row, "cookie_secret_hash", None) or row.cookie_secret_hash != hash_cookie_secret(parsed.secret):
            return None
    await update_handler_record(AuthSession, db, row.id, {"last_seen_at": now})
    row.last_seen_at = now
    return row


async def bind_browser_session_client_record(db: Any, session_id: UUID, *, client_id: UUID | None) -> Any:
    return await update_handler_record(
        AuthSession,
        db,
        session_id,
        {"client_id": client_id, "last_seen_at": datetime.now(timezone.utc)},
    )


async def maybe_rotate_browser_session_cookie_record(db: Any, session_row: Any) -> str | None:
    if session_row is None:
        return None
    renewal_seconds = max(int(settings.session_cookie_renewal_seconds), 60)
    now = datetime.now(timezone.utc)
    rotated_at = _utc(getattr(session_row, "cookie_rotated_at", None)) or _utc(getattr(session_row, "cookie_issued_at", None))
    if rotated_at is not None and (now - rotated_at).total_seconds() < renewal_seconds:
        return None
    secret = new_session_cookie_secret()
    payload = {
        "cookie_secret_hash": hash_cookie_secret(secret),
        "cookie_rotated_at": now,
        "cookie_issued_at": getattr(session_row, "cookie_issued_at", None) or now,
        "last_seen_at": now,
    }
    await update_handler_record(AuthSession, db, session_row.id, payload)
    session_row.cookie_secret_hash = payload["cookie_secret_hash"]
    session_row.cookie_rotated_at = now
    session_row.cookie_issued_at = payload["cookie_issued_at"]
    session_row.last_seen_at = now
    return secret


async def create_token_record(db: Any, token: str, claims: dict[str, Any] | None = None, **kwargs: Any) -> Any:
    row = await TokenRecord.handlers.create.core(
        {
            "payload": _token_record_payload(token, claims, **kwargs),
            "db": db,
        }
    )
    return _created_item(row)


async def issue_token_pair_records(
    db: Any,
    *,
    jwt: Any,
    sub: str,
    tid: str,
    client_id: str | None,
    cert_thumbprint: str | None = None,
    refresh_family_id: str | None = None,
    refresh_parent_token: str | None = None,
    authorization_trace: dict[str, Any] | None = None,
    delegation_provenance: dict[str, Any] | None = None,
    **extra: Any,
) -> tuple[str, str]:
    access_token, refresh_token = await jwt.async_sign_pair(
        sub=sub,
        tid=tid,
        cert_thumbprint=cert_thumbprint,
        persist_token=False,
        **extra,
    )
    access_claims = await jwt.async_decode(access_token, verify_exp=False)
    refresh_claims = await jwt.async_decode(refresh_token, verify_exp=False)
    if authorization_trace is not None:
        access_claims["authorization_trace"] = deepcopy(authorization_trace)
        refresh_claims["authorization_trace"] = deepcopy(authorization_trace)
    if delegation_provenance is not None:
        access_claims["delegation_provenance"] = deepcopy(delegation_provenance)
        refresh_claims["delegation_provenance"] = deepcopy(delegation_provenance)
    if client_id:
        access_claims["client_id"] = client_id
        refresh_claims["client_id"] = client_id
    family_id = refresh_family_id or str(uuid4())
    refresh_parent_hash = token_hash(refresh_parent_token) if refresh_parent_token else None
    await create_token_record(
        db,
        access_token,
        access_claims,
        token_kind="access",
        token_type_hint="access_token",
        refresh_family_id=family_id,
        refresh_parent_hash=refresh_parent_hash,
    )
    await create_token_record(
        db,
        refresh_token,
        refresh_claims,
        token_kind="refresh",
        token_type_hint="refresh_token",
        refresh_family_id=family_id,
        refresh_parent_hash=refresh_parent_hash,
    )
    return access_token, refresh_token


async def append_audit_event_record(db: Any, **payload: Any) -> Any:
    row = await AuditEvent.handlers.create.core({"payload": payload, "db": db})
    return _created_item(row)


__all__ = [
    "append_audit_event_record",
    "bind_browser_session_client_record",
    "create_browser_session_record",
    "create_handler_record",
    "create_token_record",
    "delete_handler_record",
    "first_handler_record",
    "issue_token_pair_records",
    "list_handler_records",
    "maybe_rotate_browser_session_cookie_record",
    "read_handler_record",
    "resolve_browser_session_record",
    "token_hash",
    "update_handler_record",
]
