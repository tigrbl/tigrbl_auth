"""Reusable trust-resolution bases."""

from abc import ABC

from tba_contracts_security_trust import (
    IssuerTrustDecision,
    IssuerTrustResolverPort,
)


class IssuerTrustResolverBase(IssuerTrustResolverPort, ABC):
    def resolve(self, issuer: str, profile: str, /) -> IssuerTrustDecision:
        raise NotImplementedError


class WalletTrustProviderBase(ABC):
    def trust_for_wallet(self, wallet_id: str, /) -> object:
        raise NotImplementedError


__all__ = ["IssuerTrustResolverBase", "WalletTrustProviderBase"]
