"""Canonical ports for public-key registration and authentication."""

from __future__ import annotations

from datetime import datetime
from typing import Protocol, runtime_checkable

from .attestation import (
    AttestationTrustResult,
    AuthenticatorAttestation,
    AuthenticatorMetadataResult,
)
from .ceremonies import CeremonyConsumption, CeremonyReservation
from .credentials import PublicKeyCredentialSource


@runtime_checkable
class CeremonyStatePort(Protocol):
    async def reserve(
        self, reservation: CeremonyReservation, /
    ) -> CeremonyReservation: ...
    async def load(self, ceremony_id: str, /) -> CeremonyReservation | None: ...
    async def consume(
        self, consumption: CeremonyConsumption, /
    ) -> CeremonyConsumption: ...
    async def fail(self, ceremony_id: str, reason: str, /) -> None: ...


@runtime_checkable
class PublicKeyCredentialStorePort(Protocol):
    async def insert(
        self, credential: PublicKeyCredentialSource, /
    ) -> PublicKeyCredentialSource: ...
    async def update_assertion_state(
        self,
        credential_id: str,
        *,
        sign_count: int,
        backup_state: bool,
        used_at: datetime,
    ) -> PublicKeyCredentialSource: ...
    async def revoke(self, credential_id: str, /) -> None: ...


@runtime_checkable
class PublicKeyCredentialLookupPort(Protocol):
    async def find_by_external_id(
        self, tenant_id: str, rp_id: str, external_id: bytes, /
    ) -> PublicKeyCredentialSource | None: ...
    async def list_for_principal(
        self, tenant_id: str, principal_id: str, rp_id: str, /
    ) -> tuple[PublicKeyCredentialSource, ...]: ...


@runtime_checkable
class PublicKeySignatureVerifierPort(Protocol):
    def verify(
        self,
        *,
        public_key: bytes,
        algorithm: int,
        message: bytes,
        signature: bytes,
    ) -> bool: ...


@runtime_checkable
class AttestationStatementVerifierPort(Protocol):
    def verify(
        self, attestation: AuthenticatorAttestation, /
    ) -> AttestationTrustResult: ...


@runtime_checkable
class AuthenticatorMetadataProviderPort(Protocol):
    async def resolve(self, aaguid: bytes, /) -> AuthenticatorMetadataResult: ...


@runtime_checkable
class RelyingPartyConfigurationPort(Protocol):
    async def resolve(self, tenant_id: str, rp_id: str, /) -> object | None: ...


@runtime_checkable
class OriginPolicyPort(Protocol):
    def allows(self, *, rp_id: str, origin: str) -> bool: ...


__all__ = [
    "AttestationStatementVerifierPort",
    "AuthenticatorMetadataProviderPort",
    "CeremonyStatePort",
    "OriginPolicyPort",
    "PublicKeyCredentialLookupPort",
    "PublicKeyCredentialStorePort",
    "PublicKeySignatureVerifierPort",
    "RelyingPartyConfigurationPort",
]
