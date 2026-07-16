"""Reusable workload-identity bases."""

from abc import ABC

from tigrbl_workload_identity_contracts import (
    SpiffeId,
    SpiffeTrustBundle,
    Svid,
    SvidProviderPort,
    SvidVerifierPort,
    TrustBundleProviderPort,
    TrustDomain,
)


class SvidProviderBase(SvidProviderPort, ABC):
    def fetch_svid(self, audience: str | None = None, /) -> Svid:
        raise NotImplementedError


class SvidVerifierBase(SvidVerifierPort, ABC):
    def verify_svid(self, svid: Svid, audience: str | None = None, /) -> SpiffeId:
        raise NotImplementedError


class TrustBundleProviderBase(TrustBundleProviderPort, ABC):
    def bundle_for(self, trust_domain: TrustDomain, /) -> SpiffeTrustBundle:
        raise NotImplementedError


__all__ = ["SvidProviderBase", "SvidVerifierBase", "TrustBundleProviderBase"]
