from tigrbl_security_trust_contracts import IssuerTrustDecision, IssuerTrustResolverPort


class PinnedIssuerTrustProvider(IssuerTrustResolverPort):
    def __init__(self, trusted_issuers: dict[str, set[str]] | None = None):
        self._trusted = {
            profile: set(issuers)
            for profile, issuers in (trusted_issuers or {}).items()
        }

    def trust(self, issuer: str, profile: str) -> None:
        if not issuer or not profile:
            raise ValueError("issuer and profile are required")
        self._trusted.setdefault(profile, set()).add(issuer)

    def distrust(self, issuer: str, profile: str) -> None:
        self._trusted.get(profile, set()).discard(issuer)

    def resolve(self, issuer: str, profile: str, /) -> IssuerTrustDecision:
        trusted = issuer in self._trusted.get(profile, set())
        reason = (
            "issuer explicitly pinned for profile"
            if trusted
            else "issuer not pinned for profile"
        )
        return IssuerTrustDecision(issuer, profile, trusted, reason)


__all__ = ["PinnedIssuerTrustProvider"]
