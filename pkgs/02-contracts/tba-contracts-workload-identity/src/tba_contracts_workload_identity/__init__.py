"""Protocol-neutral workload identity contracts with deprecated SPIFFE compatibility exports."""

from .credentials import WorkloadCredential, WorkloadCredentialRequest, WorkloadCredentialSet
from .delegation import DelegatedWorkloadCredentialRequest, WorkloadCredentialEntitlement
from .identity import WorkloadIdentityRef
from .ports import DelegatedWorkloadCredentialProviderPort, WorkloadCredentialProviderPort, WorkloadCredentialVerifierPort, WorkloadReferenceResolverPort, WorkloadTrustMaterialProviderPort
from .references import ResolvedWorkload, WorkloadReference
from .selectors import WorkloadSelector
from .trust import WorkloadTrustMaterial

# Compatibility only. Canonical SPIFFE ownership moves to layer 10/50.
from .bundles import SpiffeTrustBundle, TrustBundleProviderPort
from .spiffe import SpiffeId, TrustDomain
from .svid import Svid, SvidFormat, SvidProviderPort, SvidVerifierPort

__all__ = [
    "DelegatedWorkloadCredentialProviderPort",
    "DelegatedWorkloadCredentialRequest",
    "ResolvedWorkload",
    "SpiffeId",
    "SpiffeTrustBundle",
    "Svid",
    "SvidFormat",
    "SvidProviderPort",
    "SvidVerifierPort",
    "TrustBundleProviderPort",
    "TrustDomain",
    "WorkloadCredential",
    "WorkloadCredentialEntitlement",
    "WorkloadCredentialProviderPort",
    "WorkloadCredentialRequest",
    "WorkloadCredentialSet",
    "WorkloadCredentialVerifierPort",
    "WorkloadIdentityRef",
    "WorkloadReference",
    "WorkloadReferenceResolverPort",
    "WorkloadSelector",
    "WorkloadTrustMaterial",
    "WorkloadTrustMaterialProviderPort",
]