from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Final

ECDSA_SIGNATURE_ALGS = frozenset({"ES256", "ES384", "ES512", "ES256K"})
EDDSA_SIGNATURE_ALGS = frozenset({"EdDSA"})
ML_DSA_65_ALG: Final[str] = "ML-DSA-65"
PQC_SIGNATURE_ALGS: Final[frozenset[str]] = frozenset({ML_DSA_65_ALG})
PQC_JWK_KTY: Final[str] = "PQC"


@dataclass(frozen=True)
class AlgorithmPolicy:
    allowed_algs: frozenset[str] = (
        EDDSA_SIGNATURE_ALGS | ECDSA_SIGNATURE_ALGS | PQC_SIGNATURE_ALGS
    )
    disallowed_algs: frozenset[str] = frozenset(
        {"none", "RS256", "RS384", "RS512", "PS256", "PS384", "PS512"}
    )
    warning_algs: frozenset[str] = ECDSA_SIGNATURE_ALGS
    pqc_required: bool = False

    @classmethod
    def certification_default(cls) -> "AlgorithmPolicy":
        return cls()


@dataclass(frozen=True)
class KeyBoundary:
    key_id: str
    owner_type: str
    owner_id: str
    algorithm: str
    rotation_epoch: int
    visible_to: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class VerifierPolicy:
    issuer: str
    audiences: frozenset[str]
    required_scopes: frozenset[str]
    max_authz_staleness_seconds: int
    allowed_algs: frozenset[str] = frozenset({"RS256", "ES256", "EdDSA"})


@dataclass(frozen=True)
class MachineIdentity:
    subject_id: str
    owner_id: str
    tenant_id: str
    credential_id: str
    credential_rotates_at: datetime
    allowed_audiences: frozenset[str]
    human: bool = False


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


__all__ = [
    "AlgorithmPolicy",
    "ECDSA_SIGNATURE_ALGS",
    "EDDSA_SIGNATURE_ALGS",
    "KeyBoundary",
    "ML_DSA_65_ALG",
    "MachineIdentity",
    "PQC_JWK_KTY",
    "PQC_SIGNATURE_ALGS",
    "RealmState",
    "TenantState",
    "VerifierPolicy",
]
