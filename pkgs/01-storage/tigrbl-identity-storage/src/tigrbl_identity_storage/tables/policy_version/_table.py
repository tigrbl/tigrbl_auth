"""Durable policy version records for PAP and PRP surfaces."""

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


class PolicyVersion(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "policy_versions"
    __table_args__ = ({"schema": "authn"},)

    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    policy_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    version_number: Mapped[int] = acol(storage=S(Integer, nullable=False, default=1, index=True))
    source: Mapped[str] = acol(storage=S(String(4000), nullable=False))
    source_hash: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    relation: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    context_equals: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    promoted: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=False, index=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="draft", index=True))
    version_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


__all__ = ["PolicyVersion"]
