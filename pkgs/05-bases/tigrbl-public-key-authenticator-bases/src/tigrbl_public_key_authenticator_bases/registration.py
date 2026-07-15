from abc import ABC

from tigrbl_identity_contracts.public_key_authentication import (
    CredentialRegistrationResult,
    PublicKeyRegistrationIntent,
    PublicKeyRegistrationOptions,
    VerifiedCredentialRegistration,
)


class PublicKeyCredentialRegistrationBase(ABC):
    async def begin_registration(
        self, intent: PublicKeyRegistrationIntent, /
    ) -> PublicKeyRegistrationOptions:
        raise NotImplementedError

    async def complete_registration(
        self, registration: VerifiedCredentialRegistration, /
    ) -> CredentialRegistrationResult:
        raise NotImplementedError


__all__ = ["PublicKeyCredentialRegistrationBase"]
