"""Table-owned operator activity log."""

from __future__ import annotations

from tigrbl_identity_storage.framework import (
    RestOltpTable,
    Integer,
    Mapped,
    S,
    String,
    acol,
)


class OperatorActivity(RestOltpTable):
    __tablename__ = "operator_activity"

    id: Mapped[int] = acol(
        storage=S(Integer, primary_key=True, autoincrement=True, nullable=False)
    )
    ts: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    kind: Mapped[str] = acol(storage=S(String(255), nullable=False))
    resource: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    record_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    status: Mapped[str | None] = acol(storage=S(String(64), nullable=True))
    transaction_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True))


__all__ = ["OperatorActivity"]
