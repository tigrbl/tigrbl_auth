"""Durable advanced-authentication challenge records."""

from __future__ import annotations

import datetime as dt

from tigrbl_identity_storage.framework import (
    Boolean,
    GUIDPk,
    JSON,
    Mapped,
    RestOltpTable,
    S,
    String,
    TZDateTime,
    Timestamped,
    acol,
)


class AuthenticationChallenge(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "authentication_challenges"
    __table_args__ = {"extend_existing": True, "schema": "authn"}

    challenge_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    subject_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    challenge_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    expected_nonce: Mapped[str] = acol(storage=S(String(255), nullable=False))
    issued_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False, index=True))
    expires_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False, index=True))
    allowed_methods: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    step_up_required: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=False, index=True))
    bound_credential_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    consumed: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=False, index=True))


__all__ = ["AuthenticationChallenge"]
