'Artifact operation and key-material value objects.'
from __future__ import annotations

from .types import *  # noqa: F401,F403

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


@dataclass(frozen=True, slots=True)
class PQCSignatureKeyPair:
    """Post-quantum signature key material returned by signing providers."""

    algorithm: str
    public_key: bytes
    secret_key: bytes
    library: str = "pqcrypto"


__all__ = [
    "Alg",
    "Artifact",
    "ArtifactFormat",
    "ArtifactKind",
    "AuthorizationDecisionTrace",
    "Canon",
    "CanonicalizeRequest",
    "CapabilityMap",
    "CertificateRequest",
    "CertificateVerifyRequest",
    "DeriveKeyRequest",
    "DelegationProvenance",
    "DPoPNonceRecord",
    "DPoPProofClaims",
    "ExportKeyRequest",
    "IssueRequest",
    "JWTPayload",
    "KeyArtifact",
    "KeyDescriptor",
    "KeyMaterial",
    "KeyPage",
    "KeyRefLike",
    "ListKeysRequest",
    "MTLSClientAuthentication",
    "NormalizedDescriptor",
    "OpenRequest",
    "OpenResult",
    "Operation",
    "DPoPBinding",
    "MTLSBinding",
    "PQCSignatureKeyPair",
    "ParsedArtifact",
    "ParseRequest",
    "ProofBinding",
    "RewrapRequest",
    "TokenIntrospectionRequest",
    "TokenIntrospectionResult",
    "TokenIssueRequest",
    "TokenVerifyRequest",
    "VerificationResult",
    "VerifyRequest",
]
