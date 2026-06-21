"""Durable control-plane correctness report artifacts."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, Boolean, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from ._ops import create_record, first_record, list_records


class ControlCorrectnessReport(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "control_correctness_reports"
    __table_args__ = ({"schema": "authn"},)

    report_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    release_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    passed: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=False, index=True))
    report_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))

    @classmethod
    async def snapshot(cls, db: Any, **payload: Any) -> "ControlCorrectnessReport":
        payload.setdefault("report_payload", dict(payload))
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, report_id: str) -> "ControlCorrectnessReport | None":
        return await first_record(cls, db, {"report_id": report_id})

    @classmethod
    async def list_for_release(cls, db: Any, *, release_id: str) -> list["ControlCorrectnessReport"]:
        return await list_records(cls, db, {"release_id": release_id})


__all__ = ["ControlCorrectnessReport"]
