from collections.abc import Awaitable, Callable
from typing import TypeAlias

AppraiseAttestation: TypeAlias = Callable[..., object | Awaitable[object]]
ResolveAuthenticatorMetadata: TypeAlias = Callable[..., object | Awaitable[object]]
ReappraiseAuthenticator: TypeAlias = Callable[..., object | Awaitable[object]]

__all__ = [
    "AppraiseAttestation",
    "ReappraiseAuthenticator",
    "ResolveAuthenticatorMetadata",
]
