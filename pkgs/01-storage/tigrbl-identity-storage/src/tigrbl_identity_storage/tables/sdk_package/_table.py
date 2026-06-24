"""Durable SDK package catalog."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from .._ops import create_record, first_record, record_id, update_record


class SDKPackageRecord(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "sdk_packages"
    __table_args__ = ({"schema": "authn"},)

    sdk_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    package_name: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    language: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    version: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    release_channel: Mapped[str] = acol(storage=S(String(64), nullable=False, default="stable", index=True))
    contract_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))


__all__ = ["SDKPackageRecord"]
