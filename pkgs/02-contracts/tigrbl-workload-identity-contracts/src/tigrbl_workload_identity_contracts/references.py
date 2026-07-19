"""Protocol-neutral workload references and resolution results."""

from dataclasses import dataclass, field
from typing import Mapping

from tigrbl_identity_core import WorkloadReferenceId

from .identity import WorkloadIdentityRef


@dataclass(frozen=True, slots=True)
class WorkloadReference:
    reference_id: WorkloadReferenceId
    kind: str
    scope: str
    value: object


@dataclass(frozen=True, slots=True)
class ResolvedWorkload:
    reference: WorkloadReference
    identity: WorkloadIdentityRef | None = None
    attributes: Mapping[str, object] = field(default_factory=dict)
    lifecycle_version: str | None = None


__all__ = ["ResolvedWorkload", "WorkloadReference"]