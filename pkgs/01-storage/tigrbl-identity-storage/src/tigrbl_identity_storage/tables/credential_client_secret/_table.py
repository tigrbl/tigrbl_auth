"""Durable OAuth client-secret credential records."""

from __future__ import annotations

import datetime as dt
from typing import Any

from tigrbl_identity_storage.framework import GUIDPk, JSON, Mapped, RestOltpTable, S, String, TZDateTime, Timestamped, acol

from .._ops import first_record, list_records, record_id, update_record


class CredentialClientSecret(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "credential_client_secrets"
    __table_args__ = {"extend_existing": True, "schema": "authn"}

    credential_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    principal_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    client_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    secret_digest: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    expires_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    secret_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


__all__ = ["CredentialClientSecret"]
