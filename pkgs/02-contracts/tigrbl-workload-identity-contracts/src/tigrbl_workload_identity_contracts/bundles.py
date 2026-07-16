"""Canonical workload trust-bundle contracts."""

from dataclasses import dataclass
from typing import Protocol, Sequence

from .spiffe import TrustDomain


@dataclass(frozen=True, slots=True)
class SpiffeTrustBundle:
    trust_domain: TrustDomain
    version: str
    x509_authorities: Sequence[bytes] = ()
    jwt_authorities: Sequence[object] = ()


class TrustBundleProviderPort(Protocol):
    def bundle_for(self, trust_domain: TrustDomain, /) -> SpiffeTrustBundle: ...


__all__ = ["SpiffeTrustBundle", "TrustBundleProviderPort"]
