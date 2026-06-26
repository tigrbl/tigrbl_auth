"""Durable federated login session records."""

from __future__ import annotations

from tigrbl_identity_storage.framework import (
    Boolean,
    GUIDPk,
    JSON,
    Mapped,
    RestOltpTable,
    S,
    String,
    Timestamped,
    acol,
)


class FederatedSession(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "federated_sessions"
    __table_args__ = ({"schema": "authn"},)

    session_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    provider_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    issuer: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    audience: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    logout_supported: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=False, index=True))
    normalized_claims: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))
    bound_at: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))


__all__ = ["FederatedSession"]
