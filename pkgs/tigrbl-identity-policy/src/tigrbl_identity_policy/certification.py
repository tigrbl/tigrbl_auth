"""Runtime certification helpers for strategic security concerns.

The functions in this module are deliberately small and dependency-light.  They
turn the SSOT strategic concern contracts into executable checks that product
surfaces, resource validators, and certification tests can share without
booting the full ASGI application.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import re
import time
from typing import Any, Iterable, Mapping, Sequence
from urllib.parse import urlparse


class CertificationError(ValueError):
    """Raised when a strategic security certification check fails closed."""


_SLUG_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")
_SECRET_KEYS = {"password", "secret", "token", "access_token", "refresh_token"}


def _require_slug(value: str, label: str) -> str:
    if not _SLUG_RE.fullmatch(value):
        raise CertificationError(f"invalid {label}: {value!r}")
    return value


def _require_https_url(value: str, label: str, *, allow_http_localhost: bool = False) -> str:
    parsed = urlparse(value)
    if parsed.scheme == "https" and parsed.netloc:
        return value.rstrip("/")
    if (
        allow_http_localhost
        and parsed.scheme == "http"
        and parsed.hostname in {"localhost", "127.0.0.1", "::1"}
        and parsed.netloc
    ):
        return value.rstrip("/")
    raise CertificationError(f"{label} must be an absolute https issuer URL")


def deterministic_issuer(
    base_issuer: str,
    *,
    realm_slug: str | None = None,
    tenant_slug: str | None = None,
    allow_http_localhost: bool = False,
) -> str:
    """Derive an issuer without consulting request host/proxy headers."""

    issuer = _require_https_url(
        base_issuer,
        "base_issuer",
        allow_http_localhost=allow_http_localhost,
    )
    if realm_slug is not None:
        issuer = f"{issuer}/realms/{_require_slug(realm_slug, 'realm_slug')}"
    if tenant_slug is not None:
        if realm_slug is None:
            raise CertificationError("tenant issuer derivation requires a realm slug")
        issuer = f"{issuer}/tenants/{_require_slug(tenant_slug, 'tenant_slug')}"
    return issuer


@dataclass(frozen=True)
class RealmState:
    realm_id: str
    slug: str
    issuer: str
    jwks_uri: str
    key_ids: frozenset[str]
    tenant_ids: frozenset[str] = field(default_factory=frozenset)
    client_ids: frozenset[str] = field(default_factory=frozenset)
    policy_ids: frozenset[str] = field(default_factory=frozenset)
    token_ids: frozenset[str] = field(default_factory=frozenset)
    cache_namespace: str | None = None
    admin_authorities: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class TenantState:
    tenant_id: str
    slug: str
    realm_id: str
    issuer: str
    jwks_uri: str
    key_ids: frozenset[str]
    client_ids: frozenset[str] = field(default_factory=frozenset)
    user_ids: frozenset[str] = field(default_factory=frozenset)
    policy_ids: frozenset[str] = field(default_factory=frozenset)
    credential_ids: frozenset[str] = field(default_factory=frozenset)
    token_ids: frozenset[str] = field(default_factory=frozenset)
    cache_namespace: str | None = None


def _assert_disjoint(label: str, owners: Mapping[str, frozenset[str]]) -> None:
    seen: dict[str, str] = {}
    for owner, values in owners.items():
        for value in values:
            previous = seen.setdefault(value, owner)
            if previous != owner:
                raise CertificationError(
                    f"{label} {value!r} crosses from {previous!r} to {owner!r}"
                )


def assert_realm_isolation(realms: Sequence[RealmState]) -> None:
    """Prove realm-scoped objects and metadata do not cross realm boundaries."""

    if len(realms) < 2:
        raise CertificationError("realm isolation certification requires at least two realms")
    ids = [realm.realm_id for realm in realms]
    slugs = [realm.slug for realm in realms]
    issuers = [realm.issuer for realm in realms]
    jwks = [realm.jwks_uri for realm in realms]
    namespaces = [realm.cache_namespace for realm in realms if realm.cache_namespace]
    for label, values in {
        "realm id": ids,
        "realm slug": slugs,
        "issuer": issuers,
        "jwks_uri": jwks,
        "cache namespace": namespaces,
    }.items():
        if len(values) != len(set(values)):
            raise CertificationError(f"duplicate {label} in realm isolation set")

    _assert_disjoint("tenant", {r.realm_id: r.tenant_ids for r in realms})
    _assert_disjoint("client", {r.realm_id: r.client_ids for r in realms})
    _assert_disjoint("policy", {r.realm_id: r.policy_ids for r in realms})
    _assert_disjoint("token", {r.realm_id: r.token_ids for r in realms})
    _assert_disjoint("key", {r.realm_id: r.key_ids for r in realms})
    _assert_disjoint("admin authority", {r.realm_id: r.admin_authorities for r in realms})


def assert_tenant_isolation(tenants: Sequence[TenantState]) -> None:
    """Prove same-realm and cross-realm tenant state cannot overlap."""

    if len(tenants) < 2:
        raise CertificationError("tenant isolation certification requires at least two tenants")
    pairs = {(tenant.realm_id, tenant.tenant_id) for tenant in tenants}
    if len(pairs) != len(tenants):
        raise CertificationError("duplicate tenant id inside a realm")
    for label, values in {
        "issuer": [t.issuer for t in tenants],
        "jwks_uri": [t.jwks_uri for t in tenants],
        "cache namespace": [t.cache_namespace for t in tenants if t.cache_namespace],
    }.items():
        if len(values) != len(set(values)):
            raise CertificationError(f"duplicate tenant {label}")
    _assert_disjoint("tenant client", {t.tenant_id: t.client_ids for t in tenants})
    _assert_disjoint("tenant user", {t.tenant_id: t.user_ids for t in tenants})
    _assert_disjoint("tenant policy", {t.tenant_id: t.policy_ids for t in tenants})
    _assert_disjoint("tenant credential", {t.tenant_id: t.credential_ids for t in tenants})
    _assert_disjoint("tenant token", {t.tenant_id: t.token_ids for t in tenants})
    _assert_disjoint("tenant key", {t.tenant_id: t.key_ids for t in tenants})


def assert_issuer_consistency(
    *,
    expected_issuer: str,
    metadata_issuer: str,
    token_issuer: str | None = None,
    jwks_uri: str | None = None,
    allowed_jwks_uri: str | None = None,
) -> None:
    if metadata_issuer != expected_issuer:
        raise CertificationError("metadata issuer mismatch")
    if token_issuer is not None and token_issuer != expected_issuer:
        raise CertificationError("token issuer mismatch")
    if allowed_jwks_uri is not None and jwks_uri != allowed_jwks_uri:
        raise CertificationError("jwks_uri mismatch")


@dataclass(frozen=True)
class CapabilityRecord:
    name: str
    enabled: bool
    evidence_id: str | None = None
    route: str | None = None


def runtime_capability_truth(
    configured: Sequence[CapabilityRecord],
    advertised: Iterable[str],
) -> dict[str, bool]:
    """Return evidence-backed capability truth and fail on stale advertising."""

    by_name = {record.name: record for record in configured}
    advertised_set = set(advertised)
    unknown = advertised_set.difference(by_name)
    if unknown:
        raise CertificationError(f"advertised unknown capabilities: {sorted(unknown)}")
    for name in advertised_set:
        record = by_name[name]
        if not record.enabled:
            raise CertificationError(f"disabled capability advertised: {name}")
        if not record.evidence_id:
            raise CertificationError(f"capability lacks evidence: {name}")
    return {name: record.enabled and bool(record.evidence_id) for name, record in by_name.items()}


@dataclass
class AuthorizationState:
    subject_id: str
    version: int = 1
    updated_at: float = field(default_factory=time.time)
    mutations: list[str] = field(default_factory=list)

    def mutate(self, reason: str) -> int:
        if not reason:
            raise CertificationError("authorization mutation requires a reason")
        self.version += 1
        self.updated_at = time.time()
        self.mutations.append(reason)
        return self.version


@dataclass(frozen=True)
class AuthorizationSnapshot:
    subject_id: str
    version: int
    issued_at: float
    max_staleness_seconds: int


def assert_authorization_fresh(
    snapshot: AuthorizationSnapshot,
    state: AuthorizationState,
    *,
    now: float | None = None,
) -> None:
    if snapshot.subject_id != state.subject_id:
        raise CertificationError("authorization subject mismatch")
    current_time = time.time() if now is None else now
    if snapshot.version < state.version:
        raise CertificationError("authorization snapshot predates current mutation version")
    if current_time - snapshot.issued_at > snapshot.max_staleness_seconds:
        raise CertificationError("authorization snapshot exceeds freshness window")


def validate_jwk_set(
    jwks: Mapping[str, Any],
    *,
    allowed_algs: frozenset[str] = frozenset({"RS256", "ES256", "EdDSA"}),
) -> None:
    keys = jwks.get("keys")
    if not isinstance(keys, list) or not keys:
        raise CertificationError("JWKS must contain a non-empty keys list")
    kids: set[str] = set()
    for key in keys:
        if not isinstance(key, Mapping):
            raise CertificationError("JWK must be an object")
        kid = key.get("kid")
        if not isinstance(kid, str) or not kid:
            raise CertificationError("JWK kid is required")
        if kid in kids:
            raise CertificationError("duplicate JWK kid")
        kids.add(kid)
        alg = key.get("alg")
        if alg == "none" or alg not in allowed_algs:
            raise CertificationError("unsupported JWK algorithm")
        kty = key.get("kty")
        if alg.startswith("RS") and kty != "RSA":
            raise CertificationError("RSA algorithm requires RSA key type")
        if alg.startswith("ES") and kty != "EC":
            raise CertificationError("EC algorithm requires EC key type")
        if alg == "EdDSA" and kty != "OKP":
            raise CertificationError("EdDSA requires OKP key type")
        if kty == "EC" and key.get("crv") not in {"P-256", "P-384", "P-521"}:
            raise CertificationError("unsupported EC curve")
        if kty == "OKP" and key.get("crv") not in {"Ed25519", "Ed448"}:
            raise CertificationError("unsupported OKP curve")


@dataclass(frozen=True)
class KeyBoundary:
    key_id: str
    owner_type: str
    owner_id: str
    algorithm: str
    rotation_epoch: int
    visible_to: frozenset[str] = field(default_factory=frozenset)


def assert_crypto_boundaries(keys: Sequence[KeyBoundary]) -> None:
    by_id: dict[str, KeyBoundary] = {}
    for key in keys:
        if key.owner_type not in {"realm", "tenant"}:
            raise CertificationError("key owner type must be realm or tenant")
        existing = by_id.setdefault(key.key_id, key)
        if existing is not key:
            raise CertificationError("duplicate key id across crypto boundaries")
        if key.owner_id in key.visible_to:
            continue
        if key.owner_type == "tenant" and key.visible_to:
            raise CertificationError("tenant key visible outside its owner boundary")
        if key.rotation_epoch < 1:
            raise CertificationError("key rotation epoch must be positive")


@dataclass(frozen=True)
class VerifierPolicy:
    issuer: str
    audiences: frozenset[str]
    required_scopes: frozenset[str]
    max_authz_staleness_seconds: int
    allowed_algs: frozenset[str] = frozenset({"RS256", "ES256", "EdDSA"})


def assert_verifier_accepts(policy: VerifierPolicy, token_claims: Mapping[str, Any]) -> None:
    if token_claims.get("iss") != policy.issuer:
        raise CertificationError("verifier issuer mismatch")
    audience = token_claims.get("aud")
    token_audiences = {audience} if isinstance(audience, str) else set(audience or [])
    if not token_audiences.intersection(policy.audiences):
        raise CertificationError("verifier audience mismatch")
    scopes = set(str(token_claims.get("scope", "")).split())
    if not policy.required_scopes.issubset(scopes):
        raise CertificationError("verifier required scope missing")
    now = int(time.time())
    if int(token_claims.get("exp", 0)) <= now:
        raise CertificationError("verifier rejects expired token")
    if int(token_claims.get("nbf", 0) or 0) > now:
        raise CertificationError("verifier rejects not-yet-valid token")
    authz_iat = int(token_claims.get("authz_iat", token_claims.get("iat", now)))
    if now - authz_iat > policy.max_authz_staleness_seconds:
        raise CertificationError("verifier rejects stale authorization")


@dataclass(frozen=True)
class MachineIdentity:
    subject_id: str
    owner_id: str
    tenant_id: str
    credential_id: str
    credential_rotates_at: datetime
    allowed_audiences: frozenset[str]
    human: bool = False


def assert_machine_identity_governed(identity: MachineIdentity, *, now: datetime | None = None) -> None:
    current = now or datetime.now(timezone.utc)
    if identity.human:
        raise CertificationError("machine identity cannot be marked human")
    if not identity.owner_id or not identity.tenant_id:
        raise CertificationError("machine identity requires owner and tenant scope")
    if identity.credential_rotates_at <= current:
        raise CertificationError("machine identity credential is past rotation deadline")
    if not identity.allowed_audiences:
        raise CertificationError("machine identity requires bounded audiences")


@dataclass(frozen=True)
class DelegationStep:
    actor: str
    subject: str
    scopes: frozenset[str]
    proof_id: str


def assert_delegation_provenance(
    chain: Sequence[DelegationStep],
    *,
    max_depth: int,
    allowed_final_scopes: frozenset[str],
) -> None:
    if not chain:
        raise CertificationError("delegation chain is required")
    if len(chain) > max_depth:
        raise CertificationError("delegation chain exceeds maximum depth")
    seen_actors: set[str] = set()
    previous_subject = chain[0].subject
    for step in chain:
        if not step.proof_id:
            raise CertificationError("delegation step requires proof")
        if step.actor in seen_actors:
            raise CertificationError("delegation chain cycle detected")
        seen_actors.add(step.actor)
        if step.subject != previous_subject:
            raise CertificationError("delegation subject continuity broken")
        previous_subject = step.actor
    if not chain[-1].scopes.issubset(allowed_final_scopes):
        raise CertificationError("delegation final scopes exceed attenuation")


@dataclass(frozen=True)
class AuthorizationEvent:
    event_type: str
    subject_id: str
    actor_id: str
    decision: str
    correlation_id: str
    occurred_at: datetime
    attributes: Mapping[str, Any] = field(default_factory=dict)


def sanitize_event_attributes(attributes: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: "[REDACTED]" if key.lower() in _SECRET_KEYS else value
        for key, value in attributes.items()
    }


def assert_observable_event(event: AuthorizationEvent) -> dict[str, Any]:
    if event.decision not in {"allow", "deny"}:
        raise CertificationError("authorization event decision must be allow or deny")
    required = [event.event_type, event.subject_id, event.actor_id, event.correlation_id]
    if any(not value for value in required):
        raise CertificationError("authorization event missing required identity fields")
    return {
        "event_type": event.event_type,
        "subject_id": event.subject_id,
        "actor_id": event.actor_id,
        "decision": event.decision,
        "correlation_id": event.correlation_id,
        "occurred_at": event.occurred_at.isoformat(),
        "attributes": sanitize_event_attributes(event.attributes),
    }


@dataclass(frozen=True)
class RuntimeQualification:
    artifact_sha256: str
    dependency_lock_sha256: str
    config_sha256: str
    product_surface: str
    capabilities: frozenset[str]


def stable_sha256(value: Mapping[str, Any] | Sequence[Any] | str) -> str:
    if isinstance(value, str):
        payload = value.encode("utf-8")
    else:
        payload = repr(value).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def assert_runtime_qualified(
    qualified: RuntimeQualification,
    running: RuntimeQualification,
) -> None:
    if qualified != running:
        raise CertificationError("running runtime does not match qualified deployment truth")
