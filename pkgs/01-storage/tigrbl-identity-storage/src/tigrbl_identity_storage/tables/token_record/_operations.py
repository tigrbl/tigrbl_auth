'Token-record table-owned lifecycle operations.'
from __future__ import annotations

from ._table import *  # noqa: F401,F403

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


def _to_epoch(value: dt.datetime | None) -> int | None:
    if value is None:
        return None
    normalized = (
        value if value.tzinfo is not None else value.replace(tzinfo=dt.timezone.utc)
    )
    return int(normalized.timestamp())


@op_ctx(
    bind=TokenRecord,
    alias="persist_issued",
    target="custom",
    arity="collection",
    rest=False,
)
async def persist_issued(cls: type[TokenRecord], ctx: dict[str, Any]) -> TokenRecord:
    payload = dict(ctx.get("payload") or {})
    claims = dict(payload.get("claims") or {})
    digest = payload["token_hash"]
    result = await cls.handlers.list.core(
        {"payload": {"filters": {"token_hash": digest}}, "db": ctx["db"]}
    )
    row = _items(result)[0] if _items(result) else None
    now = dt.datetime.now(dt.timezone.utc)
    record_payload = {
        "token_hash": digest,
        "jti": claims.get("jti") or _field(row, "jti"),
        "token_kind": payload.get("token_kind")
        or claims.get("kind")
        or claims.get("typ")
        or _field(row, "token_kind", "access"),
        "token_type_hint": payload.get("token_type_hint")
        or _field(row, "token_type_hint"),
        "refresh_family_id": payload.get("refresh_family_id")
        or _field(row, "refresh_family_id"),
        "refresh_parent_hash": payload.get("refresh_parent_hash")
        or _field(row, "refresh_parent_hash"),
        "refresh_successor_hash": payload.get("refresh_successor_hash")
        or _field(row, "refresh_successor_hash"),
        "active": payload.get("active")
        if payload.get("active") is not None
        else _field(row, "active", True),
        "subject": str(
            claims.get("sub")
            or payload.get("subject")
            or _field(row, "subject", "unknown")
        ),
        "tenant_id": _to_uuid(
            claims.get("tid") or payload.get("tenant_id") or _field(row, "tenant_id")
        ),
        "client_id": _to_uuid(
            claims.get("client_id")
            or claims.get("azp")
            or payload.get("client_id")
            or _field(row, "client_id")
        ),
        "scope": claims.get("scope") or payload.get("scope") or _field(row, "scope"),
        "issuer": claims.get("iss") or payload.get("issuer") or _field(row, "issuer"),
        "kid": claims.get("kid") or payload.get("kid") or _field(row, "kid"),
        "key_version": payload.get("key_version") or _field(row, "key_version"),
        "audience": claims.get("aud")
        or payload.get("audience")
        or _field(row, "audience"),
        "claims": claims or _field(row, "claims"),
        "issued_at": payload.get("issued_at")
        or _to_datetime(claims.get("iat"))
        or _field(row, "issued_at")
        or now,
        "expires_at": payload.get("expires_at")
        or _to_datetime(claims.get("exp"))
        or _field(row, "expires_at"),
        "used_at": payload.get("used_at") or _field(row, "used_at"),
        "reuse_detected_at": payload.get("reuse_detected_at")
        or _field(row, "reuse_detected_at"),
    }
    if row is None:
        return _created(
            await cls.handlers.create.core({"payload": record_payload, "db": ctx["db"]})
        )
    return _created(
        await cls.handlers.update.core(
            {
                "path_params": {"id": _field(row, "id")},
                "payload": record_payload,
                "db": ctx["db"],
            }
        )
    )


@op_ctx(
    bind=TokenRecord,
    alias="mark_rotated",
    target="custom",
    arity="collection",
    rest=False,
)
async def mark_rotated(
    cls: type[TokenRecord], ctx: dict[str, Any]
) -> TokenRecord | None:
    payload = dict(ctx.get("payload") or {})
    result = await cls.handlers.list.core(
        {"payload": {"filters": {"token_hash": payload["token_hash"]}}, "db": ctx["db"]}
    )
    row = _items(result)[0] if _items(result) else None
    if row is None:
        return None
    return _created(
        await cls.handlers.update.core(
            {
                "path_params": {"id": _field(row, "id")},
                "payload": {
                    "active": False,
                    "used_at": payload.get("used_at")
                    or dt.datetime.now(dt.timezone.utc),
                    "refresh_successor_hash": payload.get("successor_hash"),
                    "revoked_reason": payload.get("reason")
                    or _field(row, "revoked_reason")
                    or "refresh_rotated",
                },
                "db": ctx["db"],
            }
        )
    )


@op_ctx(
    bind=TokenRecord,
    alias="revoke_family",
    target="custom",
    arity="collection",
    rest=False,
)
async def revoke_family(
    cls: type[TokenRecord], ctx: dict[str, Any]
) -> list[TokenRecord]:
    payload = dict(ctx.get("payload") or {})
    family_id = payload["refresh_family_id"]
    rows = _items(
        await cls.handlers.list.core(
            {"payload": {"filters": {"refresh_family_id": family_id}}, "db": ctx["db"]}
        )
    )
    now = dt.datetime.now(dt.timezone.utc)
    updated: list[TokenRecord] = []
    for row in rows:
        update_payload = {
            "active": False,
            "revoked_at": _field(row, "revoked_at") or now,
            "revoked_reason": payload.get("reason")
            or _field(row, "revoked_reason")
            or "refresh_family_revoked",
        }
        if (
            payload.get("reuse_token_hash")
            and _field(row, "token_hash") == payload["reuse_token_hash"]
        ):
            update_payload["reuse_detected_at"] = (
                _field(row, "reuse_detected_at") or now
            )
        updated.append(
            _created(
                await cls.handlers.update.core(
                    {
                        "path_params": {"id": _field(row, "id")},
                        "payload": update_payload,
                        "db": ctx["db"],
                    }
                )
            )
        )
    return updated


@op_ctx(
    bind=TokenRecord,
    alias="introspect",
    target="custom",
    arity="collection",
    rest=False,
)
async def introspect(cls: type[TokenRecord], ctx: dict[str, Any]) -> dict[str, Any]:
    payload = dict(ctx.get("payload") or {})
    digest = payload.get("token_hash") or token_hash(payload["token"])
    now = dt.datetime.now(dt.timezone.utc)
    rows = _items(
        await cls.handlers.list.core(
            {"payload": {"filters": {"token_hash": digest}}, "db": ctx["db"]}
        )
    )
    row = rows[0] if rows else None
    if row is None:
        return {"active": False}
    expires_at = _field(row, "expires_at")
    if expires_at is not None:
        expiry = (
            expires_at
            if expires_at.tzinfo is not None
            else expires_at.replace(tzinfo=dt.timezone.utc)
        )
        if expiry <= now:
            await cls.handlers.update.core(
                {
                    "path_params": {"id": _field(row, "id")},
                    "payload": {"active": False, "revoked_reason": "expired"},
                    "db": ctx["db"],
                }
            )
            return {"active": False}
    if _field(row, "revoked_at") is not None or not bool(_field(row, "active")):
        await cls.handlers.update.core(
            {
                "path_params": {"id": _field(row, "id")},
                "payload": {"active": False, "last_introspected_at": now},
                "db": ctx["db"],
            }
        )
        return {"active": False}
    await cls.handlers.update.core(
        {
            "path_params": {"id": _field(row, "id")},
            "payload": {"last_introspected_at": now},
            "db": ctx["db"],
        }
    )
    response = dict(_field(row, "claims") or {})
    response.setdefault("sub", _field(row, "subject"))
    if _field(row, "scope"):
        response.setdefault("scope", _field(row, "scope"))
    if _field(row, "client_id") is not None:
        response.setdefault("client_id", str(_field(row, "client_id")))
    if _field(row, "issuer"):
        response.setdefault("iss", _field(row, "issuer"))
    exp = _to_epoch(expires_at)
    if exp is not None:
        response.setdefault("exp", exp)
    response["active"] = True
    return response


__all__ = [
    "AuthorizationCodeGrantForm",
    "IntrospectOut",
    "PasswordGrantForm",
    "RefreshIn",
    "TokenPair",
    "TokenRecord",
]
