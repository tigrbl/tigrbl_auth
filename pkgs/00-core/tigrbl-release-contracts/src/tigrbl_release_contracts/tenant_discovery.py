from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TenantPublicDiscoveryBoundaryFeature:
    feature_id: str
    category: str
    runtime_objects: tuple[str, ...]
    guarded_capabilities: tuple[str, ...]


__all__ = ["TenantPublicDiscoveryBoundaryFeature"]
