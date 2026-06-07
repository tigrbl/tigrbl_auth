from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ConvergenceState(str, Enum):
    PENDING = "pending"
    CONVERGED = "converged"
    LATE = "late"


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


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
        elapsed = (_parse_time(self.observed_at) - _parse_time(self.issued_at)).total_seconds()
        return ConvergenceState.CONVERGED if elapsed <= self.expected_within_seconds else ConvergenceState.LATE


@dataclass(frozen=True, slots=True)
class LivenessConvergenceReport:
    passed: bool
    converged: tuple[ConvergenceEvent, ...]
    pending: tuple[ConvergenceEvent, ...]
    late: tuple[ConvergenceEvent, ...]
    failures: tuple[str, ...]


def evaluate_liveness_convergence(events: tuple[ConvergenceEvent, ...]) -> LivenessConvergenceReport:
    converged = tuple(event for event in events if event.state is ConvergenceState.CONVERGED)
    pending = tuple(event for event in events if event.state is ConvergenceState.PENDING)
    late = tuple(event for event in events if event.state is ConvergenceState.LATE)
    failures = tuple(
        [*(f"mutation {event.mutation_id!r} is pending convergence" for event in pending)]
        + [*(f"mutation {event.mutation_id!r} converged after its expected window" for event in late)]
    )
    return LivenessConvergenceReport(
        passed=not failures,
        converged=converged,
        pending=pending,
        late=late,
        failures=failures,
    )


__all__ = [
    "ConvergenceEvent",
    "ConvergenceState",
    "LivenessConvergenceReport",
    "evaluate_liveness_convergence",
]
