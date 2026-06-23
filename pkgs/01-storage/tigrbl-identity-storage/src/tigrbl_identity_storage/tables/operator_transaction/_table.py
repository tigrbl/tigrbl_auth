"""Table-owned operator transaction log."""

from __future__ import annotations

import json
from typing import Any, Mapping

from tigrbl_identity_storage.framework import RestOltpTable, Mapped, S, String, acol

from .._ops import create_record, field, list_records


class OperatorTransaction(RestOltpTable):
    __tablename__ = "operator_transactions"

    transaction_id: Mapped[str] = acol(storage=S(String(255), primary_key=True, nullable=False))
    ts: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    command: Mapped[str] = acol(storage=S(String(255), nullable=False))
    resource: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    status: Mapped[str] = acol(storage=S(String(64), nullable=False))
    record_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    changed_ids_json: Mapped[str] = acol(storage=S(String(8000), nullable=False, default="[]"))
    summary_json: Mapped[str] = acol(storage=S(String(20000), nullable=False, default="{}"))
    actor: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    profile: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    tenant: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    issuer: Mapped[str | None] = acol(storage=S(String(512), nullable=True))
    before_checksum: Mapped[str | None] = acol(storage=S(String(128), nullable=True))
    after_checksum: Mapped[str | None] = acol(storage=S(String(128), nullable=True))

    @classmethod
    async def record_transaction(cls, db: Any, payload: Mapping[str, Any]) -> "OperatorTransaction":
        return await create_record(
            cls,
            db,
            {
                "transaction_id": payload.get("transaction_id"),
                "ts": payload.get("ts"),
                "command": payload.get("command"),
                "resource": payload.get("resource"),
                "status": payload.get("status"),
                "record_id": payload.get("record_id"),
                "changed_ids_json": json.dumps(list(payload.get("changed_ids") or []), sort_keys=True),
                "summary_json": json.dumps(dict(payload.get("summary") or {}), sort_keys=True),
                "actor": payload.get("actor"),
                "profile": payload.get("profile"),
                "tenant": payload.get("tenant"),
                "issuer": payload.get("issuer"),
                "before_checksum": payload.get("before_checksum"),
                "after_checksum": payload.get("after_checksum"),
            },
        )

    @classmethod
    async def list_transactions(cls, db: Any) -> list[dict[str, Any]]:
        rows = await list_records(cls, db)
        return [
            {
                "transaction_id": field(row, "transaction_id"),
                "ts": field(row, "ts"),
                "command": field(row, "command"),
                "resource": field(row, "resource"),
                "status": field(row, "status"),
                "record_id": field(row, "record_id"),
                "changed_ids": json.loads(field(row, "changed_ids_json") or "[]"),
                "summary": json.loads(field(row, "summary_json") or "{}"),
                "actor": field(row, "actor"),
                "profile": field(row, "profile"),
                "tenant": field(row, "tenant"),
                "issuer": field(row, "issuer"),
                "before_checksum": field(row, "before_checksum"),
                "after_checksum": field(row, "after_checksum"),
            }
            for row in sorted(rows, key=lambda item: (str(field(item, "ts", "")), str(field(item, "transaction_id", ""))))
        ]


__all__ = ["OperatorTransaction"]
