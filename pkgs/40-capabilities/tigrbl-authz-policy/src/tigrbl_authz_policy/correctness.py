"""Compatibility re-export for assurance correctness helpers."""

from __future__ import annotations

from .assurance import (
    AuthorizationReference,
    AuthorizationSafetyPropertyEvaluator,
    IntegrityReport,
    ReferenceCatalog,
    SafetyPropertyResult,
    TenantRealmIsolationReport,
    TrustEdge,
    validate_authorization_referential_integrity,
    validate_tenant_realm_isolation,
    validate_trust_graph_integrity,
)

__all__ = [
    "AuthorizationReference",
    "AuthorizationSafetyPropertyEvaluator",
    "IntegrityReport",
    "ReferenceCatalog",
    "SafetyPropertyResult",
    "TenantRealmIsolationReport",
    "TrustEdge",
    "validate_authorization_referential_integrity",
    "validate_tenant_realm_isolation",
    "validate_trust_graph_integrity",
]
