from __future__ import annotations

from tigrbl_user_plane_contracts.authz.liveness import (
    ConvergenceEvent,
    ConvergenceState,
    LivenessConvergenceReport,
)


def evaluate_liveness_convergence(events: tuple[ConvergenceEvent, ...]) -> LivenessConvergenceReport:
    by_id = {event.event_id: event for event in events}
    rows = tuple(by_id[event_id] for event_id in sorted(by_id))
    converged = tuple(event for event in rows if event.state is ConvergenceState.CONVERGED)
    pending = tuple(event for event in rows if event.state is ConvergenceState.PENDING)
    late = tuple(event for event in rows if event.state is ConvergenceState.LATE)
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
