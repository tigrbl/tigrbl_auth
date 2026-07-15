"""Versioned OAuth protected-resource profile and provider composition."""

from __future__ import annotations

from tigrbl_identity_contracts.protocol_processing import (
    build_protocol_capability_report,
)

from .bindings import CAPABILITY_REQUIREMENTS
from .capability import (
    ProtectedResourceAuthorizationCapability,
    build_protected_resource_authorization_capability,
)
from .claims import (
    RESOURCE_SERVER_ACCESS_TOKEN_CLAIM_CLASSES,
    compose_access_token_claim_set,
)
from .compatibility import (
    COMPATIBILITY_PATHS,
    ProtectedResourceCompatibility,
    compatibility,
)
from .errors import (
    ProtectedResourceBindingError,
    ProtectedResourceProfileError,
    UnsupportedProtectedResourceProfileError,
)
from .features import FEATURES_BY_VERSION, supports
from .metadata import VerifierContractProfile, verifier_contract_from_metadata
from .migrations import migrate_verifier_metadata
from .sender_constraints import (
    DpopCnfBindingValidator,
    MtlsCnfBindingValidator,
    SenderConstraintValidator,
)
from .verifier import (
    AccessTokenClaims,
    DPoPBinding,
    FrameworkRequest,
    IntrospectionClient,
    IntrospectionTransport,
    JWKSCache,
    MTLSBinding,
    PolicyHook,
    ResourceRequirement,
    ResourceServerError,
    ResourceServerVerifier,
    TokenValidationError,
    VerificationResult,
    VerificationStatus,
    bearer_token_from_authorization,
    verify_framework_request,
)
from .versions import (
    CURRENT_VERSION,
    SPECIFICATION_VERSIONS,
    VERSION_HISTORY,
    ProtectedResourceProfileVersion,
    ProtectedResourceSpecification,
    select_version,
)


def capability_report() -> dict[str, object]:
    return build_protocol_capability_report(
        protocol="oauth-protected-resource",
        revision=CURRENT_VERSION.identifier,
        features=tuple(FEATURES_BY_VERSION[CURRENT_VERSION.identifier]),
        evidence_links=("tests/unit/test_versioned_resource_server_profile.py",),
        extra_requirements=CAPABILITY_REQUIREMENTS,
        include_default_artifact_requirements=False,
    )


__all__ = [
    "CAPABILITY_REQUIREMENTS",
    "COMPATIBILITY_PATHS",
    "CURRENT_VERSION",
    "FEATURES_BY_VERSION",
    "RESOURCE_SERVER_ACCESS_TOKEN_CLAIM_CLASSES",
    "SPECIFICATION_VERSIONS",
    "VERSION_HISTORY",
    "AccessTokenClaims",
    "DPoPBinding",
    "DpopCnfBindingValidator",
    "FrameworkRequest",
    "IntrospectionClient",
    "IntrospectionTransport",
    "JWKSCache",
    "MTLSBinding",
    "MtlsCnfBindingValidator",
    "PolicyHook",
    "ProtectedResourceAuthorizationCapability",
    "ProtectedResourceBindingError",
    "ProtectedResourceCompatibility",
    "ProtectedResourceProfileError",
    "ProtectedResourceProfileVersion",
    "ProtectedResourceSpecification",
    "ResourceRequirement",
    "ResourceServerError",
    "ResourceServerVerifier",
    "SenderConstraintValidator",
    "TokenValidationError",
    "UnsupportedProtectedResourceProfileError",
    "VerificationResult",
    "VerificationStatus",
    "VerifierContractProfile",
    "bearer_token_from_authorization",
    "build_protected_resource_authorization_capability",
    "capability_report",
    "compatibility",
    "compose_access_token_claim_set",
    "migrate_verifier_metadata",
    "select_version",
    "supports",
    "verifier_contract_from_metadata",
    "verify_framework_request",
]
