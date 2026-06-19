from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeQualification:
    artifact_sha256: str
    dependency_lock_sha256: str
    config_sha256: str
    product_surface: str
    capabilities: frozenset[str]


__all__ = ["RuntimeQualification"]
