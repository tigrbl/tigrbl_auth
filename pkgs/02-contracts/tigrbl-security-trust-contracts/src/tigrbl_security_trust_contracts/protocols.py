"""Protocol contracts for security/trust extension surfaces."""

from __future__ import annotations

from typing import Any, Mapping, Protocol, Sequence

from .keys import (
    AttestKeyRequest,
    AttestationEvidence,
    DecapsulateRequest,
    DecryptRequest,
    EncapsulateRequest,
    EncapsulationResult,
    EncryptRequest,
    ExportPublicKeyRequest,
    ExportPublicKeyResult,
    KeyHandle,
    KeySpec,
    SignRequest,
    SignResult,
    UnwrapKeyRequest,
    VerifyAttestationRequest,
    VerifySignatureRequest,
    VerifySignatureResult,
    WrappedKeyMaterial,
    WrapKeyRequest,
)
from .auth_context import (
    AcrEvaluationRequest,
    AcrEvaluationResult,
    AmrEvaluationRequest,
    AmrEvaluationResult,
)
from .types import (
    Alg,
    Artifact,
    AuthorizationDecisionTrace,
    CapabilityMap,
    CanonicalizeRequest,
    DelegationProvenance,
    DeriveKeyRequest,
    DPoPBinding,
    ExportKeyRequest,
    IssueRequest,
    KeyArtifact,
    KeyDescriptor,
    KeyMaterial,
    KeyPage,
    KeyRefLike,
    ListKeysRequest,
    NormalizedDescriptor,
    OpenRequest,
    OpenResult,
    ParsedArtifact,
    ParseRequest,
    ProofBinding,
    RewrapRequest,
    TokenIntrospectionRequest,
    TokenIntrospectionResult,
    VerificationResult,
    VerifyRequest,
    MTLSBinding,
)


class ICapabilityProvider(Protocol):
    """Provider capability discovery."""

    def supports(self) -> CapabilityMap: ...


class IArtifactIssuer(Protocol):
    """Artifact production: sign, mint, issue, encrypt, wrap, seal, prove."""

    async def issue(self, request: IssueRequest) -> Artifact: ...


class IArtifactVerifier(Protocol):
    """Artifact verification against payload/context/policy."""

    async def verify(self, request: VerifyRequest) -> VerificationResult: ...


class IArtifactOpener(Protocol):
    """Open protected artifacts into plaintext or key material."""

    async def open(self, request: OpenRequest) -> OpenResult: ...


class IArtifactCodec(Protocol):
    """Artifact parsing and payload canonicalization."""

    async def parse(self, request: ParseRequest) -> ParsedArtifact: ...

    async def canonicalize(self, request: CanonicalizeRequest) -> bytes: ...


class IRecipientSetEditor(Protocol):
    """Recipient-set mutation for multi-recipient envelopes."""

    async def rewrap(self, request: RewrapRequest) -> Artifact: ...


class IKeyResolver(Protocol):
    """Resolve opaque references into provider-specific key handles."""

    async def resolve_key(
        self, ref: KeyRefLike, *, include_secret: bool = False
    ) -> KeyRefLike: ...


class IKeyLifecycle(Protocol):
    """Key creation, import, rotation, destruction, and fetch lifecycle."""

    async def create_key(self, spec: Mapping[str, Any]) -> KeyRefLike: ...

    async def import_key(
        self,
        spec: Mapping[str, Any],
        material: bytes,
        *,
        public: bytes | None = None,
    ) -> KeyRefLike: ...

    async def rotate_key(
        self, kid: str, *, spec_overrides: Mapping[str, Any] | None = None
    ) -> KeyRefLike: ...

    async def destroy_key(self, kid: str, version: int | None = None) -> bool: ...

    async def get_key(
        self,
        kid: str,
        version: int | None = None,
        *,
        include_secret: bool = False,
    ) -> KeyRefLike: ...


class IKeyLifecycleProvider(Protocol):
    """Provider-neutral key lifecycle using explicit key DTOs."""

    async def create_key(self, spec: KeySpec) -> KeyHandle: ...

    async def import_key(
        self,
        spec: KeySpec,
        material: bytes,
        *,
        public: bytes | None = None,
    ) -> KeyHandle: ...

    async def rotate_key(
        self,
        kid: str,
        *,
        spec_overrides: Mapping[str, Any] | None = None,
    ) -> KeyHandle: ...

    async def destroy_key(self, kid: str, version: int | None = None) -> bool: ...


class IKeyDiscovery(Protocol):
    """Format-neutral key inventory and description."""

    async def list_keys(self, request: ListKeysRequest) -> KeyPage: ...

    async def list_versions(self, kid: str) -> tuple[int, ...]: ...

    async def describe_key(self, kid: str, version: int | None = None) -> KeyDescriptor: ...


class IKeyExporter(Protocol):
    """Export key material in requested formats such as PEM, SSH, JWK, JWKS, COSE, or DER."""

    async def export_key(self, request: ExportKeyRequest) -> KeyArtifact: ...


class IEntropySource(Protocol):
    """Cryptographic randomness source."""

    async def random_bytes(self, n: int) -> bytes: ...


class IKeyDeriver(Protocol):
    """Generic KDF surface; HKDF, PBKDF2, scrypt, etc. are selected by request.alg."""

    async def derive_key(self, request: DeriveKeyRequest) -> KeyMaterial: ...


class ISigningProvider(Protocol):
    """Provider-neutral signing and verification."""

    async def sign(self, request: SignRequest) -> SignResult: ...

    async def verify_signature(
        self,
        request: VerifySignatureRequest,
    ) -> VerifySignatureResult: ...


class IEncryptionProvider(Protocol):
    """Provider-neutral data encryption and decryption."""

    async def encrypt(self, request: EncryptRequest) -> Artifact: ...

    async def decrypt(self, request: DecryptRequest) -> bytes: ...


class IKeyWrappingProvider(Protocol):
    """Provider-neutral key wrapping and unwrapping."""

    async def wrap_key(self, request: WrapKeyRequest) -> WrappedKeyMaterial: ...

    async def unwrap_key(self, request: UnwrapKeyRequest) -> KeyMaterial: ...


class IKeyEncapsulationProvider(Protocol):
    """Provider-neutral KEM encapsulation and decapsulation."""

    async def encapsulate(self, request: EncapsulateRequest) -> EncapsulationResult: ...

    async def decapsulate(self, request: DecapsulateRequest) -> bytes: ...


class IAttestationProvider(Protocol):
    """Provider-neutral key attestation and evidence verification."""

    async def attest_key(self, request: AttestKeyRequest) -> AttestationEvidence: ...

    async def verify_attestation(
        self,
        request: VerifyAttestationRequest,
    ) -> VerificationResult: ...


class IPublicKeyExporter(Protocol):
    """Provider-neutral public key export."""

    async def export_public_key(
        self,
        request: ExportPublicKeyRequest,
    ) -> ExportPublicKeyResult: ...


class ICipherPolicy(Protocol):
    """Algorithm policy, defaults, dialect mapping, and linting."""

    def suite_id(self) -> str: ...

    def supports(self) -> CapabilityMap: ...

    def default_alg(self, op: str, *, for_key: KeyRefLike | None = None) -> Alg: ...

    def normalize(
        self,
        *,
        op: str,
        alg: Alg | None = None,
        key: KeyRefLike | None = None,
        params: Mapping[str, Any] | None = None,
        dialect: str | None = None,
    ) -> NormalizedDescriptor: ...

    def policy(self) -> Mapping[str, Any]: ...

    def features(self) -> Mapping[str, Any]: ...

    def lint(self) -> Sequence[str]: ...


class IConfirmationBindingValidator(Protocol):
    """Validate token confirmation material against a presented proof binding."""

    @property
    def confirmation_member(self) -> str: ...

    def validate_confirmation(
        self,
        cnf: Mapping[str, Any],
        binding: ProofBinding | None,
    ) -> bool: ...


class ISenderConstraintValidator(Protocol):
    """Compose supported sender-constraint proof checks."""

    def validate(
        self,
        cnf: Mapping[str, Any],
        *,
        dpop: DPoPBinding | None = None,
        mtls: MTLSBinding | None = None,
        require_dpop: bool = False,
        require_mtls: bool = False,
    ) -> bool: ...


class IVerificationKeyResolver(Protocol):
    """Resolve verification keys by key id or equivalent provider hint."""

    def get(self, key_id: str) -> Mapping[str, Any]: ...


class IVerificationKeyCache(IVerificationKeyResolver, Protocol):
    """Mutable verification-key cache independent of source format."""

    @property
    def keys(self) -> Mapping[str, Mapping[str, Any]]: ...

    def put(self, key_id: str, key: Mapping[str, Any]) -> None: ...

    def put_many(self, keys: Mapping[str, Mapping[str, Any]]) -> None: ...


class ITokenIntrospectionTransport(Protocol):
    """Provider-neutral token introspection transport."""

    def __call__(self, request: TokenIntrospectionRequest) -> TokenIntrospectionResult: ...


class ITokenIntrospectionClient(Protocol):
    """Provider-neutral token introspection client."""

    def introspect(self, request: TokenIntrospectionRequest) -> TokenIntrospectionResult: ...


class IProvenanceArtifactBuilder(Protocol):
    """Build deterministic authorization and delegation provenance artifacts."""

    def build_authorization_decision_trace(
        self,
        **kwargs: Any,
    ) -> AuthorizationDecisionTrace | Mapping[str, Any]: ...

    def build_delegation_provenance(
        self,
        **kwargs: Any,
    ) -> DelegationProvenance | Mapping[str, Any]: ...


class IPkceVerifier(Protocol):
    """PKCE S256 verifier contract."""

    def verify_challenge(self, *, verifier: str, challenge: str) -> bool: ...


class IAcrEvaluator(Protocol):
    """Authentication Context Class Reference evaluator."""

    def evaluate_acr(self, request: AcrEvaluationRequest) -> AcrEvaluationResult: ...


class IAmrEvaluator(Protocol):
    """Authentication Methods References evaluator."""

    def evaluate_amr(self, request: AmrEvaluationRequest) -> AmrEvaluationResult: ...


__all__ = [
    "IArtifactCodec",
    "IArtifactIssuer",
    "IArtifactOpener",
    "IArtifactVerifier",
    "ICapabilityProvider",
    "ICipherPolicy",
    "IConfirmationBindingValidator",
    "IEntropySource",
    "IAttestationProvider",
    "IEncryptionProvider",
    "IKeyEncapsulationProvider",
    "IKeyDeriver",
    "IKeyDiscovery",
    "IKeyExporter",
    "IKeyLifecycle",
    "IKeyLifecycleProvider",
    "IKeyResolver",
    "IKeyWrappingProvider",
    "IPublicKeyExporter",
    "IProvenanceArtifactBuilder",
    "IPkceVerifier",
    "IRecipientSetEditor",
    "ISigningProvider",
    "ISenderConstraintValidator",
    "ITokenIntrospectionClient",
    "ITokenIntrospectionTransport",
    "IVerificationKeyCache",
    "IVerificationKeyResolver",
    "IAcrEvaluator",
    "IAmrEvaluator",
]
