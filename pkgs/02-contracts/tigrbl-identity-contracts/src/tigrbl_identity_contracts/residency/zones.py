"""Residency zone contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass


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


__all__ = ["ResidencyZone"]
