from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping, Protocol


class VerificationStatus(str, Enum):
    ALLOWED = "allowed"
    DENIED = "denied"


class ResourceServerError(RuntimeError):
    pass


class TokenValidationError(ResourceServerError):
    pass


def _normalize(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({value.strip() for value in values if value and value.strip()}))


def _required_text(value: str, field_name: str) -> str:
    cleaned = str(value).strip()
    if not cleaned:
        raise ValueError(f"{field_name} is required")
    return cleaned


@dataclass(frozen=True, slots=True)
class AccessTokenClaims:
    iss: str
    sub: str
    aud: tuple[str, ...]
    exp: int
    iat: int
    scope: tuple[str, ...] = ()
    cnf: Mapping[str, Any] = field(default_factory=dict)
    token_type: str = "access_token"

    def __post_init__(self) -> None:
        if not self.iss or not self.sub:
            raise ValueError("access token claims require issuer and subject")
        object.__setattr__(self, "aud", _normalize(self.aud))
        object.__setattr__(self, "scope", _normalize(self.scope))
        object.__setattr__(self, "cnf", dict(self.cnf))


@dataclass(frozen=True, slots=True)
class ResourceRequirement:
    issuer: str
    audience: str
    scopes: tuple[str, ...] = ()
    require_dpop: bool = False
    require_mtls: bool = False
    max_authz_staleness_seconds: int | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "scopes", _normalize(self.scopes))


@dataclass(frozen=True, slots=True)
class VerificationResult:
    status: VerificationStatus
    subject: str | None
    reason: str
    matched_scopes: tuple[str, ...] = ()
    policy_reference: str | None = None

    @property
    def allowed(self) -> bool:
        return self.status == VerificationStatus.ALLOWED


@dataclass(frozen=True, slots=True)
class DPoPBinding:
    jwk_thumbprint: str
    htm: str
    htu: str
    jti: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "jwk_thumbprint",
            _required_text(self.jwk_thumbprint, "DPoP JWK thumbprint"),
        )
        object.__setattr__(self, "htm", _required_text(self.htm, "DPoP htm").upper())
        object.__setattr__(self, "htu", _required_text(self.htu, "DPoP htu"))
        object.__setattr__(self, "jti", _required_text(self.jti, "DPoP jti"))


@dataclass(frozen=True, slots=True)
class MTLSBinding:
    certificate_thumbprint: str


class IntrospectionTransport(Protocol):
    def __call__(self, token: str) -> Mapping[str, Any]: ...


class PolicyHook(Protocol):
    def __call__(
        self,
        claims: AccessTokenClaims,
        requirement: ResourceRequirement,
    ) -> tuple[bool, str]: ...


@dataclass(frozen=True, slots=True)
class FrameworkRequest:
    authorization: str | None
    dpop: DPoPBinding | None = None
    mtls: MTLSBinding | None = None


@dataclass(frozen=True, slots=True)
class ProtectedResourceVerifierContract:
    verifier_logic_id: str
    issuer: str
    accepted_issuers: tuple[str, ...]
    resource: str
    accepted_audiences: tuple[str, ...]
    accepted_token_classes: tuple[str, ...]
    sender_constraint_modes: tuple[str, ...]
    sender_constraint_required: bool
    required_claims: tuple[str, ...]
    replay_expectation: str
    freshness_expectation: str
    introspection_auth_methods: tuple[str, ...]

    def as_metadata_projection(self) -> dict[str, object]:
        return {
            "resource": self.resource,
            "authorization_servers": list(self.accepted_issuers),
            "token_types_supported": list(self.accepted_token_classes),
            "proof_modes_supported": list(self.sender_constraint_modes),
            "proof_binding_required": self.sender_constraint_required,
            "required_claims": list(self.required_claims),
            "introspection_endpoint_auth_methods_supported": list(self.introspection_auth_methods),
            "verifier_logic": self.verifier_logic_id,
            "verification_freshness_expectation": self.freshness_expectation,
            "verification_replay_expectation": self.replay_expectation,
        }


@dataclass(frozen=True, slots=True)
class VerifierContractProfile:
    issuer: str
    audiences: tuple[str, ...]
    required_scopes: tuple[str, ...]
    allowed_algs: tuple[str, ...]
    jwks_uri: str
    introspection_endpoint: str
    max_authz_staleness_seconds: int
    clock_skew_seconds: int
    fail_closed: bool

    def resource_requirement(self) -> ResourceRequirement:
        if not self.audiences:
            raise ValueError("verifier contract has no accepted audience")
        return ResourceRequirement(
            issuer=self.issuer,
            audience=self.audiences[0],
            scopes=self.required_scopes,
            max_authz_staleness_seconds=self.max_authz_staleness_seconds,
        )


@dataclass(frozen=True, slots=True)
class CapabilityAttestation:
    version: str
    issuer: str
    product_surface: str | None
    profile: str
    capabilities: tuple[str, ...]
    routes: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    claim_ids: tuple[str, ...]
    generated_at: str
    artifact_sha256: str

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["capabilities"] = list(self.capabilities)
        payload["routes"] = list(self.routes)
        payload["evidence_ids"] = list(self.evidence_ids)
        payload["claim_ids"] = list(self.claim_ids)
        return payload


__all__ = [
    "AccessTokenClaims",
    "CapabilityAttestation",
    "DPoPBinding",
    "FrameworkRequest",
    "IntrospectionTransport",
    "MTLSBinding",
    "PolicyHook",
    "ProtectedResourceVerifierContract",
    "ResourceRequirement",
    "ResourceServerError",
    "TokenValidationError",
    "VerificationResult",
    "VerificationStatus",
    "VerifierContractProfile",
]
