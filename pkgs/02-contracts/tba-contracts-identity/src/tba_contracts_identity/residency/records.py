"""Tenant residency record contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .zones import ResidencyZone


@dataclass(frozen=True, slots=True)
class TenantResidencyRecord:
    tenant_id: str
    residency_zone: ResidencyZone
    allowed_processing_regions: tuple[str, ...]
    restricted_transfer_regions: tuple[str, ...] = ()
    realm: str | None = None
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.tenant_id:
            raise ValueError("tenant residency record requires a tenant_id")


__all__ = ["TenantResidencyRecord"]
