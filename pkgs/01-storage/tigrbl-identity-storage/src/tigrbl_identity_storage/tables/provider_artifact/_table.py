"""Durable provider artifact and descriptor registry."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from .._ops import create_record, first_record, record_id, update_record


class ProviderArtifact(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "provider_artifacts"
    __table_args__ = ({"schema": "authn"},)

    artifact_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    artifact_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    provider_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    tenant_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    status: Mapped[str] = acol(storage=S(String(64), nullable=False, default="active", index=True))
    artifact_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))


__all__ = ["ProviderArtifact"]
