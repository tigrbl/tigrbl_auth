from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


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


def evaluate_residency_access(
    record: TenantResidencyRecord,
    *,
    processing_region: str,
    tenant_id: str | None = None,
    realm: str | None = None,
) -> ResidencyDecision:
    reasons: list[str] = []
    allowed = True
    if tenant_id is not None and tenant_id != record.tenant_id:
        allowed = False
        reasons.append("tenant mismatch")
    if realm is not None and record.realm is not None and realm != record.realm:
        allowed = False
        reasons.append("realm mismatch")
    if not record.allowed_processing_regions:
        allowed = False
        reasons.append("no allowed processing regions configured")
    if processing_region in record.restricted_transfer_regions:
        allowed = False
        reasons.append("processing region is transfer-restricted")
    if (
        record.allowed_processing_regions
        and processing_region not in record.allowed_processing_regions
    ):
        allowed = False
        reasons.append("processing region is outside allowed residency boundary")
    if allowed:
        reasons.append("processing region is inside allowed residency boundary")
    return ResidencyDecision(
        allowed=allowed,
        tenant_id=record.tenant_id,
        processing_region=processing_region,
        residency_zone=record.residency_zone.zone_id,
        reasons=tuple(reasons),
        transfer_required=processing_region not in record.residency_zone.jurisdictions,
    )


def assert_residency_access(
    record: TenantResidencyRecord,
    *,
    processing_region: str,
    tenant_id: str | None = None,
    realm: str | None = None,
) -> ResidencyDecision:
    decision = evaluate_residency_access(
        record,
        processing_region=processing_region,
        tenant_id=tenant_id,
        realm=realm,
    )
    if not decision.allowed:
        raise ResidencyPolicyError("; ".join(decision.reasons))
    return decision


def residency_policy_manifest(
    records: Sequence[TenantResidencyRecord],
) -> dict[str, Any]:
    tenants = []
    for record in records:
        tenants.append(
            {
                "tenant_id": record.tenant_id,
                "realm": record.realm,
                "residency_zone": record.residency_zone.zone_id,
                "allowed_processing_regions": list(record.allowed_processing_regions),
                "restricted_transfer_regions": list(record.restricted_transfer_regions),
                "sovereign_controls": list(record.residency_zone.sovereign_controls),
            }
        )
    return {"tenants": tenants}


__all__ = [
    "ResidencyDecision",
    "ResidencyPolicyError",
    "ResidencyZone",
    "TenantResidencyRecord",
    "assert_residency_access",
    "evaluate_residency_access",
    "residency_policy_manifest",
]
