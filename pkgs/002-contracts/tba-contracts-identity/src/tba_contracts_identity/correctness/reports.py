from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CorrectnessProofSection:
    section_id: str
    passed: bool
    summary: str
    failures: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.section_id or not self.summary:
            raise ValueError("section_id and summary are required")
        object.__setattr__(self, "failures", tuple(sorted(set(self.failures))))


@dataclass(frozen=True, slots=True)
class ControlPlaneCorrectnessReport:
    report_id: str
    passed: bool
    sections: tuple[CorrectnessProofSection, ...]
    failures: tuple[str, ...]


__all__ = [
    "ControlPlaneCorrectnessReport",
    "CorrectnessProofSection",
]
