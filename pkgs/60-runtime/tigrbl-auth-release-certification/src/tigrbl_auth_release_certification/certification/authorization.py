from __future__ import annotations

import time
from typing import Iterable, Sequence

from .base import CertificationError
from tigrbl_release_contracts import (
    AuthorizationSnapshot,
    AuthorizationState,
    CapabilityRecord,
)


def runtime_capability_truth(
    configured: Sequence[CapabilityRecord],
    advertised: Iterable[str],
) -> dict[str, bool]:
    """Return evidence-backed capability truth and fail on stale advertising."""

    by_name = {record.name: record for record in configured}
    advertised_set = set(advertised)
    unknown = advertised_set.difference(by_name)
    if unknown:
        raise CertificationError(f"advertised unknown capabilities: {sorted(unknown)}")
    for name in advertised_set:
        record = by_name[name]
        if not record.enabled:
            raise CertificationError(f"disabled capability advertised: {name}")
        if not record.evidence_id:
            raise CertificationError(f"capability lacks evidence: {name}")
    return {name: record.enabled and bool(record.evidence_id) for name, record in by_name.items()}


def mutate_authorization_state(state: AuthorizationState, reason: str) -> int:
    if not reason:
        raise CertificationError("authorization mutation requires a reason")
    state.version += 1
    state.updated_at = time.time()
    state.mutations.append(reason)
    return state.version


if not hasattr(AuthorizationState, "mutate"):
    AuthorizationState.mutate = mutate_authorization_state  # type: ignore[attr-defined]


def assert_authorization_fresh(
    snapshot: AuthorizationSnapshot,
    state: AuthorizationState,
    *,
    now: float | None = None,
) -> None:
    if snapshot.subject_id != state.subject_id:
        raise CertificationError("authorization subject mismatch")
    current_time = time.time() if now is None else now
    if snapshot.version < state.version:
        raise CertificationError("authorization snapshot predates current mutation version")
    if current_time - snapshot.issued_at > snapshot.max_staleness_seconds:
        raise CertificationError("authorization snapshot exceeds freshness window")
