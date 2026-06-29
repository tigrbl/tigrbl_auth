"""Durable DPoP replay ledger."""

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


class DpopReplay(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "dpop_replays"
    __table_args__ = ({"schema": "authn"},)

    replay_key: Mapped[str] = acol(storage=S(String(64), nullable=False, unique=True, index=True))
    jkt: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    jti: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    htm: Mapped[str] = acol(storage=S(String(16), nullable=False, index=True))
    htu: Mapped[str] = acol(storage=S(String(2000), nullable=False, index=True))
    ath: Mapped[str | None] = acol(storage=S(String(512), nullable=True, index=True))
    proof_iat: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False, index=True))
    first_seen_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False, index=True))
    expires_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False, index=True))


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


def replay_key(*, jkt: str, jti: str, htm: str, htu: str, ath: str | None = None) -> str:
    material = "\x1f".join(
        (
            str(jkt).strip(),
            str(jti).strip(),
            str(htm).upper().strip(),
            str(htu).strip(),
            str(ath or "").strip(),
        )
    ).encode("utf-8")
    return hashlib.sha256(material).hexdigest()


def replay_payload(
    *,
    jkt: str,
    jti: str,
    htm: str,
    htu: str,
    ath: str | None,
    proof_iat: dt.datetime | int | float,
    first_seen_at: dt.datetime,
    expires_at: dt.datetime,
) -> dict[str, Any]:
    normalized_jkt = str(jkt).strip()
    normalized_jti = str(jti).strip()
    normalized_htm = str(htm).upper().strip()
    normalized_htu = str(htu).strip()
    normalized_ath = str(ath).strip() if ath not in {None, ""} else None
    return {
        "replay_key": replay_key(
            jkt=normalized_jkt,
            jti=normalized_jti,
            htm=normalized_htm,
            htu=normalized_htu,
            ath=normalized_ath,
        ),
        "jkt": normalized_jkt,
        "jti": normalized_jti,
        "htm": normalized_htm,
        "htu": normalized_htu,
        "ath": normalized_ath,
        "proof_iat": _as_aware(proof_iat),
        "first_seen_at": _as_aware(first_seen_at),
        "expires_at": _as_aware(expires_at),
    }


__all__ = ["DpopReplay", "replay_key", "replay_payload"]
