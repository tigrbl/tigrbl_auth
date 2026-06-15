from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence

from .base import CertificationError


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
