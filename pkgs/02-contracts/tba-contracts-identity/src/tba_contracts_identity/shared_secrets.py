"""Protocol-neutral shared-secret hashing and verification contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, TypeAlias, runtime_checkable


EncodedSecretHash: TypeAlias = bytes | str


@dataclass(frozen=True, slots=True)
class SecretHashPolicy:
    algorithm: str
    work_factor: int
    maximum_input_bytes: int | None = None


@dataclass(frozen=True, slots=True)
class SecretHash:
    encoded: EncodedSecretHash
    algorithm: str


@dataclass(frozen=True, slots=True)
class SecretVerificationResult:
    verified: bool
    algorithm: str | None = None
    needs_rehash: bool = False


@runtime_checkable
class SecretHashingPort(Protocol):
    policy: SecretHashPolicy

    def hash_secret(self, presented: str | bytes, /) -> SecretHash: ...


@runtime_checkable
class SecretVerificationPort(Protocol):
    def verify_secret(
        self,
        presented: str | bytes,
        expected: SecretHash | EncodedSecretHash | None,
        /,
    ) -> SecretVerificationResult: ...


__all__ = [
    "EncodedSecretHash",
    "SecretHash",
    "SecretHashPolicy",
    "SecretHashingPort",
    "SecretVerificationPort",
    "SecretVerificationResult",
]
