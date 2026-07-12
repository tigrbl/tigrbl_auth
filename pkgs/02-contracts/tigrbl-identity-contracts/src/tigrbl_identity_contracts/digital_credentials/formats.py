from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CredentialFormat:
    identifier: str
    media_type: str | None = None


@dataclass(frozen=True, slots=True)
class CredentialType:
    identifier: str
    format: CredentialFormat


__all__ = ["CredentialFormat", "CredentialType"]
