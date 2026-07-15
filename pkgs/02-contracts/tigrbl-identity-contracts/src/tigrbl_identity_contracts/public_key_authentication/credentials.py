"""Stable public-key credential contracts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CredentialLifecycleStatus(str, Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    SUSPENDED = "suspended"


@dataclass(frozen=True, slots=True)
class CredentialDescriptor:
    external_id: bytes
    transports: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class CredentialBinding:
    tenant_id: str
    rp_id: str
    principal_id: str | None = None
    user_handle: bytes | None = None


@dataclass(frozen=True, slots=True)
class PublicKeyCredentialSource:
    credential_id: str
    external_id: bytes
    public_key: bytes
    algorithm: int
    binding: CredentialBinding
    sign_count: int = 0
    transports: tuple[str, ...] = ()
    discoverable: bool = False
    backup_eligible: bool = False
    backup_state: bool = False
    status: CredentialLifecycleStatus = CredentialLifecycleStatus.ACTIVE


PublicKeyCredential = PublicKeyCredentialSource

__all__ = [
    "CredentialBinding",
    "CredentialDescriptor",
    "CredentialLifecycleStatus",
    "PublicKeyCredential",
    "PublicKeyCredentialSource",
]
