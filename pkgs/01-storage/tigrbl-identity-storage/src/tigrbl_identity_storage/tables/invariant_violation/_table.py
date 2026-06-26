"""Durable authorization invariant violation records."""

from __future__ import annotations

from tigrbl_identity_storage.framework import (
    GUIDPk,
    JSON,
    Mapped,
    RestOltpTable,
    S,
    String,
    Timestamped,
    acol,
)


class InvariantViolation(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "invariant_violations"
    __table_args__ = ({"schema": "authn"},)

    invariant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    severity: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    message: Mapped[str] = acol(storage=S(String(2000), nullable=False))
    evidence: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))


__all__ = ["InvariantViolation"]
