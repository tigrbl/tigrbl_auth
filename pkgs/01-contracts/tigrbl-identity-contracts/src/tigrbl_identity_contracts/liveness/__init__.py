from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from tigrbl_identity_core.clock import parse_time


class ConvergenceState(str, Enum):
    PENDING = "pending"
    CONVERGED = "converged"
    LATE = "late"


@dataclass(frozen=True, slots=True)
class ConvergenceEvent:
    event_id: str
    mutation_id: str
    resource_id: str
    issued_at: str
    observed_at: str | None = None
    expected_within_seconds: int = 60

    def __post_init__(self) -> None:
        if not self.event_id or not self.mutation_id or not self.resource_id:
            raise ValueError("event_id, mutation_id, and resource_id are required")
        if self.expected_within_seconds < 0:
            raise ValueError("expected_within_seconds cannot be negative")

    @property
    def state(self) -> ConvergenceState:
        if self.observed_at is None:
            return ConvergenceState.PENDING
        elapsed = (parse_time(self.observed_at) - parse_time(self.issued_at)).total_seconds()
        return ConvergenceState.CONVERGED if elapsed <= self.expected_within_seconds else ConvergenceState.LATE


@dataclass(frozen=True, slots=True)
class LivenessConvergenceReport:
    passed: bool
    converged: tuple[ConvergenceEvent, ...]
    pending: tuple[ConvergenceEvent, ...]
    late: tuple[ConvergenceEvent, ...]
    failures: tuple[str, ...]

__all__ = [
    "ConvergenceEvent",
    "ConvergenceState",
    "LivenessConvergenceReport",
]
