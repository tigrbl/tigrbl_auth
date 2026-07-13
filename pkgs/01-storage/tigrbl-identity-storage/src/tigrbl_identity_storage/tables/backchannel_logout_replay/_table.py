"""Durable OpenID Connect Back-Channel Logout replay ledger schema."""

from __future__ import annotations

import datetime as dt

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


class BackchannelLogoutReplay(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "backchannel_logout_replays"
    __table_args__ = ({"schema": "authn"},)

    replay_key: Mapped[str] = acol(
        storage=S(String(64), nullable=False, unique=True, index=True)
    )
    jti: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    issuer: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    client_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    seen_at: Mapped[dt.datetime] = acol(
        storage=S(TZDateTime, nullable=False, index=True)
    )
    expires_at: Mapped[dt.datetime] = acol(
        storage=S(TZDateTime, nullable=False, index=True)
    )


__all__ = ["BackchannelLogoutReplay"]
