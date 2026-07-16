"""Canonical digital credential status contracts."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class CredentialStatusReference:
    method: str
    uri: str
    index: str | int | None = None


class CredentialStatusResolverPort(Protocol):
    def resolve(self, reference: CredentialStatusReference, /) -> str: ...


__all__ = ["CredentialStatusReference", "CredentialStatusResolverPort"]
