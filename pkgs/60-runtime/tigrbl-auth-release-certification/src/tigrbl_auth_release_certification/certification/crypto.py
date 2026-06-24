from __future__ import annotations

import base64
import time
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence

from .base import CertificationError
from tigrbl_identity_concrete import MachineIdentity
from tigrbl_release_contracts import (
    AlgorithmPolicy,
    KeyBoundary,
    ML_DSA_65_ALG,
    PQC_JWK_KTY,
    PQC_SIGNATURE_ALGS,
    VerifierPolicy,
)


RSA_SIGNATURE_PREFIXES = ("RS", "PS")


def _b64url_decode(value: str) -> bytes:
    return base64.urlsafe_b64decode((value + "=" * (-len(value) % 4)).encode("ascii"))


def normalize_pqc_algorithm(algorithm: str) -> str:
    normalized = str(algorithm or "").replace("_", "-").upper()
    if normalized in {"ML-DSA-65", "MLDSA65"}:
        return ML_DSA_65_ALG
    raise CertificationError("unsupported post-quantum signature algorithm")


def public_key_from_pqc_jwk(jwk: Mapping[str, Any]) -> bytes:
    if str(jwk.get("kty") or "") != PQC_JWK_KTY:
        raise CertificationError("PQC JWK requires PQC key type")
    normalize_pqc_algorithm(str(jwk.get("alg") or jwk.get("crv") or ""))
    x = jwk.get("x")
    if not isinstance(x, str) or not x:
        raise CertificationError("PQC JWK requires public key material")
    return _b64url_decode(x)


def algorithm_policy_report(algorithms: Sequence[str], policy: AlgorithmPolicy | None = None) -> dict[str, Any]:
    active = policy or AlgorithmPolicy.certification_default()
    normalized = tuple(str(alg) for alg in algorithms)
    refused = tuple(alg for alg in normalized if alg in active.disallowed_algs or alg.startswith(RSA_SIGNATURE_PREFIXES))
    warnings = tuple(alg for alg in normalized if alg in active.warning_algs)
    pqc_available = tuple(alg for alg in normalized if alg in PQC_SIGNATURE_ALGS)
    return {
        "allowed": [alg for alg in normalized if alg in active.allowed_algs and alg not in refused],
        "refused": list(refused),
        "warnings": [f"{alg} is classical ECDSA and not post-quantum resistant" for alg in warnings],
        "pqc": {
            "ready": bool(pqc_available) if active.pqc_required else bool(PQC_SIGNATURE_ALGS),
            "registered_algs": list(pqc_available),
            "required": active.pqc_required,
            "policy_registered_algs": sorted(PQC_SIGNATURE_ALGS),
        },
    }


def assert_algorithm_policy(algorithm: str, policy: AlgorithmPolicy | None = None) -> None:
    active = policy or AlgorithmPolicy.certification_default()
    alg = str(algorithm)
    if alg in active.disallowed_algs or alg.startswith(RSA_SIGNATURE_PREFIXES):
        raise CertificationError("RSA signature algorithms are disallowed by certification policy")
    if active.pqc_required and alg not in PQC_SIGNATURE_ALGS:
        raise CertificationError("post-quantum signature algorithm required by certification policy")
    if alg not in active.allowed_algs:
        raise CertificationError("unsupported signature algorithm")


def validate_jwk_set(
    jwks: Mapping[str, Any],
    *,
    allowed_algs: frozenset[str] = frozenset({"RS256", "ES256", "EdDSA"}) | PQC_SIGNATURE_ALGS,
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
        if alg in PQC_SIGNATURE_ALGS:
            normalize_pqc_algorithm(str(alg))
            if kty != PQC_JWK_KTY:
                raise CertificationError("PQC algorithm requires PQC key type")
            public_key_from_pqc_jwk(key)
        if kty == "EC" and key.get("crv") not in {"P-256", "P-384", "P-521"}:
            raise CertificationError("unsupported EC curve")
        if kty == "OKP" and key.get("crv") not in {"Ed25519", "Ed448"}:
            raise CertificationError("unsupported OKP curve")


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


def assert_machine_identity_governed(identity: MachineIdentity, *, now: datetime | None = None) -> None:
    current = now or datetime.now(timezone.utc)
    if identity.human:
        raise CertificationError("machine identity cannot be marked human")
    if not identity.owner_id or not identity.tenant_id:
        raise CertificationError("machine identity requires owner and tenant scope")
    if identity.credential_rotates_at is None or identity.credential_rotates_at <= current:
        raise CertificationError("machine identity credential is past rotation deadline")
    if not identity.allowed_audiences:
        raise CertificationError("machine identity requires bounded audiences")
