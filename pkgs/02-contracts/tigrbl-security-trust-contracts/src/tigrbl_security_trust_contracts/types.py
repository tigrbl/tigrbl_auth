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
        if not isinstance(jwk_thumbprint, str) and hasattr(
            jwk_thumbprint, "confirmation_claim"
        ):
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


@dataclass(frozen=True, slots=True)
class AuthorizationDecisionTrace:
    """Deterministic authorization decision artifact shape."""

    request_hash: str
    policy_hash: str
    derivation_hash: str
    decision_key: str
    request: Mapping[str, Any]
    derived_grant: Mapping[str, Any]
    artifact_type: str = "authorization_decision_trace"
    artifact_version: int = 1

    def as_dict(self) -> dict[str, Any]:
        return {
            "artifact_type": self.artifact_type,
            "artifact_version": self.artifact_version,
            "request_hash": self.request_hash,
            "policy_hash": self.policy_hash,
            "derivation_hash": self.derivation_hash,
            "decision_key": self.decision_key,
            "request": dict(self.request),
            "derived_grant": dict(self.derived_grant),
        }


@dataclass(frozen=True, slots=True)
class DelegationProvenance:
    """Deterministic delegation lineage artifact shape."""

    lineage_id: str
    subject_token_hash: str
    actor_token_hash: str | None
    nodes: Mapping[str, Any]
    edge: Mapping[str, Any]
    artifact_type: str = "delegation_provenance"
    artifact_version: int = 1

    def as_dict(self) -> dict[str, Any]:
        return {
            "artifact_type": self.artifact_type,
            "artifact_version": self.artifact_version,
            "lineage_id": self.lineage_id,
            "subject_token_hash": self.subject_token_hash,
            "actor_token_hash": self.actor_token_hash,
            "nodes": dict(self.nodes),
            "edge": dict(self.edge),
        }

from . import _artifact_types
from ._artifact_types import *  # noqa: F401,F403

__all__ = _artifact_types.__all__

