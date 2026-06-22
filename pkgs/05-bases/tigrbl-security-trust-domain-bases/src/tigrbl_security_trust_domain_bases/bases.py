"""Domain base classes composed from the horizontal security/trust contracts."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping, Sequence

from tigrbl_security_trust_contracts import (
    Artifact,
    CanonicalizeRequest,
    CapabilityMap,
    CertificateRequest,
    CertificateVerifyRequest,
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
    TokenIssueRequest,
    TokenVerifyRequest,
    VerificationResult,
    VerifyRequest,
    MTLSBinding,
)


class CapabilityProviderBase(ABC):
    """Base for providers that advertise executable capability."""

    @abstractmethod
    def supports(self) -> CapabilityMap: ...


class ArtifactCodecBase(ABC):
    """Base for parsers and deterministic canonicalizers."""

    async def parse(self, request: ParseRequest) -> ParsedArtifact:
        raise NotImplementedError

    async def canonicalize(self, request: CanonicalizeRequest) -> bytes:
        raise NotImplementedError


class ArtifactIssuerBase(ABC):
    """Base for providers that produce generic artifacts."""

    async def issue(self, request: IssueRequest) -> Artifact:
        raise NotImplementedError


class ArtifactVerifierBase(ABC):
    """Base for providers that verify generic artifacts."""

    async def verify(self, request: VerifyRequest) -> VerificationResult:
        raise NotImplementedError


class ArtifactOpenerBase(ABC):
    """Base for providers that open protected artifacts."""

    async def open(self, request: OpenRequest) -> OpenResult:
        raise NotImplementedError


class RecipientSetEditorBase(ABC):
    """Base for recipient-set mutation on multi-recipient envelopes."""

    async def rewrap(self, request: RewrapRequest) -> Artifact:
        raise NotImplementedError


class SigningDomainBase(
    CapabilityProviderBase, ArtifactIssuerBase, ArtifactVerifierBase, ArtifactCodecBase
):
    """Domain composition for detached or attached signing providers."""


class ProofOfPossessionDomainBase(
    CapabilityProviderBase, ArtifactIssuerBase, ArtifactVerifierBase
):
    """Domain composition for request-bound proof-of-possession providers."""


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
    CapabilityProviderBase, ArtifactIssuerBase, ArtifactOpenerBase, RecipientSetEditorBase
):
    """Domain composition for multi-recipient encryption providers."""


class KeyProviderDomainBase(CapabilityProviderBase):
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


class CipherPolicyDomainBase(CapabilityProviderBase):
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
                issues.append(f"default_alg({op})={default} not in supports().ops[{op}]")
        return tuple(issues)


class ConfirmationBindingValidatorBase(CapabilityProviderBase):
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


class SenderConstraintValidatorBase(CapabilityProviderBase):
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


class VerificationKeyResolverBase(CapabilityProviderBase):
    """Base for verification key resolution and JWKS-backed caches."""

    def get(self, kid: str) -> Mapping[str, Any]:
        raise NotImplementedError


class JWKSCacheBase(VerificationKeyResolverBase):
    """Base for mutable JWKS verification key caches."""

    @property
    def keys(self) -> Mapping[str, Mapping[str, Any]]:
        raise NotImplementedError

    def put_jwks(self, jwks: Mapping[str, Any]) -> None:
        raise NotImplementedError


class TokenIntrospectionClientBase(CapabilityProviderBase):
    """Base for provider-neutral token introspection clients."""

    def introspect(
        self,
        request: TokenIntrospectionRequest,
    ) -> TokenIntrospectionResult:
        raise NotImplementedError
