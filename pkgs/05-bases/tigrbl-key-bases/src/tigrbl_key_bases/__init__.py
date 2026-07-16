"""Reusable key-provider bases."""

from abc import ABC
from typing import Any, Mapping

from tigrbl_security_trust_contracts import (
    AttestKeyRequest,
    AttestationEvidence,
    EncapsulateRequest,
    EncapsulationResult,
    ExportPublicKeyRequest,
    ExportPublicKeyResult,
    IAttestationProvider,
    ICapabilityProvider,
    IKeyEncapsulationProvider,
    IKeyLifecycleProvider,
    IKeyResolver,
    IKeyWrappingProvider,
    IPublicKeyExporter,
    KeyHandle,
    KeyMaterial,
    KeyRefLike,
    KeySpec,
    UnwrapKeyRequest,
    VerificationResult,
    VerifyAttestationRequest,
    WrappedKeyMaterial,
    WrapKeyRequest,
)
from tigrbl_signing_bases import SigningProviderBase


class KeyLifecycleProviderBase(IKeyLifecycleProvider, ICapabilityProvider, ABC):
    async def create_key(self, spec: KeySpec) -> KeyHandle:
        raise NotImplementedError

    async def import_key(self, spec: KeySpec, material: bytes, *, public: bytes | None = None) -> KeyHandle:
        raise NotImplementedError

    async def rotate_key(self, kid: str, *, spec_overrides: Mapping[str, Any] | None = None) -> KeyHandle:
        raise NotImplementedError

    async def destroy_key(self, kid: str, version: int | None = None) -> bool:
        raise NotImplementedError


class KeyResolverBase(IKeyResolver, ICapabilityProvider, ABC):
    async def resolve_key(self, ref: KeyRefLike, *, include_secret: bool = False) -> KeyRefLike:
        raise NotImplementedError


class KeyWrappingProviderBase(IKeyWrappingProvider, ICapabilityProvider, ABC):
    async def wrap_key(self, request: WrapKeyRequest) -> WrappedKeyMaterial:
        raise NotImplementedError

    async def unwrap_key(self, request: UnwrapKeyRequest) -> KeyMaterial:
        raise NotImplementedError


class KeyEncapsulationProviderBase(IKeyEncapsulationProvider, ICapabilityProvider, ABC):
    async def encapsulate(self, request: EncapsulateRequest) -> EncapsulationResult:
        raise NotImplementedError

    async def decapsulate(self, request) -> bytes:
        raise NotImplementedError


class AttestationProviderBase(IAttestationProvider, ICapabilityProvider, ABC):
    async def attest_key(self, request: AttestKeyRequest) -> AttestationEvidence:
        raise NotImplementedError

    async def verify_attestation(self, request: VerifyAttestationRequest) -> VerificationResult:
        raise NotImplementedError


class PublicKeyExporterBase(IPublicKeyExporter, ICapabilityProvider, ABC):
    async def export_public_key(self, request: ExportPublicKeyRequest) -> ExportPublicKeyResult:
        raise NotImplementedError


class CryptoKeyProviderBase(
    KeyLifecycleProviderBase,
    KeyResolverBase,
    SigningProviderBase,
    KeyWrappingProviderBase,
    KeyEncapsulationProviderBase,
    AttestationProviderBase,
    PublicKeyExporterBase,
):
    """Composite base for a provider intentionally implementing the full key surface."""


__all__ = [
    "AttestationProviderBase",
    "CryptoKeyProviderBase",
    "KeyEncapsulationProviderBase",
    "KeyLifecycleProviderBase",
    "KeyResolverBase",
    "KeyWrappingProviderBase",
    "PublicKeyExporterBase",
]
