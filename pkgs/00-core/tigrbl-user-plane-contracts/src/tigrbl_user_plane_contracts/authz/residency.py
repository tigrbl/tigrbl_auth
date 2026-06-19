from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


class ResidencyPolicyError(PermissionError):
    """Raised when data residency policy denies or cannot evaluate a request."""


@dataclass(frozen=True, slots=True)
class ResidencyZone:
    zone_id: str
    jurisdictions: tuple[str, ...]
    sovereign_controls: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.zone_id:
            raise ValueError("residency zone requires a zone_id")
        if not self.jurisdictions:
            raise ValueError("residency zone requires at least one jurisdiction")


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


@dataclass(frozen=True, slots=True)
class ResidencyDecision:
    allowed: bool
    tenant_id: str
    processing_region: str
    residency_zone: str
    reasons: tuple[str, ...]
    transfer_required: bool


__all__ = [
    "ResidencyDecision",
    "ResidencyPolicyError",
    "ResidencyZone",
    "TenantResidencyRecord",
]
