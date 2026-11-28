from collections.abc import Awaitable, Callable
from typing import TypeAlias

from tba_contracts_identity.public_key_authentication import (
    PublicKeyAuthenticationIntent,
    PublicKeyAuthenticationOptions,
    PublicKeyAuthenticationResult,
    VerifiedPublicKeyAssertion,
)

BeginAuthentication: TypeAlias = Callable[
    [PublicKeyAuthenticationIntent],
    PublicKeyAuthenticationOptions | Awaitable[PublicKeyAuthenticationOptions],
]
CompleteAuthentication: TypeAlias = Callable[
    [VerifiedPublicKeyAssertion],
    PublicKeyAuthenticationResult | Awaitable[PublicKeyAuthenticationResult],
]

__all__ = ["BeginAuthentication", "CompleteAuthentication"]
