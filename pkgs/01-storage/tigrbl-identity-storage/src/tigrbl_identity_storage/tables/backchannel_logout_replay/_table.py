"""Durable OpenID Connect Back-Channel Logout replay ledger."""

from __future__ import annotations

import datetime as dt
import hashlib
from datetime import timezone
from typing import Any

from tigrbl_identity_storage.framework import (
    GUIDPk,
    Mapped,
    RestOltpTable,
    S,
    String,
    TZDateTime,
    Timestamped,
    acol,
    op_ctx,
)


class BackchannelLogoutReplay(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "backchannel_logout_replays"
    __table_args__ = ({"schema": "authn"},)

    replay_key: Mapped[str] = acol(storage=S(String(64), nullable=False, unique=True, index=True))
    jti: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    issuer: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    client_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    seen_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False, index=True))
    expires_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False, index=True))


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
    if isinstance(row, dict):
        return row.get(key, default)
    return getattr(row, key, default)


def _record_id(row: Any) -> Any:
    return _field(row, "id")


def _as_aware(value: Any) -> dt.datetime:
    if isinstance(value, dt.datetime):
        parsed = value
    elif isinstance(value, (int, float)):
        parsed = dt.datetime.fromtimestamp(value, tz=timezone.utc)
    else:
        parsed = dt.datetime.fromisoformat(str(value))
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def replay_key(*, issuer: str, client_id: str, jti: str) -> str:
    material = f"{issuer.strip()}\x1f{client_id.strip()}\x1f{jti.strip()}".encode("utf-8")
    return hashlib.sha256(material).hexdigest()


@op_ctx(
    bind=BackchannelLogoutReplay,
    alias="register",
    target="custom",
    arity="collection",
    rest=False,
)
async def register(cls: type[BackchannelLogoutReplay], ctx: dict[str, Any]) -> BackchannelLogoutReplay:
    payload = dict(ctx.get("payload") or {})
    db = ctx["db"]
    jti = str(payload["jti"]).strip()
    issuer = str(payload["issuer"]).strip()
    client_id = str(payload["client_id"]).strip()
    now = _as_aware(payload.get("now") or dt.datetime.now(timezone.utc))
    expires_at = _as_aware(payload["expires_at"])
    key = replay_key(issuer=issuer, client_id=client_id, jti=jti)

    rows = _items(await cls.handlers.list.core({"payload": {}, "db": db}))
    for row in rows:
        row_expires_at = _as_aware(_field(row, "expires_at"))
        if row_expires_at <= now:
            await cls.handlers.delete.core({"path_params": {"id": _record_id(row)}, "db": db})
            continue
        if _field(row, "replay_key") == key:
            raise ValueError("replayed logout token")

    return _created(
        await cls.handlers.create.core(
            {
                "payload": {
                    "replay_key": key,
                    "jti": jti,
                    "issuer": issuer,
                    "client_id": client_id,
                    "seen_at": now,
                    "expires_at": expires_at,
                },
                "db": db,
            }
        )
    )


__all__ = ["BackchannelLogoutReplay", "replay_key"]
