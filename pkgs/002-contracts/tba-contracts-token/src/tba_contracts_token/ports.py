from typing import Mapping, Protocol

from .profiles import TokenProfile
from .verification import TokenVerificationRequest, TokenVerificationResult


class TokenIssuerPort(Protocol):
    def issue(
        self, profile: TokenProfile, claims: Mapping[str | int, object], /
    ) -> str | bytes: ...


class TokenVerifierPort(Protocol):
    def verify(
        self, request: TokenVerificationRequest, /
    ) -> TokenVerificationResult: ...


__all__ = ["TokenIssuerPort", "TokenVerifierPort"]
