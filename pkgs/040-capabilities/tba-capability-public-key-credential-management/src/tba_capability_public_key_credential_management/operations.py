from collections.abc import Awaitable, Callable
from typing import TypeAlias

ListCredentials: TypeAlias = Callable[..., object | Awaitable[object]]
RenameCredential: TypeAlias = Callable[..., object | Awaitable[object]]
RevokeCredential: TypeAlias = Callable[..., object | Awaitable[object]]

__all__ = ["ListCredentials", "RenameCredential", "RevokeCredential"]
