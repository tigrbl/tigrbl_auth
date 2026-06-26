"""Durable authorization invariant evaluation records."""

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


class InvariantEvaluation(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "invariant_evaluations"
    __table_args__ = ({"schema": "authn"},)

    invariant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    passed: Mapped[bool] = acol(storage=S(Boolean, nullable=False, index=True))
    message: Mapped[str] = acol(storage=S(String(2000), nullable=False))
    evaluated_at: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    evidence: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))


__all__ = ["InvariantEvaluation"]
