"""Canonical workload selector contracts."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkloadSelector:
    selector_type: str
    value: str


__all__ = ["WorkloadSelector"]
