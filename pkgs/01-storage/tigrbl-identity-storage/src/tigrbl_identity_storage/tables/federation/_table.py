"""Durable federation registry records."""

from __future__ import annotations

from tigrbl_identity_storage.framework import (
    Boolean,
    GUIDPk,
    Integer,
    JSON,
    Mapped,
    RestOltpTable,
    S,
    String,
    Timestamped,
    acol,
)


class Federation(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "federations"
    __table_args__ = ({"schema": "authn"},)

    federation_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    issuer: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    discovery_url: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    audience: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    logout_supported: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=False, index=True))
    display_name: Mapped[str] = acol(storage=S(String(255), nullable=False))
    claim_mapping: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))
    scopes: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))
    key_set_version: Mapped[int] = acol(storage=S(Integer, nullable=False, default=1))
    enabled: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=True, index=True))


__all__ = ["Federation"]
