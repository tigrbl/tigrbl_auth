"""Domain base classes composed from the horizontal security/trust contracts."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping, Sequence

from tigrbl_identity_contracts.oidc import (
    ClaimsProviderPort,
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


class ClaimsProviderBase(ClaimsProviderPort, CapabilityProviderBase):
    """Base for provider-style claims assembly."""

    async def claims(self, request: Any) -> Any:
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


class KeyLifecycleProviderBase(IKeyLifecycleProvider, CapabilityProviderBase):
    """Base for provider-neutral key creation, import, rotation, and destruction."""

    async def create_key(self, spec: KeySpec) -> KeyHandle:
        raise NotImplementedError

    async def import_key(
        self,
        spec: KeySpec,
        material: bytes,
        *,
        public: bytes | None = None,
    ) -> KeyHandle:
        raise NotImplementedError

    async def rotate_key(
        self,
        kid: str,
        *,
        spec_overrides: Mapping[str, Any] | None = None,
    ) -> KeyHandle:
        raise NotImplementedError

    async def destroy_key(self, kid: str, version: int | None = None) -> bool:
        raise NotImplementedError


class KeyResolverBase(IKeyResolver, CapabilityProviderBase):
    """Base for resolving opaque key references into provider handles."""

    async def resolve_key(
        self,
        ref: KeyRefLike,
        *,
        include_secret: bool = False,
    ) -> KeyRefLike:
        raise NotImplementedError


class EncryptionProviderBase(IEncryptionProvider, CapabilityProviderBase):
    """Base for data encryption and decryption providers."""

    async def encrypt(self, request: EncryptRequest) -> Artifact:
        raise NotImplementedError

    async def decrypt(self, request: DecryptRequest) -> bytes:
        raise NotImplementedError


class KeyWrappingProviderBase(IKeyWrappingProvider, CapabilityProviderBase):
    """Base for key wrapping and unwrapping providers."""

    async def wrap_key(self, request: WrapKeyRequest) -> WrappedKeyMaterial:
        raise NotImplementedError

    async def unwrap_key(self, request: UnwrapKeyRequest) -> KeyMaterial:
        raise NotImplementedError


class KeyEncapsulationProviderBase(IKeyEncapsulationProvider, CapabilityProviderBase):
    """Base for KEM encapsulation and decapsulation providers."""

    async def encapsulate(self, request: EncapsulateRequest) -> EncapsulationResult:
        raise NotImplementedError

    async def decapsulate(self, request: DecapsulateRequest) -> bytes:
        raise NotImplementedError


class AttestationProviderBase(IAttestationProvider, CapabilityProviderBase):
    """Base for key attestation and evidence verification providers."""

    async def attest_key(self, request: AttestKeyRequest) -> AttestationEvidence:
        raise NotImplementedError

    async def verify_attestation(
        self,
        request: VerifyAttestationRequest,
    ) -> VerificationResult:
        raise NotImplementedError


class PublicKeyExporterBase(IPublicKeyExporter, CapabilityProviderBase):
    """Base for public key material export."""

    async def export_public_key(
        self,
        request: ExportPublicKeyRequest,
    ) -> ExportPublicKeyResult:
        raise NotImplementedError


class CryptoKeyProviderBase(
    KeyLifecycleProviderBase,
    KeyResolverBase,
    SigningProviderBase,
    EncryptionProviderBase,
    KeyWrappingProviderBase,
    KeyEncapsulationProviderBase,
    AttestationProviderBase,
    PublicKeyExporterBase,
):
    """Composite base for providers that intentionally implement the full key surface."""


class CipherPolicyDomainBase(ICipherPolicy, CapabilityProviderBase):
    """Domain base for cipher-suite policy, defaults, dialect mapping, and linting."""

    @abstractmethod
    def suite_id(self) -> str: ...

    @abstractmethod
    def default_alg(self, op: str, *, for_key: KeyRefLike | None = None) -> str: ...

    @abstractmethod
    def normalize(
        self,
        *,
        op: str,
        alg: str | None = None,
        key: KeyRefLike | None = None,
        params: Mapping[str, Any] | None = None,
        dialect: str | None = None,
    ) -> NormalizedDescriptor: ...

    def policy(self) -> Mapping[str, Any]:
        raise NotImplementedError

    def features(self) -> Mapping[str, Any]:
        raise NotImplementedError

    def lint(self) -> Sequence[str]:
        return self._lint()

    def _lint(self) -> Sequence[str]:
        issues: list[str] = []
        supported = self.supports().ops
        for op, allowed in supported.items():
            try:
                default = self.default_alg(op)
            except Exception as exc:  # pragma: no cover - defensive base behavior
                issues.append(f"default_alg({op}) raised: {exc!r}")
                continue
            if default not in set(allowed):
                issues.append(
                    f"default_alg({op})={default} not in supports().ops[{op}]"
                )
        return tuple(issues)


class ConfirmationBindingValidatorBase(
    IConfirmationBindingValidator, CapabilityProviderBase
):
    """Base for proof confirmation validators such as DPoP or mTLS cnf checks."""

    @property
    @abstractmethod
    def confirmation_member(self) -> str: ...

    def validate_confirmation(
        self,
        cnf: Mapping[str, Any],
        binding: ProofBinding | None,
    ) -> bool:
        raise NotImplementedError


class SenderConstraintValidatorBase(ISenderConstraintValidator, CapabilityProviderBase):
    """Base for composing sender-constraint validation providers."""

    def validate(
        self,
        cnf: Mapping[str, Any],
        *,
        dpop: DPoPBinding | None = None,
        mtls: MTLSBinding | None = None,
        require_dpop: bool = False,
        require_mtls: bool = False,
    ) -> bool:
        raise NotImplementedError


class VerificationKeyResolverBase(IVerificationKeyResolver, CapabilityProviderBase):
    """Base for verification key resolution."""

    def get(self, key_id: str) -> Mapping[str, Any]:
        raise NotImplementedError


class VerificationKeyCacheBase(IVerificationKeyCache, VerificationKeyResolverBase):
    """Base for mutable verification-key caches independent of source format."""

    @property
    def keys(self) -> Mapping[str, Mapping[str, Any]]:
        raise NotImplementedError

    def put(self, key_id: str, key: Mapping[str, Any]) -> None:
        raise NotImplementedError

    def put_many(self, keys: Mapping[str, Mapping[str, Any]]) -> None:
        for key_id, key in keys.items():
            self.put(key_id, key)


class TokenIntrospectionClientBase(ITokenIntrospectionClient, CapabilityProviderBase):
    """Base for provider-neutral token introspection clients."""

    def introspect(
        self,
        request: TokenIntrospectionRequest,
    ) -> TokenIntrospectionResult:
        raise NotImplementedError
