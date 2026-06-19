"""Horizontal protocol contracts for security/trust domains."""

from __future__ import annotations

from typing import Any, Mapping, Protocol, Sequence

from .types import (
    Alg,
    Artifact,
    CanonicalizeRequest,
    CapabilityMap,
    DeriveKeyRequest,
    ExportKeyRequest,
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
    RewrapRequest,
    VerificationResult,
    VerifyRequest,
    IssueRequest,
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
