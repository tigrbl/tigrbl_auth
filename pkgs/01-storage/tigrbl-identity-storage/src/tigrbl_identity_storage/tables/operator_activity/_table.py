"""Table-owned operator activity log."""

from __future__ import annotations

from typing import Any, Mapping

from tigrbl_identity_storage.framework import RestOltpTable, Integer, Mapped, S, String, acol

from .._ops import create_record, field, list_records


class OperatorActivity(RestOltpTable):
    __tablename__ = "operator_activity"

    id: Mapped[int] = acol(storage=S(Integer, primary_key=True, autoincrement=True, nullable=False))
    ts: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    kind: Mapped[str] = acol(storage=S(String(255), nullable=False))
    resource: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    record_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    status: Mapped[str | None] = acol(storage=S(String(64), nullable=True))
    transaction_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True))

    @classmethod
    async def record_activity(cls, db: Any, payload: Mapping[str, Any]) -> "OperatorActivity":
        return await create_record(
            cls,
            db,
            {
                "ts": payload.get("ts"),
                "kind": payload.get("kind"),
                "resource": payload.get("resource"),
                "record_id": payload.get("id") or payload.get("record_id"),
                "status": payload.get("status"),
                "transaction_id": payload.get("transaction_id"),
            },
        )

    @classmethod
    async def list_activity(cls, db: Any) -> list[dict[str, Any]]:
        rows = await list_records(cls, db)
        return [
            {
                "seq": int(field(row, "id") or 0),
                "ts": field(row, "ts"),
                "kind": field(row, "kind"),
                "resource": field(row, "resource"),
                "id": field(row, "record_id"),
                "status": field(row, "status"),
                "transaction_id": field(row, "transaction_id"),
            }
            for row in sorted(rows, key=lambda item: int(field(item, "id") or 0))
        ]


__all__ = ["OperatorActivity"]
