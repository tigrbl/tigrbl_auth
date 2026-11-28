"""Protocol-neutral workload identity extension ports."""

from typing import Protocol

from .credentials import WorkloadCredential, WorkloadCredentialRequest, WorkloadCredentialSet
from .delegation import DelegatedWorkloadCredentialRequest
from .identity import WorkloadIdentityRef
from .references import ResolvedWorkload, WorkloadReference
from .trust import WorkloadTrustMaterial


class WorkloadReferenceResolverPort(Protocol):
    def resolve(self, reference: WorkloadReference, /) -> ResolvedWorkload: ...


class WorkloadCredentialProviderPort(Protocol):
    def obtain(self, request: WorkloadCredentialRequest, /) -> WorkloadCredentialSet: ...


class DelegatedWorkloadCredentialProviderPort(Protocol):
    def obtain_for(self, request: DelegatedWorkloadCredentialRequest, /) -> WorkloadCredentialSet: ...


class WorkloadCredentialVerifierPort(Protocol):
    def verify(
        self,
        credential: WorkloadCredential,
        expected_identity: WorkloadIdentityRef | None = None,
        /,
    ) -> WorkloadIdentityRef: ...


class WorkloadTrustMaterialProviderPort(Protocol):
    def trust_material_for(self, identity: WorkloadIdentityRef, format: str, /) -> WorkloadTrustMaterial: ...


__all__ = [
    "DelegatedWorkloadCredentialProviderPort",
    "WorkloadCredentialProviderPort",
    "WorkloadCredentialVerifierPort",
    "WorkloadReferenceResolverPort",
    "WorkloadTrustMaterialProviderPort",
]