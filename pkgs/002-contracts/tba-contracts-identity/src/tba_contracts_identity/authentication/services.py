"""Service identity authentication contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass

from ..principals import Identity


@dataclass(frozen=True, slots=True)
class ServiceIdentityAuthentication:
    service: Identity
    credential_id: str
    granted_permissions: tuple[str, ...]


__all__ = ["ServiceIdentityAuthentication"]
