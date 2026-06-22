"""DTOs and type aliases for security/trust extension surfaces."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence, TypeAlias, TypedDict

Alg: TypeAlias = str
ArtifactKind: TypeAlias = str
ArtifactFormat: TypeAlias = str
Canon: TypeAlias = str
Operation: TypeAlias = str
KeyRefLike: TypeAlias = str | bytes | Mapping[str, Any]


class JWTPayload(TypedDict, total=False):
    """Neutral JWT claim-set contract; domain layers interpret claim semantics."""

    iss: str
    sub: str
    aud: str | Sequence[str]
    exp: int
    nbf: int
    iat: int
    jti: str
    typ: str
    tid: str
    scope: str
    cnf: Mapping[str, Any]


def _required_text(value: object, field_name: str) -> str:
    cleaned = str(value).strip()
    if not cleaned:
        raise ValueError(f"{field_name} is required")
    return cleaned


@dataclass(frozen=True)
class CapabilityMap:
    """Normalized capability advertisement shared by provider contracts."""

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


@dataclass(frozen=True, slots=True)
class ProofBinding:
    """Confirmation-claim binding for proof-of-possession and sender constraints."""

    method: str
    confirmation_claim: Mapping[str, str]
    credential_id: str | None = None

    def __post_init__(self) -> None:
        method = _required_text(self.method, "proof binding method").lower()
        if method not in {"dpop", "mtls"}:
            raise ValueError("proof binding method must be dpop or mtls")
        claim = {
            str(key).strip(): str(value).strip()
            for key, value in self.confirmation_claim.items()
            if str(key).strip() and str(value).strip()
        }
        if method == "dpop" and not claim.get("jkt"):
            raise ValueError("DPoP proof binding requires cnf.jkt")
        if method == "mtls" and not claim.get("x5t#S256"):
            raise ValueError("mTLS proof binding requires cnf.x5t#S256")
        object.__setattr__(self, "method", method)
        object.__setattr__(self, "confirmation_claim", claim)
        if self.credential_id is not None:
            object.__setattr__(
                self,
                "credential_id",
                _required_text(self.credential_id, "credential id"),
            )

    @classmethod
    def for_mtls(cls, credential: object) -> "ProofBinding":
        return cls(
            "mtls",
            getattr(credential, "confirmation_claim"),
            credential_id=getattr(credential, "id", None),
        )

    @classmethod
    def for_dpop(
        cls,
        jwk_thumbprint: str | object,
        *,
        credential_id: str | None = None,
    ) -> "ProofBinding":
        if not isinstance(jwk_thumbprint, str) and hasattr(jwk_thumbprint, "confirmation_claim"):
            return cls(
                "dpop",
                getattr(jwk_thumbprint, "confirmation_claim"),
                credential_id=getattr(jwk_thumbprint, "id", None),
            )
        return cls("dpop", {"jkt": str(jwk_thumbprint)}, credential_id=credential_id)


@dataclass(frozen=True, slots=True)
class DPoPProofClaims:
    """Parsed DPoP proof claim-set used by proof validators."""

    jti: str
    htm: str
    htu: str
    iat: int | None
    nonce: str | None
    ath: str | None
    jkt: str

    def as_dict(self) -> dict[str, object]:
        return {
            "jti": self.jti,
            "htm": self.htm,
            "htu": self.htu,
            "iat": self.iat,
            "nonce": self.nonce,
            "ath": self.ath,
            "jkt": self.jkt,
        }


@dataclass(frozen=True, slots=True)
class DPoPNonceRecord:
    """Issued nonce and expiry pair for DPoP nonce stores."""

    nonce: str
    expires_at: int


@dataclass(frozen=True, slots=True, kw_only=True)
class DPoPBinding(ProofBinding):
    """Presented DPoP proof binding material for request-bound validation."""

    jwk_thumbprint: str
    htm: str
    htu: str
    jti: str
    iat: int | None = None
    ath: str | None = None
    nonce: str | None = None
    method: str = "dpop"
    confirmation_claim: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        thumbprint = _required_text(self.jwk_thumbprint, "DPoP JWK thumbprint")
        object.__setattr__(self, "jwk_thumbprint", thumbprint)
        object.__setattr__(self, "htm", _required_text(self.htm, "DPoP htm").upper())
        object.__setattr__(self, "htu", _required_text(self.htu, "DPoP htu"))
        object.__setattr__(self, "jti", _required_text(self.jti, "DPoP jti"))
        if not self.confirmation_claim:
            object.__setattr__(self, "confirmation_claim", {"jkt": thumbprint})
        ProofBinding.__post_init__(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class MTLSBinding(ProofBinding):
    """Presented mTLS certificate binding material for request-bound validation."""

    certificate_thumbprint: str
    method: str = "mtls"
    confirmation_claim: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        thumbprint = _required_text(
            self.certificate_thumbprint, "mTLS certificate thumbprint"
        )
        object.__setattr__(self, "certificate_thumbprint", thumbprint)
        if not self.confirmation_claim:
            object.__setattr__(self, "confirmation_claim", {"x5t#S256": thumbprint})
        ProofBinding.__post_init__(self)


@dataclass(frozen=True, slots=True)
class MTLSClientAuthentication:
    """mTLS client-authentication result projected as a confirmation claim."""

    auth_method: str
    cert_thumbprint: str

    @property
    def confirmation_claim(self) -> dict[str, str]:
        return {"x5t#S256": str(self.cert_thumbprint)}


@dataclass(frozen=True, slots=True)
class TokenIntrospectionRequest:
    """Provider-neutral token introspection input."""

    token: str
    token_type_hint: str | None = None


@dataclass(frozen=True, slots=True)
class TokenIntrospectionResult:
    """Provider-neutral token introspection result."""

    active: bool
    claims: Mapping[str, Any] = field(default_factory=dict)


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
    "Canon",
    "CanonicalizeRequest",
    "CapabilityMap",
    "CertificateRequest",
    "CertificateVerifyRequest",
    "DeriveKeyRequest",
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
