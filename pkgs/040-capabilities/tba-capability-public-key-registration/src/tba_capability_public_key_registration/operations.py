from collections.abc import Awaitable, Callable
from typing import TypeAlias

from tba_contracts_identity.public_key_authentication import (
    CredentialRegistrationResult,
    PublicKeyRegistrationIntent,
    PublicKeyRegistrationOptions,
    VerifiedCredentialRegistration,
)

BeginRegistration: TypeAlias = Callable[
    [PublicKeyRegistrationIntent],
    PublicKeyRegistrationOptions | Awaitable[PublicKeyRegistrationOptions],
]
CompleteRegistration: TypeAlias = Callable[
    [VerifiedCredentialRegistration],
    CredentialRegistrationResult | Awaitable[CredentialRegistrationResult],
]

__all__ = ["BeginRegistration", "CompleteRegistration"]
