"""Compatibility facade for bases extracted into canonical families."""

from tba_bases_certificate import CertificatePathValidatorBase
from tba_bases_did import DidResolverBase
from tba_bases_trust import IssuerTrustResolverBase, WalletTrustProviderBase
from tba_bases_workload_identity import (
    SvidProviderBase,
    SvidVerifierBase,
    TrustBundleProviderBase,
)


__all__ = [
    "CertificatePathValidatorBase",
    "DidResolverBase",
    "IssuerTrustResolverBase",
    "SvidProviderBase",
    "SvidVerifierBase",
    "TrustBundleProviderBase",
    "WalletTrustProviderBase",
]
