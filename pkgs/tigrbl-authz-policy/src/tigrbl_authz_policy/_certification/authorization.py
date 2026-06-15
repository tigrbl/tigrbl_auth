from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Iterable, Sequence

from .base import CertificationError


@dataclass(frozen=True)
class CapabilityRecord:
    name: str
    enabled: bool
    evidence_id: str | None = None
    route: str | None = None


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


@dataclass
class AuthorizationState:
    subject_id: str
    version: int = 1
    updated_at: float = field(default_factory=time.time)
    mutations: list[str] = field(default_factory=list)

    def mutate(self, reason: str) -> int:
        if not reason:
            raise CertificationError("authorization mutation requires a reason")
        self.version += 1
        self.updated_at = time.time()
        self.mutations.append(reason)
        return self.version


@dataclass(frozen=True)
class AuthorizationSnapshot:
    subject_id: str
    version: int
    issued_at: float
    max_staleness_seconds: int


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
