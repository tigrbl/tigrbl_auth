"""Domain base classes composed from the horizontal security/trust contracts."""
# ruff: noqa: E402, F401

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping, Sequence

from tigrbl_identity_contracts.oidc import OidcFederationPort, WebFingerResolverPort
from tigrbl_identity_model_bases import SubjectIdentifierStrategyBase
from tigrbl_authentication_context_bases import AcrEvaluatorBase, AmrEvaluatorBase
from tigrbl_security_artifact_bases import (
    ProtectedArtifactOpenerBase as ArtifactOpenerBase,
    ProtectedArtifactVerifierBase as ArtifactVerifierBase,
    RecipientSetEditorBase,
    SecurityArtifactCodecBase as ArtifactCodecBase,
    SecurityArtifactIssuerBase as ArtifactIssuerBase,
)

from tigrbl_security_trust_contracts import (
    AcrEvaluationRequest,
    AcrEvaluationResult,
    AttestKeyRequest,
    AttestationEvidence,
    Artifact,
    AmrEvaluationRequest,
    AmrEvaluationResult,
    CanonicalizeRequest,
    CapabilityMap,
    CertificateRequest,
    CertificateVerifyRequest,
    DecapsulateRequest,
    DecryptRequest,
    DeriveKeyRequest,
    DPoPBinding,
    EncapsulateRequest,
    EncapsulationResult,
    EncryptRequest,
    ExportPublicKeyRequest,
    ExportPublicKeyResult,
    ExportKeyRequest,
    IssueRequest,
    KeyArtifact,
    KeyDescriptor,
    KeyHandle,
    KeyMaterial,
    KeyPage,
    KeyRefLike,
    KeySpec,
    ListKeysRequest,
    NormalizedDescriptor,
    OpenRequest,
    OpenResult,
    ParsedArtifact,
    ParseRequest,
    ProofBinding,
    RewrapRequest,
    SignRequest,
    SignResult,
    TokenIntrospectionRequest,
    TokenIntrospectionResult,
    TokenIssueRequest,
    TokenVerifyRequest,
    UnwrapKeyRequest,
    VerifyAttestationRequest,
    VerifySignatureRequest,
    VerifySignatureResult,
    VerificationResult,
    VerifyRequest,
    WrappedKeyMaterial,
    WrapKeyRequest,
    MTLSBinding,
    IAcrEvaluator,
    IAmrEvaluator,
    IArtifactCodec,
    IArtifactIssuer,
    IArtifactOpener,
    IArtifactVerifier,
    IAttestationProvider,
    ICapabilityProvider,
    ICipherPolicy,
    IConfirmationBindingValidator,
    IEncryptionProvider,
    IEntropySource,
    IKeyDeriver,
    IKeyDiscovery,
    IKeyEncapsulationProvider,
    IKeyExporter,
    IKeyLifecycle,
    IKeyLifecycleProvider,
    IKeyResolver,
    IKeyWrappingProvider,
    IPkceVerifier,
    IPublicKeyExporter,
    IRecipientSetEditor,
    ISenderConstraintValidator,
    ISigningProvider,
    ITokenIntrospectionClient,
    IVerificationKeyCache,
    IVerificationKeyResolver,
)


class CapabilityProviderBase(ICapabilityProvider, ABC):
    """Base for providers that advertise executable capability."""

    @abstractmethod
    def supports(self) -> CapabilityMap: ...


class SigningDomainBase(
    CapabilityProviderBase, ArtifactIssuerBase, ArtifactVerifierBase, ArtifactCodecBase
):
    """Domain composition for detached or attached signing providers."""


class SigningProviderBase(ISigningProvider, CapabilityProviderBase):
    """Base for provider-neutral signing and signature verification."""

    async def sign(self, request: SignRequest) -> SignResult:
        raise NotImplementedError

    async def verify_signature(
        self,
        request: VerifySignatureRequest,
    ) -> VerifySignatureResult:
        raise NotImplementedError


class ProofOfPossessionDomainBase(
    CapabilityProviderBase, ArtifactIssuerBase, ArtifactVerifierBase
):
    """Domain composition for request-bound proof-of-possession providers."""


class PkceVerifierBase(IPkceVerifier, CapabilityProviderBase):
    """Base for PKCE challenge verification providers."""

    def verify_challenge(self, *, verifier: str, challenge: str) -> bool:
        raise NotImplementedError


WebFingerResolverBase = WebFingerResolverPort
OidcFederationProviderBase = OidcFederationPort


class TokenServiceDomainBase(
    CapabilityProviderBase, ArtifactIssuerBase, ArtifactVerifierBase, ArtifactCodecBase
):
    """Token service base with claim-aware convenience methods."""

    async def issue_token(self, request: TokenIssueRequest) -> Artifact:
        raise NotImplementedError

    async def verify_token(self, request: TokenVerifyRequest) -> VerificationResult:
        raise NotImplementedError

    async def export_verification_keys(self, request: ExportKeyRequest) -> KeyArtifact:
        raise NotImplementedError


class TokenDomainBase(TokenServiceDomainBase):
    """Backward-compatible alias for token service domain composition."""


class CertificateServiceDomainBase(
    CapabilityProviderBase, ArtifactIssuerBase, ArtifactVerifierBase, ArtifactCodecBase
):
    """Certificate/CSR service base with X.509-aware convenience methods."""

    async def create_csr(self, request: CertificateRequest) -> Artifact:
        raise NotImplementedError

    async def issue_certificate(self, request: CertificateRequest) -> Artifact:
        raise NotImplementedError

    async def verify_certificate(
        self, request: CertificateVerifyRequest
    ) -> VerificationResult:
        raise NotImplementedError

    async def parse_certificate(self, request: ParseRequest) -> ParsedArtifact:
        raise NotImplementedError


class CertificateDomainBase(CertificateServiceDomainBase):
    """Backward-compatible alias for certificate service domain composition."""


class CryptoDomainBase(CapabilityProviderBase, ArtifactIssuerBase, ArtifactOpenerBase):
    """Domain composition for single-recipient crypto providers."""


class MreCryptoDomainBase(
    CapabilityProviderBase,
    ArtifactIssuerBase,
    ArtifactOpenerBase,
    RecipientSetEditorBase,
):
    """Domain composition for multi-recipient encryption providers."""


class KeyProviderDomainBase(
    IKeyResolver,
    IKeyLifecycle,
    IKeyLifecycleProvider,
    IKeyDiscovery,
    IKeyExporter,
    IEntropySource,
    IKeyDeriver,
    CapabilityProviderBase,
):
    """Domain composition for key lifecycle, resolution, discovery, export, entropy, and KDF."""

    async def resolve_key(
        self, ref: KeyRefLike, *, include_secret: bool = False
    ) -> KeyRefLike:
        raise NotImplementedError

    async def create_key(self, spec: Mapping[str, Any]) -> KeyRefLike:
        raise NotImplementedError

    async def import_key(
        self,
        spec: Mapping[str, Any],
        material: bytes,
        *,
        public: bytes | None = None,
    ) -> KeyRefLike:
        raise NotImplementedError

    async def rotate_key(
        self, kid: str, *, spec_overrides: Mapping[str, Any] | None = None
    ) -> KeyRefLike:
        raise NotImplementedError

    async def destroy_key(self, kid: str, version: int | None = None) -> bool:
        raise NotImplementedError

    async def get_key(
        self,
        kid: str,
        version: int | None = None,
        *,
        include_secret: bool = False,
    ) -> KeyRefLike:
        raise NotImplementedError

    async def list_keys(self, request: ListKeysRequest) -> KeyPage:
        raise NotImplementedError

    async def list_versions(self, kid: str) -> tuple[int, ...]:
        raise NotImplementedError

    async def describe_key(self, kid: str, version: int | None = None) -> KeyDescriptor:
        raise NotImplementedError

    async def export_key(self, request: ExportKeyRequest) -> KeyArtifact:
        raise NotImplementedError

    async def random_bytes(self, n: int) -> bytes:
        raise NotImplementedError

    async def derive_key(self, request: DeriveKeyRequest) -> KeyMaterial:
        raise NotImplementedError



from .key_bases import *  # noqa: F401,F403

