"""Service credential contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ServiceCredential:
    credential_id: str
    service_id: str
    label: str
    raw_key: str
    created_at: str
    revoked: bool = False
    expires_at: str | None = None


__all__ = ["ServiceCredential"]
