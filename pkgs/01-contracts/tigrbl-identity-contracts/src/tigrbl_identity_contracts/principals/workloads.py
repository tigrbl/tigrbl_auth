"""Workload principal profile contract objects."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkloadIdentity:
    workload_id: str
    tenant_id: str
    trust_domain: str
    cloud: str
    namespace: str
    attestor: str
    credential_id: str
    created_at: str
    revoked: bool = False


__all__ = ["WorkloadIdentity"]
