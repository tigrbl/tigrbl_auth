"""Service principal contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ServiceIdentity:
    service_id: str
    tenant_id: str
    name: str
    scopes: tuple[str, ...]
    enabled: bool = True


__all__ = ["ServiceIdentity"]
