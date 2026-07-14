"""Local API key authenticator provider."""

from __future__ import annotations

import hashlib
import hmac

from tigrbl_identity_authenticator_bases import AuthenticatorBase, CredentialKindMixin
from tigrbl_identity_contracts.authenticators import AuthenticationFactorClass, AuthenticatorKind
from tigrbl_identity_contracts.credentials import CredentialKind


class ApiKeyLocalAuthenticator(CredentialKindMixin, AuthenticatorBase):
    def __init__(self) -> None:
        super().__init__(
            kind=AuthenticatorKind.API_KEY_LOCAL,
            factor_class=AuthenticationFactorClass.POSSESSION,
            credential_kind=CredentialKind.API_KEY,
            description="Local API key authentication.",
        )

    @staticmethod
    def digest_key(presented: str | bytes) -> str:
        value = presented.encode("utf-8") if isinstance(presented, str) else bytes(presented)
        if not value:
            raise ValueError("API key is required")
        return hashlib.sha256(value).hexdigest()

    def matches_digest(self, presented: str | bytes, expected: str) -> bool:
        return hmac.compare_digest(self.digest_key(presented), expected)


__all__ = ["ApiKeyLocalAuthenticator"]
