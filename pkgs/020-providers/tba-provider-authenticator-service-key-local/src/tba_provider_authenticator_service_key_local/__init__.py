"""Local service key authenticator provider."""

from __future__ import annotations

import hmac

from tba_bases_authenticator import AuthenticatorBase, CredentialKindMixin
from tba_contracts_identity.authenticators import AuthenticationFactorClass, AuthenticatorKind
from tba_contracts_identity.credentials import CredentialKind
from tba_primitives_identity.credential_digests import (
    credential_digest,
    text_credential_digest,
)


class ServiceKeyLocalAuthenticator(CredentialKindMixin, AuthenticatorBase):
    def __init__(self) -> None:
        super().__init__(
            kind=AuthenticatorKind.SERVICE_KEY_LOCAL,
            factor_class=AuthenticationFactorClass.SERVICE,
            credential_kind=CredentialKind.SERVICE_KEY,
            description="Local service key authentication.",
        )

    @staticmethod
    def digest_key(presented: str | bytes) -> str:
        if not presented:
            raise ValueError("service key is required")
        return credential_digest(presented)

    @staticmethod
    def digest_text_key(presented: str) -> str:
        if not presented:
            raise ValueError("service key is required")
        return text_credential_digest(presented)

    def matches_digest(self, presented: str | bytes, expected: str) -> bool:
        return hmac.compare_digest(self.digest_key(presented), expected)


__all__ = ["ServiceKeyLocalAuthenticator"]
