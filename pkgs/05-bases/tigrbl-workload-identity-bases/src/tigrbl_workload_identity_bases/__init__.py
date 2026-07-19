"""Reusable protocol-neutral workload-identity bases."""

from abc import ABC

from tigrbl_workload_identity_contracts import (
    DelegatedWorkloadCredentialProviderPort,
    DelegatedWorkloadCredentialRequest,
    ResolvedWorkload,
    SpiffeId,
    SpiffeTrustBundle,
    Svid,
    SvidProviderPort,
    SvidVerifierPort,
    TrustBundleProviderPort,
    TrustDomain,
    WorkloadCredential,
    WorkloadCredentialProviderPort,
    WorkloadCredentialRequest,
    WorkloadCredentialSet,
    WorkloadCredentialVerifierPort,
    WorkloadIdentityRef,
    WorkloadReference,
    WorkloadReferenceResolverPort,
    WorkloadTrustMaterial,
    WorkloadTrustMaterialProviderPort,
)


class WorkloadReferenceResolverBase(WorkloadReferenceResolverPort, ABC):
    def resolve(self, reference: WorkloadReference, /) -> ResolvedWorkload:
        raise NotImplementedError


class WorkloadCredentialProviderBase(WorkloadCredentialProviderPort, ABC):
    def obtain(self, request: WorkloadCredentialRequest, /) -> WorkloadCredentialSet:
        raise NotImplementedError


class DelegatedWorkloadCredentialProviderBase(
    DelegatedWorkloadCredentialProviderPort,
    ABC,
):
    def obtain_for(
        self,
        request: DelegatedWorkloadCredentialRequest,
        /,
    ) -> WorkloadCredentialSet:
        raise NotImplementedError


class WorkloadCredentialVerifierBase(WorkloadCredentialVerifierPort, ABC):
    def verify(
        self,
        credential: WorkloadCredential,
        expected_identity: WorkloadIdentityRef | None = None,
        /,
    ) -> WorkloadIdentityRef:
        raise NotImplementedError


class WorkloadTrustMaterialProviderBase(
    WorkloadTrustMaterialProviderPort,
    ABC,
):
    def trust_material_for(
        self,
        identity: WorkloadIdentityRef,
        format: str,
        /,
    ) -> WorkloadTrustMaterial:
        raise NotImplementedError


# Compatibility bases for the existing SPIFFE-named layer-20 providers. New
# providers must implement the neutral bases above; these leave layer 05 after
# those providers are migrated.
class SvidProviderBase(SvidProviderPort, ABC):
    def fetch_svid(self, audience: str | None = None, /) -> Svid:
        raise NotImplementedError


class SvidVerifierBase(SvidVerifierPort, ABC):
    def verify_svid(self, svid: Svid, audience: str | None = None, /) -> SpiffeId:
        raise NotImplementedError


class TrustBundleProviderBase(TrustBundleProviderPort, ABC):
    def bundle_for(self, trust_domain: TrustDomain, /) -> SpiffeTrustBundle:
        raise NotImplementedError


__all__ = [
    "DelegatedWorkloadCredentialProviderBase",
    "SvidProviderBase",
    "SvidVerifierBase",
    "TrustBundleProviderBase",
    "WorkloadCredentialProviderBase",
    "WorkloadCredentialVerifierBase",
    "WorkloadReferenceResolverBase",
    "WorkloadTrustMaterialProviderBase",
]