"""JOSE, JWT, JWK, JWS, and JWE surfaces for the Tigrbl identity package suite."""

from __future__ import annotations

from .boundary import (
    RFC_TARGETS,
    JoseKey,
    JoseKeyRotationResult,
    JoseKeySet,
    JoseKeyStatus,
    JoseKeyUse,
    jwk_thumbprint,
    publish_tenant_jwks,
    rfc_vector_manifest,
    validate_public_jwk,
)
from .jwe_policy import JWEPolicy
from .key_material import JWK_PRIVATE_PARAMETERS, materialize_public_key_record
from .jwt_coder import JWTCoder
from .configuration import (
    DefaultJoseProviderSettings,
    configure_jose_provider,
    jose_provider_source,
)
from .key_rotation_policy import (
    EffectiveKeyRotationPolicy,
    KeyRotationAdministration,
    KeyRotationPolicyGovernance,
    KeyRotationPolicyOverlapError,
    KeyRotationPolicyVersion,
)
from .pqc import (
    ML_DSA_65_ALG,
    PQC_JWK_KTY,
    PQC_LIBRARY_NAME,
    PQC_REQUIRED_DEPENDENCY,
    PQC_SIGNATURE_ALGS,
    PQCError,
    PQCSignatureKeyPair,
    generate_pqc_signature_keypair,
    pqc_backend_report,
    pqc_public_jwk,
    pqc_signing_jwk,
    sign_pqc_payload,
    verify_pqc_signature,
)

__all__ = [
    "DefaultJoseProviderSettings",
    "EffectiveKeyRotationPolicy",
    "JoseKey",
    "JoseKeyRotationResult",
    "JoseKeySet",
    "JoseKeyStatus",
    "JoseKeyUse",
    "JWTCoder",
    "KeyRotationAdministration",
    "KeyRotationPolicyGovernance",
    "KeyRotationPolicyOverlapError",
    "KeyRotationPolicyVersion",
    "JWEPolicy",
    "JWK_PRIVATE_PARAMETERS",
    "ML_DSA_65_ALG",
    "PQCError",
    "PQC_JWK_KTY",
    "PQC_LIBRARY_NAME",
    "PQC_REQUIRED_DEPENDENCY",
    "PQC_SIGNATURE_ALGS",
    "PQCSignatureKeyPair",
    "RFC_TARGETS",
    "configure_jose_provider",
    "generate_pqc_signature_keypair",
    "jose_provider_source",
    "jwk_thumbprint",
    "materialize_public_key_record",
    "pqc_backend_report",
    "pqc_public_jwk",
    "pqc_signing_jwk",
    "publish_tenant_jwks",
    "rfc_vector_manifest",
    "sign_pqc_payload",
    "validate_public_jwk",
    "verify_pqc_signature",
]
