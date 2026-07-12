from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class IssuerTrustDecision:
    issuer: str
    profile: str
    trusted: bool
    reason: str | None = None


class IssuerTrustResolverPort(Protocol):
    def resolve(self, issuer: str, profile: str, /) -> IssuerTrustDecision: ...


__all__ = ["IssuerTrustDecision", "IssuerTrustResolverPort"]
