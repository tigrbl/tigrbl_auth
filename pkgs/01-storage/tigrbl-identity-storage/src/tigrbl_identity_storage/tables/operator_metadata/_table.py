"""Table-owned operator store metadata."""

from __future__ import annotations

import json
from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, Mapped, S, String, TZDateTime, acol

from .._ops import create_record, field, first_record, list_records, record_id, update_record, utc_now


class OperatorMetadata(RestOltpTable):
    __tablename__ = "operator_metadata"

    key: Mapped[str] = acol(storage=S(String(255), primary_key=True, nullable=False))
    value_json: Mapped[str] = acol(storage=S(String(8000), nullable=False, default="null"))
    updated_at: Mapped[Any] = acol(storage=S(TZDateTime, nullable=False, default=utc_now))


__all__ = ["OperatorMetadata"]
