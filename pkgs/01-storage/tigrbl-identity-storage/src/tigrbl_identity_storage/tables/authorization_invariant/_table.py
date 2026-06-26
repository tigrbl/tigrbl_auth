"""Durable authorization invariant definitions."""

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


class AuthorizationInvariant(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "authorization_invariants"
    __table_args__ = ({"schema": "authn"},)

    invariant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    title: Mapped[str] = acol(storage=S(String(255), nullable=False))
    property_family: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    statement: Mapped[str] = acol(storage=S(String(2000), nullable=False))
    verification_method: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    severity: Mapped[str] = acol(storage=S(String(64), nullable=False, default="error", index=True))
    enabled: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=True, index=True))
    feature_ids: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))
    spec_ids: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))
    tags: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))


__all__ = ["AuthorizationInvariant"]
