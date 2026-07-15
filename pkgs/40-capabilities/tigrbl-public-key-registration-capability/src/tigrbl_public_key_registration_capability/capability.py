from __future__ import annotations

import inspect

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
    CapabilityState,
)
from tigrbl_identity_contracts.public_key_authentication import (
    CredentialRegistrationResult,
    PublicKeyRegistrationIntent,
    PublicKeyRegistrationOptions,
    VerifiedCredentialRegistration,
)

from .operations import BeginRegistration, CompleteRegistration


async def _resolve(value: object) -> object:
    return await value if inspect.isawaitable(value) else value


class PublicKeyRegistrationCapability(Capability):
    def __init__(
        self, begin: BeginRegistration | None, complete: CompleteRegistration | None
    ) -> None:
        self._begin = begin
        self._complete = complete
        ready = begin is not None and complete is not None
        super().__init__(
            CapabilityDefinition("credential.public-key.registration", "1.0"),
            operations={
                "begin_public_key_registration": CapabilityOperation(
                    target=self.begin if begin else None, delegated=True
                ),
                "complete_public_key_registration": CapabilityOperation(
                    target=self.complete if complete else None, delegated=True
                ),
            },
            state=lambda: CapabilityState(
                ready=ready, status="ready" if ready else "unbound"
            ),
        )

    async def begin(
        self, intent: PublicKeyRegistrationIntent
    ) -> PublicKeyRegistrationOptions:
        if self._begin is None:
            raise NotImplementedError("registration begin target is not bound")
        value = await _resolve(self._begin(intent))
        if not isinstance(value, PublicKeyRegistrationOptions):
            raise TypeError(
                "registration begin target must return PublicKeyRegistrationOptions"
            )
        return value

    async def complete(
        self, registration: VerifiedCredentialRegistration
    ) -> CredentialRegistrationResult:
        if self._complete is None:
            raise NotImplementedError("registration completion target is not bound")
        value = await _resolve(self._complete(registration))
        if not isinstance(value, CredentialRegistrationResult):
            raise TypeError(
                "registration completion target must return CredentialRegistrationResult"
            )
        return value


__all__ = ["PublicKeyRegistrationCapability"]
