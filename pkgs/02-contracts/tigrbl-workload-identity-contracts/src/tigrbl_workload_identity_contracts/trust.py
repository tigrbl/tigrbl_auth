"""Protocol-neutral workload trust material."""

from dataclasses import dataclass

from tigrbl_identity_core import TrustMaterialId


@dataclass(frozen=True, slots=True)
class WorkloadTrustMaterial:
    material_id: TrustMaterialId
    trust_domain: str
    format: str
    artifact: bytes
    version: str


__all__ = ["WorkloadTrustMaterial"]