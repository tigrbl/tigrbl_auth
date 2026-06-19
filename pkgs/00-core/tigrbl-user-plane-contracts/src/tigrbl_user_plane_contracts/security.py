"""Shared DTOs for the security/trust horizontal contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, Sequence, TypeAlias

Alg: TypeAlias = str
ArtifactKind: TypeAlias = str
ArtifactFormat: TypeAlias = str
Canon: TypeAlias = str
Operation: TypeAlias = str
KeyRefLike: TypeAlias = str | bytes | Mapping[str, Any]


@dataclass(frozen=True)
class CapabilityMap:
    """Normalized capability advertisement shared by all provider contracts."""

    ops: Mapping[Operation, Sequence[Alg]] = field(default_factory=dict)
    formats: Sequence[ArtifactFormat] = ()
    algs: Sequence[Alg] = ()
    modes: Sequence[str] = ()
    canons: Sequence[Canon] = ()
    features: Sequence[str] = ()


@dataclass(frozen=True)
class Artifact:
    """Common artifact envelope for signatures, tokens, certs, ciphertexts, and proofs."""

    kind: ArtifactKind
    format: ArtifactFormat
    bytes_value: bytes | None = None
    text_value: str | None = None
    structured: Mapping[str, Any] | None = None
    meta: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class IssueRequest:
    """Input to generic artifact production."""

    op: Operation
    payload: Any | None = None
    key: KeyRefLike | None = None
    alg: Alg | None = None
    format: ArtifactFormat | None = None
    canon: Canon | None = None
    context: Mapping[str, Any] = field(default_factory=dict)
    policy: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class VerifyRequest:
    """Input to generic artifact verification."""

    artifact: Artifact
    payload: Any | None = None
    key: KeyRefLike | None = None
    context: Mapping[str, Any] = field(default_factory=dict)
    policy: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class VerificationResult:
    """Common verification outcome."""

    valid: bool
    reason: str | None = None
    claims: Mapping[str, Any] | None = None
    subject: Mapping[str, Any] | None = None
    meta: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class OpenRequest:
    """Input to opening protected artifacts such as ciphertexts and envelopes."""

    artifact: Artifact
    key: KeyRefLike | None = None
    identities: Sequence[KeyRefLike] = ()
    aad: bytes | None = None
    policy: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class OpenResult:
    """Output from opening protected artifacts."""

    plaintext: bytes | None = None
    material: bytes | None = None
    meta: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ParseRequest:
    """Input to artifact parsing."""

    artifact: Artifact
    trusted: bool = False
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ParsedArtifact:
    """Structured parse result; trust depends on caller-selected verification."""

    kind: ArtifactKind
    format: ArtifactFormat
    header: Mapping[str, Any] = field(default_factory=dict)
    body: Mapping[str, Any] = field(default_factory=dict)
    meta: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CanonicalizeRequest:
    """Input to deterministic canonicalization before issuing or verifying."""

    payload: Any
    canon: Canon | None = None
    format: ArtifactFormat | None = None
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RewrapRequest:
    """Input to recipient-set mutation for multi-recipient envelopes."""

    artifact: Artifact
    add: Sequence[KeyRefLike] = ()
    remove: Sequence[str] = ()
    recipient_alg: Alg | None = None
    policy: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class NormalizedDescriptor:
    """Provider-ready cipher-policy decision."""

    op: Operation
    alg: Alg
    dialect: str | None = None
    mapped: Mapping[str, Any] = field(default_factory=dict)
    params: Mapping[str, Any] = field(default_factory=dict)
    constraints: Mapping[str, Any] = field(default_factory=dict)
    policy: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ListKeysRequest:
    """Input to generic key inventory discovery."""

    selector: Mapping[str, Any] = field(default_factory=dict)
    include_versions: bool = False
    include_disabled: bool = False
    cursor: str | None = None
    limit: int | None = None


@dataclass(frozen=True)
class KeyDescriptor:
    """Format-neutral key description."""

    kid: str
    version: int | None = None
    type: str | None = None
    alg: Alg | None = None
    uses: Sequence[str] = ()
    state: str | None = None
    export_policy: str | None = None
    fingerprint: str | None = None
    public: bytes | None = None
    uri: str | None = None
    tags: Mapping[str, str] = field(default_factory=dict)
    meta: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class KeyPage:
    """Paged key inventory result."""

    items: Sequence[KeyDescriptor]
    next_cursor: str | None = None


@dataclass(frozen=True)
class ExportKeyRequest:
    """Format-neutral key export request."""

    kid: str | None = None
    version: int | None = None
    ref: KeyRefLike | None = None
    format: ArtifactFormat = "raw-public"
    scope: str = "public"
    selector: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class KeyArtifact:
    """Exported key material in a requested format."""

    format: ArtifactFormat
    bytes_value: bytes | None = None
    text_value: str | None = None
    structured: Mapping[str, Any] | None = None
    meta: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DeriveKeyRequest:
    """Generic key-derivation request; the algorithm is data, not a method name."""

    alg: Alg
    input_key_material: bytes | KeyRefLike
    salt: bytes | None = None
    info: bytes | None = None
    length: int | None = None
    context: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class KeyMaterial:
    """Derived or generated key material."""

    material: bytes | None = None
    key: KeyRefLike | None = None
    alg: Alg | None = None
    length: int | None = None
    meta: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TokenIssueRequest:
    """Token-service issue request with claim semantics kept explicit."""

    claims: Mapping[str, Any]
    alg: Alg
    format: ArtifactFormat = "token"
    key: KeyRefLike | None = None
    kid: str | None = None
    headers: Mapping[str, Any] = field(default_factory=dict)
    issuer: str | None = None
    subject: str | None = None
    audience: str | Sequence[str] | None = None
    scope: str | Sequence[str] | None = None
    lifetime_s: int | None = 3600
    policy: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TokenVerifyRequest:
    """Token-service verification request."""

    token: str | bytes | Artifact
    issuer: str | None = None
    audience: str | Sequence[str] | None = None
    leeway_s: int = 60
    key: KeyRefLike | None = None
    policy: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CertificateRequest:
    """Certificate/CSR service request with X.509 semantics kept explicit."""

    op: Operation
    subject: Mapping[str, Any] = field(default_factory=dict)
    key: KeyRefLike | None = None
    csr: bytes | Artifact | None = None
    issuer: Mapping[str, Any] | None = None
    issuer_cert: bytes | Artifact | None = None
    serial: int | None = None
    not_before: int | None = None
    not_after: int | None = None
    san: Mapping[str, Any] = field(default_factory=dict)
    extensions: Mapping[str, Any] = field(default_factory=dict)
    sig_alg: Alg | None = None
    format: ArtifactFormat = "x509-pem"
    output_der: bool = False
    policy: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CertificateVerifyRequest:
    """Certificate verification request."""

    cert: bytes | Artifact
    trust_roots: Sequence[bytes | Artifact] = ()
    intermediates: Sequence[bytes | Artifact] = ()
    check_time: int | None = None
    check_revocation: bool = False
    policy: Mapping[str, Any] = field(default_factory=dict)
    opts: Mapping[str, Any] = field(default_factory=dict)


# Protocol contracts
"""Horizontal protocol contracts for security/trust domains."""


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
