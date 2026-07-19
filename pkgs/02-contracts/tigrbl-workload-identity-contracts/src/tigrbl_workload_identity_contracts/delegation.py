"""Delegated workload credential semantics."""

from dataclasses import dataclass, field
from typing import Mapping

from tigrbl_identity_core import CredentialFormat, PrincipalRef

from .credentials import WorkloadCredentialRequest
from .references import WorkloadReference


@dataclass(frozen=True, slots=True)
class DelegatedWorkloadCredentialRequest:
    actor: PrincipalRef
    request: WorkloadCredentialRequest
    authorization_context: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class WorkloadCredentialEntitlement:
    actor: PrincipalRef
    workload: WorkloadReference
    allowed_formats: frozenset[CredentialFormat]
    constraints: Mapping[str, object] = field(default_factory=dict)


__all__ = ["DelegatedWorkloadCredentialRequest", "WorkloadCredentialEntitlement"]