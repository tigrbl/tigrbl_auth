"""Table-owned operator store metadata."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, Mapped, S, String, TZDateTime, acol
from tigrbl_identity_core.clock import utc_now


class OperatorMetadata(RestOltpTable):
    __tablename__ = "operator_metadata"

    key: Mapped[str] = acol(storage=S(String(255), primary_key=True, nullable=False))
    value_json: Mapped[str] = acol(storage=S(String(8000), nullable=False, default="null"))
    updated_at: Mapped[Any] = acol(storage=S(TZDateTime, nullable=False, default=utc_now))


__all__ = ["OperatorMetadata"]
