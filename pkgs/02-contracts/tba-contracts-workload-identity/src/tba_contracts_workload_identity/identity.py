"""Protocol-neutral workload identity references."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkloadIdentityRef:
    identifier: str
    namespace: str | None = None

    def __post_init__(self) -> None:
        if not self.identifier.strip():
            raise ValueError("workload identity identifier is required")


__all__ = ["WorkloadIdentityRef"]