from abc import ABC

from tigrbl_identity_contracts.did import (
    Did,
    DidResolutionResult,
    DidResolverPort,
    DidUrl,
)
from tigrbl_identity_contracts.workloads import (
    SpiffeId,
    SpiffeTrustBundle,
    Svid,
    SvidProviderPort,
    SvidVerifierPort,
    TrustBundleProviderPort,
    TrustDomain,
)
from tigrbl_security_trust_contracts import (
    CertificatePathValidationRequest,
    CertificatePathValidationResult,
    CertificatePathValidatorPort,
    IssuerTrustDecision,
    IssuerTrustResolverPort,
)


class DidResolverBase(DidResolverPort, ABC):
    def resolve(self, did: Did, /) -> DidResolutionResult:
        raise NotImplementedError

    def dereference(self, did_url: DidUrl, /):
        raise NotImplementedError


class SvidProviderBase(SvidProviderPort, ABC):
    def fetch_svid(self, audience: str | None = None, /) -> Svid:
        raise NotImplementedError


class SvidVerifierBase(SvidVerifierPort, ABC):
    def verify_svid(self, svid: Svid, audience: str | None = None, /) -> SpiffeId:
        raise NotImplementedError


class TrustBundleProviderBase(TrustBundleProviderPort, ABC):
    def bundle_for(self, trust_domain: TrustDomain, /) -> SpiffeTrustBundle:
        raise NotImplementedError


class IssuerTrustResolverBase(IssuerTrustResolverPort, ABC):
    def resolve(self, issuer: str, profile: str, /) -> IssuerTrustDecision:
        raise NotImplementedError


class CertificatePathValidatorBase(CertificatePathValidatorPort, ABC):
    def validate(
        self, request: CertificatePathValidationRequest, /
    ) -> CertificatePathValidationResult:
        raise NotImplementedError


class WalletTrustProviderBase(ABC):
    def trust_for_wallet(self, wallet_id: str, /) -> object:
        raise NotImplementedError


__all__ = [
    "CertificatePathValidatorBase",
    "DidResolverBase",
    "IssuerTrustResolverBase",
    "SvidProviderBase",
    "SvidVerifierBase",
    "TrustBundleProviderBase",
    "WalletTrustProviderBase",
]
