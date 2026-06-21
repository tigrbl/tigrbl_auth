"""Device principal profile contract objects."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeviceIdentity:
    device_id: str
    subject_id: str
    tenant_id: str
    credential_posture: str
    last_ip_country: str | None
    created_at: str
    revoked: bool = False


__all__ = ["DeviceIdentity"]
