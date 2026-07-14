"""Durable DPoP nonce ledger."""

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
)


class DpopNonce(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "dpop_nonces"
    __table_args__ = ({"schema": "authn"},)

    nonce_hash: Mapped[str] = acol(storage=S(String(64), nullable=False, unique=True, index=True))
    issued_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False, index=True))
    expires_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False, index=True))
    consumed_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    client_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    authorization_server_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    resource_server_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    jkt: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))


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


def nonce_hash(nonce: str) -> str:
    return hashlib.sha256(str(nonce).strip().encode("utf-8")).hexdigest()


def nonce_payload(
    *,
    nonce: str,
    issued_at: dt.datetime,
    expires_at: dt.datetime,
    consumed_at: dt.datetime | None = None,
    client_id: str | None = None,
    authorization_server_id: str | None = None,
    resource_server_id: str | None = None,
    jkt: str | None = None,
) -> dict[str, Any]:
    return {
        "nonce_hash": nonce_hash(nonce),
        "issued_at": _as_aware(issued_at),
        "expires_at": _as_aware(expires_at),
        "consumed_at": _as_aware(consumed_at) if consumed_at is not None else None,
        "client_id": str(client_id).strip() if client_id not in {None, ""} else None,
        "authorization_server_id": (
            str(authorization_server_id).strip() if authorization_server_id not in {None, ""} else None
        ),
        "resource_server_id": str(resource_server_id).strip() if resource_server_id not in {None, ""} else None,
        "jkt": str(jkt).strip() if jkt not in {None, ""} else None,
    }


__all__ = ["DpopNonce", "nonce_hash", "nonce_payload"]
