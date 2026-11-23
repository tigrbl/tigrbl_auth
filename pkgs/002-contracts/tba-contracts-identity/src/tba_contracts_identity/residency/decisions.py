"""Residency policy decision contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResidencyDecision:
    allowed: bool
    tenant_id: str
    processing_region: str
    residency_zone: str
    reasons: tuple[str, ...]
    transfer_required: bool


__all__ = ["ResidencyDecision"]
