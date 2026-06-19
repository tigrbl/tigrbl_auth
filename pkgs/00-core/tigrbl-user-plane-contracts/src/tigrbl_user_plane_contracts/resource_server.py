from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from hmac import compare_digest
from typing import Any, Callable, Iterable, Mapping, Protocol


class VerificationStatus(str, Enum):
    ALLOWED = "allowed"
    DENIED = "denied"


class ResourceServerError(RuntimeError):
    pass


class TokenValidationError(ResourceServerError):
    pass


def _utc_timestamp() -> int:
    return int(datetime.now(tz=timezone.utc).timestamp())


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
    def __call__(self, claims: AccessTokenClaims, requirement: ResourceRequirement) -> tuple[bool, str]: ...


class JWKSCache:
    def __init__(self) -> None:
        self._keys: dict[str, Mapping[str, Any]] = {}

    @property
    def keys(self) -> Mapping[str, Mapping[str, Any]]:
        return dict(self._keys)

    def put_jwks(self, jwks: Mapping[str, Any]) -> None:
        for key in jwks.get("keys", []):
            kid = key.get("kid")
            if kid:
                self._keys[str(kid)] = dict(key)

    def get(self, kid: str) -> Mapping[str, Any]:
        try:
            return self._keys[kid]
        except KeyError as exc:
            raise TokenValidationError("unknown signing key") from exc


class IntrospectionClient:
    def __init__(self, transport: IntrospectionTransport) -> None:
        self.transport = transport

    def introspect(self, token: str) -> AccessTokenClaims:
        payload = dict(self.transport(token))
        if not payload.get("active"):
            raise TokenValidationError("introspection response is inactive")
        scope_value = payload.get("scope", ())
        scopes = tuple(scope_value.split()) if isinstance(scope_value, str) else tuple(scope_value)
        aud_value = payload.get("aud", ())
        audiences = (aud_value,) if isinstance(aud_value, str) else tuple(aud_value)
        return AccessTokenClaims(
            iss=str(payload["iss"]),
            sub=str(payload["sub"]),
            aud=audiences,
            exp=int(payload["exp"]),
            iat=int(payload.get("iat", 0)),
            scope=scopes,
            cnf=payload.get("cnf", {}),
        )


class ResourceServerVerifier:
    def __init__(
        self,
        *,
        jwks_cache: JWKSCache | None = None,
        introspection_client: IntrospectionClient | None = None,
        policy_hook: PolicyHook | None = None,
        now: Callable[[], int] = _utc_timestamp,
    ) -> None:
        self.jwks_cache = jwks_cache or JWKSCache()
        self.introspection_client = introspection_client
        self.policy_hook = policy_hook
        self.now = now

    def verify_claims(
        self,
        claims: AccessTokenClaims,
        requirement: ResourceRequirement,
        *,
        dpop: DPoPBinding | None = None,
        mtls: MTLSBinding | None = None,
    ) -> VerificationResult:
        try:
            self._validate_token_claims(claims, requirement)
            self._validate_proof_bindings(claims, requirement, dpop=dpop, mtls=mtls)
            policy_reference = None
            if self.policy_hook is not None:
                allowed, policy_reference = self.policy_hook(claims, requirement)
                if not allowed:
                    return VerificationResult(VerificationStatus.DENIED, claims.sub, "denied by policy hook", policy_reference=policy_reference)
        except TokenValidationError as exc:
            return VerificationResult(VerificationStatus.DENIED, claims.sub if isinstance(claims, AccessTokenClaims) else None, str(exc))
        return VerificationResult(
            VerificationStatus.ALLOWED,
            claims.sub,
            "allowed",
            matched_scopes=tuple(scope for scope in requirement.scopes if scope in claims.scope),
            policy_reference=policy_reference,
        )

    def verify_token(
        self,
        token: str | AccessTokenClaims,
        requirement: ResourceRequirement,
        *,
        dpop: DPoPBinding | None = None,
        mtls: MTLSBinding | None = None,
    ) -> VerificationResult:
        if isinstance(token, AccessTokenClaims):
            return self.verify_claims(token, requirement, dpop=dpop, mtls=mtls)
        if self.introspection_client is None:
            return VerificationResult(VerificationStatus.DENIED, None, "opaque token requires introspection client")
        return self.verify_claims(self.introspection_client.introspect(token), requirement, dpop=dpop, mtls=mtls)

    def _validate_token_claims(self, claims: AccessTokenClaims, requirement: ResourceRequirement) -> None:
        if claims.iss != requirement.issuer:
            raise TokenValidationError("issuer mismatch")
        if requirement.audience not in claims.aud:
            raise TokenValidationError("audience mismatch")
        if claims.exp <= self.now():
            raise TokenValidationError("token expired")
        if requirement.max_authz_staleness_seconds is not None:
            authz_iat = int(getattr(claims, "iat", 0))
            if self.now() - authz_iat > requirement.max_authz_staleness_seconds:
                raise TokenValidationError("authorization snapshot stale")
        missing = set(requirement.scopes) - set(claims.scope)
        if missing:
            raise TokenValidationError(f"missing required scopes: {', '.join(sorted(missing))}")

    @staticmethod
    def _validate_proof_bindings(
        claims: AccessTokenClaims,
        requirement: ResourceRequirement,
        *,
        dpop: DPoPBinding | None,
        mtls: MTLSBinding | None,
    ) -> None:
        if requirement.require_dpop:
            expected = str(claims.cnf.get("jkt") or "").strip()
            presented = str(getattr(dpop, "jwk_thumbprint", "") or "").strip()
            if dpop is None or not expected or not compare_digest(presented, expected):
                raise TokenValidationError("DPoP binding mismatch")
        if requirement.require_mtls:
            expected = str(claims.cnf.get("x5t#S256") or "").strip()
            presented = str(getattr(mtls, "certificate_thumbprint", "") or "").strip()
            if mtls is None or not expected or not compare_digest(presented, expected):
                raise TokenValidationError("mTLS binding mismatch")


@dataclass(frozen=True, slots=True)
class FrameworkRequest:
    authorization: str | None
    dpop: DPoPBinding | None = None
    mtls: MTLSBinding | None = None


def bearer_token_from_authorization(value: str | None) -> str | None:
    if not value:
        return None
    scheme, _, token = value.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    return token


def verify_framework_request(
    verifier: ResourceServerVerifier,
    request: FrameworkRequest,
    requirement: ResourceRequirement,
) -> VerificationResult:
    token = bearer_token_from_authorization(request.authorization)
    if token is None:
        return VerificationResult(VerificationStatus.DENIED, None, "missing bearer token")
    return verifier.verify_token(token, requirement, dpop=request.dpop, mtls=request.mtls)




@dataclass(frozen=True, slots=True)
class ProtectedResourceVerifierContract:
    verifier_logic_id: str
    issuer: str
    audiences: tuple[str, ...]
    required_scopes: tuple[str, ...]
    sender_constraint_required: bool
    dpop_supported: bool
    mtls_supported: bool
    jwks_uri: str
    introspection_endpoint: str | None
    introspection_auth_methods: tuple[str, ...]
    fail_closed: bool
    replay_expectation: str

    def as_metadata_projection(self) -> dict[str, object]:
        return {
            "issuer": self.issuer,
            "audiences": list(self.audiences),
            "required_scopes": list(self.required_scopes),
            "sender_constraint_required": self.sender_constraint_required,
            "dpop_supported": self.dpop_supported,
            "mtls_supported": self.mtls_supported,
            "jwks_uri": self.jwks_uri,
            "introspection_endpoint": self.introspection_endpoint,
            "introspection_auth_methods": list(self.introspection_auth_methods),
            "fail_closed": self.fail_closed,
        }


@dataclass(frozen=True, slots=True)
class VerifierContractProfile:
    issuer: str
    audiences: tuple[str, ...]
    scopes: tuple[str, ...]
    jwks_uri: str
    allowed_algs: tuple[str, ...]
    require_dpop: bool = False
    require_mtls: bool = False
    fail_closed: bool = True

    def resource_requirement(self) -> ResourceRequirement:
        return ResourceRequirement(
            issuer=self.issuer,
            audience=self.audiences[0] if self.audiences else "",
            scopes=self.scopes,
            require_dpop=self.require_dpop,
            require_mtls=self.require_mtls,
        )


@dataclass(frozen=True, slots=True)
class CapabilityAttestation:
    profile: str
    manifest_sha256: str
    runtime_metadata_sha256: str
    capability_truth: Mapping[str, bool]
    evidence_ids: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "profile": self.profile,
            "manifest_sha256": self.manifest_sha256,
            "runtime_metadata_sha256": self.runtime_metadata_sha256,
            "capability_truth": dict(self.capability_truth),
            "evidence_ids": list(self.evidence_ids),
        }


__all__ = [

    "AccessTokenClaims",
    "DPoPBinding",
    "FrameworkRequest",
    "IntrospectionClient",
    "IntrospectionTransport",
    "JWKSCache",
    "MTLSBinding",
    "PolicyHook",
    "ResourceRequirement",
    "ResourceServerError",
    "ResourceServerVerifier",
    "TokenValidationError",
    "VerificationResult",
    "VerificationStatus",
    "bearer_token_from_authorization",
    "verify_framework_request",
    "CapabilityAttestation",
    "ProtectedResourceVerifierContract",
    "VerifierContractProfile",
]


# Canonical resource-server contract shapes preserved from the former capability modules.
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
