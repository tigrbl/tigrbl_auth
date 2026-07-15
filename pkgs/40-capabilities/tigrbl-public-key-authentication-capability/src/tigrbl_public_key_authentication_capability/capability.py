from __future__ import annotations

import inspect

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
    CapabilityState,
)
from tigrbl_identity_contracts.public_key_authentication import (
    PublicKeyAuthenticationIntent,
    PublicKeyAuthenticationOptions,
    PublicKeyAuthenticationResult,
    VerifiedPublicKeyAssertion,
)

from .operations import BeginAuthentication, CompleteAuthentication


async def _resolve(value: object) -> object:
    return await value if inspect.isawaitable(value) else value


class PublicKeyAuthenticationCapability(Capability):
    def __init__(
        self, begin: BeginAuthentication | None, complete: CompleteAuthentication | None
    ) -> None:
        self._begin = begin
        self._complete = complete
        ready = begin is not None and complete is not None
        super().__init__(
            CapabilityDefinition("credential.public-key.authentication", "1.0"),
            operations={
                "begin_public_key_authentication": CapabilityOperation(
                    target=self.begin if begin else None, delegated=True
                ),
                "complete_public_key_authentication": CapabilityOperation(
                    target=self.complete if complete else None, delegated=True
                ),
            },
            state=lambda: CapabilityState(
                ready=ready, status="ready" if ready else "unbound"
            ),
        )

    async def begin(
        self, intent: PublicKeyAuthenticationIntent
    ) -> PublicKeyAuthenticationOptions:
        if self._begin is None:
            raise NotImplementedError("authentication begin target is not bound")
        value = await _resolve(self._begin(intent))
        if not isinstance(value, PublicKeyAuthenticationOptions):
            raise TypeError(
                "authentication begin target must return PublicKeyAuthenticationOptions"
            )
        return value

    async def complete(
        self, assertion: VerifiedPublicKeyAssertion
    ) -> PublicKeyAuthenticationResult:
        if self._complete is None:
            raise NotImplementedError("authentication completion target is not bound")
        value = await _resolve(self._complete(assertion))
        if not isinstance(value, PublicKeyAuthenticationResult):
            raise TypeError(
                "authentication completion target must return PublicKeyAuthenticationResult"
            )
        return value


__all__ = ["PublicKeyAuthenticationCapability"]
