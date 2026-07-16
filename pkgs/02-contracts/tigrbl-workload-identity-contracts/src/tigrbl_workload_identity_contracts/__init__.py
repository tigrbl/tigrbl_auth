"""Canonical workload identity and SVID contracts."""

from .bundles import SpiffeTrustBundle, TrustBundleProviderPort
from .selectors import WorkloadSelector
from .spiffe import SpiffeId, TrustDomain
from .svid import Svid, SvidFormat, SvidProviderPort, SvidVerifierPort

__all__ = [
    "SpiffeId",
    "SpiffeTrustBundle",
    "Svid",
    "SvidFormat",
    "SvidProviderPort",
    "SvidVerifierPort",
    "TrustBundleProviderPort",
    "TrustDomain",
    "WorkloadSelector",
]
