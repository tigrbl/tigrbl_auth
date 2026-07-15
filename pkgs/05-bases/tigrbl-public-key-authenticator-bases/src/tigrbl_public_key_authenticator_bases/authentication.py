from abc import ABC

from tigrbl_identity_contracts.public_key_authentication import (
    PublicKeyAuthenticationIntent,
    PublicKeyAuthenticationOptions,
    PublicKeyAuthenticationResult,
    VerifiedPublicKeyAssertion,
)


class PublicKeyAssertionVerificationBase(ABC):
    async def begin_authentication(
        self, intent: PublicKeyAuthenticationIntent, /
    ) -> PublicKeyAuthenticationOptions:
        raise NotImplementedError

    async def complete_authentication(
        self, assertion: VerifiedPublicKeyAssertion, /
    ) -> PublicKeyAuthenticationResult:
        raise NotImplementedError


__all__ = ["PublicKeyAssertionVerificationBase"]
