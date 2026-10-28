"""Protocol-neutral workload trust material."""

from dataclasses import dataclass

from tba_primitives_identity import TrustMaterialId


@dataclass(frozen=True, slots=True)
class WorkloadTrustMaterial:
    material_id: TrustMaterialId
    trust_domain: str
    format: str
    artifact: bytes
    version: str


__all__ = ["WorkloadTrustMaterial"]