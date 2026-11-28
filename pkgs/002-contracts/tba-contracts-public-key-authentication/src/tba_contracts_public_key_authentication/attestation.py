"""Canonical authenticator attestation contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping


class AttestationType(str, Enum):
    NONE = "none"
    SELF = "self"
    BASIC = "basic"
    ATTCA = "attca"
    ANONCA = "anonca"
    ENTERPRISE = "enterprise"


@dataclass(frozen=True, slots=True)
class AttestationFormat:
    identifier: str


@dataclass(frozen=True, slots=True)
class AuthenticatorAttestation:
    format: AttestationFormat
    statement: bytes
    authenticator_data: bytes
    client_data_hash: bytes
    aaguid: bytes | None = None
    credential_id: bytes | None = None
    credential_public_key: bytes | None = None
    rp_id_hash: bytes | None = None


@dataclass(frozen=True, slots=True)
class AttestationTrustResult:
    trusted: bool
    attestation_type: AttestationType
    trust_path: tuple[bytes, ...] = ()
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class AuthenticatorMetadataResult:
    aaguid: bytes
    found: bool
    status: str | None = None
    attributes: Mapping[str, object] = field(default_factory=dict)


__all__ = [
    "AttestationFormat",
    "AttestationTrustResult",
    "AttestationType",
    "AuthenticatorAttestation",
    "AuthenticatorMetadataResult",
]
