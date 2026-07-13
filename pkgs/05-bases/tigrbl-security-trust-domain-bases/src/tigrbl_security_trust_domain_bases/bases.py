"""Domain base classes composed from the horizontal security/trust contracts."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping, Sequence

from tigrbl_identity_contracts.oidc import (
    OidcFederationPort,
    SubjectIdentifierStrategyPort,
    WebFingerResolverPort,
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


class ArtifactCodecBase(IArtifactCodec, ABC):
    """Base for parsers and deterministic canonicalizers."""

    async def parse(self, request: ParseRequest) -> ParsedArtifact:
        raise NotImplementedError

    async def canonicalize(self, request: CanonicalizeRequest) -> bytes:
        raise NotImplementedError


class ArtifactIssuerBase(IArtifactIssuer, ABC):
    """Base for providers that produce generic artifacts."""

    async def issue(self, request: IssueRequest) -> Artifact:
        raise NotImplementedError


class ArtifactVerifierBase(IArtifactVerifier, ABC):
    """Base for providers that verify generic artifacts."""

    async def verify(self, request: VerifyRequest) -> VerificationResult:
        raise NotImplementedError


class ArtifactOpenerBase(IArtifactOpener, ABC):
    """Base for providers that open protected artifacts."""

    async def open(self, request: OpenRequest) -> OpenResult:
        raise NotImplementedError


class RecipientSetEditorBase(IRecipientSetEditor, ABC):
    """Base for recipient-set mutation on multi-recipient envelopes."""

    async def rewrap(self, request: RewrapRequest) -> Artifact:
        raise NotImplementedError


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


class AcrEvaluatorBase(IAcrEvaluator, CapabilityProviderBase):
    """Base for Authentication Context Class Reference evaluators."""

    def evaluate_acr(self, request: AcrEvaluationRequest) -> AcrEvaluationResult:
        raise NotImplementedError


class AmrEvaluatorBase(IAmrEvaluator, CapabilityProviderBase):
    """Base for Authentication Methods References evaluators."""

    def evaluate_amr(self, request: AmrEvaluationRequest) -> AmrEvaluationResult:
        raise NotImplementedError


class SubjectIdentifierStrategyBase(
    SubjectIdentifierStrategyPort, CapabilityProviderBase
):
    """Base for public, pairwise, transient, and opaque subject strategies."""

    def derive(self, request: Any) -> Any:
        raise NotImplementedError


class WebFingerResolverBase(WebFingerResolverPort, CapabilityProviderBase):
    """Base for WebFinger discovery providers."""

    async def resolve(self, request: Any) -> Any:
        raise NotImplementedError


class OidcFederationProviderBase(OidcFederationPort, CapabilityProviderBase):
    """Base for OIDC Federation trust providers."""

    async def entity_statement(self, request: Any) -> Any:
        raise NotImplementedError


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

