"""TokenRecord-owned operation surface."""

from __future__ import annotations

from importlib import import_module
from types import ModuleType
from typing import Any

from . import _introspection
from . import _persistence
from . import _records

_BASE_MODULES = (_persistence, _records, _introspection)
_runtime: ModuleType | None = None
_request: ModuleType | None = None


def _export_module(module: ModuleType, *, skip: set[str] | None = None) -> None:
    skipped = skip or set()
    globals().update(
        {
            name: value
            for name, value in module.__dict__.items()
            if not name.startswith("__") and name not in skipped
        }
    )


for _module in _BASE_MODULES:
    _export_module(_module)


def _load_runtime_modules() -> tuple[ModuleType, ModuleType]:
    global _runtime, _request
    if _runtime is None or _request is None:
        runtime_module = import_module(f"{__name__}._runtime")
        request_module = import_module(f"{__name__}._request")
        _runtime = runtime_module
        _request = request_module
        _export_module(_runtime, skip={"_load_client"})
    return _runtime, _request


def _iter_sync_names() -> tuple[str, ...]:
    modules = list(_BASE_MODULES)
    if _runtime is not None:
        modules.append(_runtime)
    return tuple(
        name
        for module in modules
        for name in module.__dict__
        if not name.startswith("__")
    )


def _sync_request_runtime() -> None:
    runtime, request = _load_runtime_modules()
    for name in _iter_sync_names():
        if name not in globals():
            continue
        if name == "_load_client" and globals()[name] is _LOAD_CLIENT_WRAPPER:
            continue
        for module in (runtime, request):
            if hasattr(module, name):
                setattr(module, name, globals()[name])


async def _load_client(db: Any, client_id: str):
    runtime, _ = _load_runtime_modules()
    _sync_request_runtime()
    return await runtime._load_client(db, client_id)


_LOAD_CLIENT_WRAPPER = _load_client


async def token_request(*, request, db):
    _, request_module = _load_runtime_modules()
    _sync_request_runtime()
    return await request_module.token_request(request=request, db=db)


def __getattr__(name: str) -> Any:
    runtime, request = _load_runtime_modules()
    for module in (runtime, request):
        if hasattr(module, name):
            value = getattr(module, name)
            if name != "_load_client":
                globals()[name] = value
            return value
    raise AttributeError(f"{__name__!r} has no attribute {name!r}")


__all__ = sorted(
    {
        *_persistence.__all__,
        *_records.__all__,
        *_introspection.__all__,
        "_load_client",
        "token_request",
    }
)

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from .. import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

@_table_op_ctx(bind=TokenRecord, alias="persist_issued_token", target="custom", rest=False)
async def persist_issued_token(
    cls,
    db: Any,
    *,
    token_hash: str,
    claims: dict[str, Any] | None = None,
    token_kind: str = "access",
    token_type_hint: str | None = None,
    refresh_family_id: str | None = None,
    refresh_parent_hash: str | None = None,
    refresh_successor_hash: str | None = None,
    **overrides: Any,
) -> "TokenRecord":
    claims = dict(claims or {})
    existing = await first_record(cls, db, {"token_hash": token_hash})
    payload = {
        "token_hash": token_hash,
        "jti": claims.get("jti") or overrides.pop("jti", None) or field(existing, "jti"),
        "token_kind": token_kind,
        "token_type_hint": token_type_hint or field(existing, "token_type_hint") or token_kind,
        "token_status": overrides.pop("token_status", None) or "active",
        "refresh_family_id": refresh_family_id or field(existing, "refresh_family_id"),
        "refresh_parent_hash": refresh_parent_hash or field(existing, "refresh_parent_hash"),
        "refresh_successor_hash": refresh_successor_hash or field(existing, "refresh_successor_hash"),
        "active": True,
        "subject": str(claims.get("sub") or field(existing, "subject") or ""),
        "tenant_id": _to_uuid(claims.get("tid") or field(existing, "tenant_id")),
        "client_id": _to_uuid(claims.get("client_id") or claims.get("azp") or field(existing, "client_id")),
        "scope": claims.get("scope") or field(existing, "scope"),
        "issuer": claims.get("iss") or field(existing, "issuer"),
        "kid": claims.get("kid") or overrides.pop("kid", None) or field(existing, "kid"),
        "key_version": overrides.pop("key_version", None) or claims.get("key_version") or field(existing, "key_version"),
        "audience": claims.get("aud") or field(existing, "audience"),
        "claims": claims,
        "issued_at": _to_datetime(overrides.pop("issued_at", None) or claims.get("iat")) or field(existing, "issued_at") or utc_now(),
        "expires_at": _to_datetime(overrides.pop("expires_at", None) or claims.get("exp")) or field(existing, "expires_at"),
        "used_at": overrides.pop("used_at", None) or field(existing, "used_at"),
        "reuse_detected_at": overrides.pop("reuse_detected_at", None) or field(existing, "reuse_detected_at"),
        "revoked_at": None,
        "revoked_reason": None,
    }
    payload.update(overrides)
    if existing is None:
        return await create_record(cls, db, payload)
    return await update_record(cls, db, record_id(existing), payload)

@_table_op_ctx(bind=TokenRecord, alias="list_active_for_subject", target="custom", rest=False)
async def list_active_for_subject(
    cls,
    db: Any,
    *,
    subject: str,
    tenant_id: uuid.UUID | None = None,
    token_kind: str | None = None,
) -> list["TokenRecord"]:
    filters: dict[str, Any] = {"subject": subject}
    if tenant_id is not None:
        filters["tenant_id"] = tenant_id
    if token_kind is not None:
        filters["token_kind"] = token_kind
    now = utc_now()
    return [
        row
        for row in await list_records(cls, db, filters)
        if field(row, "active", True)
        and field(row, "token_status", "active") == "active"
        and field(row, "revoked_at") is None
        and (field(row, "expires_at") is None or field(row, "expires_at") > now)
    ]

@_table_op_ctx(bind=TokenRecord, alias="revoke_family", target="custom", rest=False)
async def revoke_family(
    cls,
    db: Any,
    *,
    refresh_family_id: str,
    reason: str = "refresh_token_reuse_detected",
    reuse_token_hash: str | None = None,
) -> list["TokenRecord"]:
    revoked = []
    now = utc_now()
    for row in await list_records(cls, db, {"refresh_family_id": refresh_family_id}):
        payload = {
            "active": False,
            "token_status": "revoked",
            "revoked_at": field(row, "revoked_at") or now,
            "revoked_reason": reason,
        }
        if reuse_token_hash and field(row, "token_hash") == reuse_token_hash:
            payload["reuse_detected_at"] = now
        revoked.append(await update_record(cls, db, record_id(row), payload))
    return revoked

@_table_op_ctx(bind=TokenRecord, alias="mark_rotated", target="custom", rest=False)
async def mark_rotated(
    cls,
    db: Any,
    *,
    token_hash: str,
    successor_hash: str | None = None,
    reason: str = "refresh_rotated",
) -> "TokenRecord | None":
    row = await first_record(cls, db, {"token_hash": token_hash})
    if row is None:
        return None
    payload = {
        "used_at": utc_now(),
        "active": False,
        "token_status": "rotated",
        "revoked_at": utc_now(),
        "revoked_reason": reason,
    }
    if successor_hash:
        payload["refresh_successor_hash"] = successor_hash
    return await update_record(cls, db, record_id(row), payload)

# END classmethod-to-op_ctx migration
