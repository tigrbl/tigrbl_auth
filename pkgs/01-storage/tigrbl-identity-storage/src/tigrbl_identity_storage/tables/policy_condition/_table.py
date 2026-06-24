"""Durable dynamic policy conditions."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from .._ops import clear_records, create_record, list_records


class PolicyCondition(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "policy_conditions"
    __table_args__ = ({"schema": "authn"},)

    policy_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    field_name: Mapped[str] = acol(storage=S(String(255), nullable=False))
    operator: Mapped[str] = acol(storage=S(String(64), nullable=False))
    expected: Mapped[dict | list | str | int | float | bool | None] = acol(storage=S(JSON, nullable=True))
    condition_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


__all__ = ["PolicyCondition"]
