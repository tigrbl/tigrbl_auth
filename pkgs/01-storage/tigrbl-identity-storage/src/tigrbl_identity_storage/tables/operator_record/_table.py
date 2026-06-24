"""Table-owned operator resource records."""

from __future__ import annotations

import copy
from typing import Any, Mapping

from tigrbl_identity_storage.framework import RestOltpTable, Boolean, Mapped, S, String, acol



def _default_status(resource: str) -> str:
    return "staged" if resource in {"keys"} else "active"


class OperatorRecord(RestOltpTable):
    __tablename__ = "operator_records"

    id: Mapped[str] = acol(storage=S(String(512), primary_key=True, nullable=False))
    resource: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    record_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    status: Mapped[str] = acol(storage=S(String(64), nullable=False, default="active", index=True))
    enabled: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=True))
    created_at: Mapped[str] = acol(storage=S(String(64), nullable=False))
    updated_at: Mapped[str] = acol(storage=S(String(64), nullable=False))
    actor: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    profile: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    tenant: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    issuer: Mapped[str | None] = acol(storage=S(String(512), nullable=True))
    revision: Mapped[int] = acol(storage=S(nullable=False, default=1))
    data_json: Mapped[str] = acol(storage=S(String(20000), nullable=False, default="{}"))

    @staticmethod
    def store_id(resource: str, record_id: str) -> str:
        return f"{resource}:{record_id}"


def _without_revision(record: Mapping[str, Any]) -> dict[str, Any]:
    cleaned = copy.deepcopy(dict(record))
    cleaned.pop("revision", None)
    return cleaned


__all__ = ["OperatorRecord"]
