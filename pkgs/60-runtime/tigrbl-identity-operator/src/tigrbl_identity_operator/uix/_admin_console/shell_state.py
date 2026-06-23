from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Mapping

from tigrbl_authz_policy.control_plane import (
    PolicyDecision,
    PUBLIC_CLIENT_FIELDS,
    assert_client_mutation_authority,
    build_compliance_report,
    expose_client_record,
    filter_visible_tenants,
    simulate_policy,
)
from tigrbl_authz_policy import (
    ABACAdministrator,
    AttributePolicy,
    DynamicCondition,
)
from tigrbl_authz_policy import (
    ADMIN_CLIENT_FIELDS,
    DELEGATED_MUTABLE_CLIENT_FIELDS,
    DELEGATED_VISIBLE_CLIENT_FIELDS,
    DelegatedAdminScope,
    DelegatedAdministrator,
)
from tigrbl_authz_policy import PolicyEngine
from tigrbl_authz_policy import (
    AuthorizationInvariant,
    InvariantEvaluation,
    InvariantRegistry,
    InvariantSeverity,
    InvariantViolation,
    VerificationMethod,
    default_authorization_invariant_registry,
)
from tigrbl_authz_policy import (
    ServiceIdentityAuthentication,
    ServiceIdentityRegistry,
)
from tigrbl_authz_policy import RBACAdministrator, Role
from tigrbl_authz_policy.governance_extension import (
    AccessReviewWorkflow,
    EntitlementManager,
    PluginRuntimeRegistry,
    SDKEcosystemCatalog,
    ScimPatchOperation,
    ScimProvisioningPlane,
    build_provisioning_governance_ecosystem_delivery_summary,
    build_phase5_delivery_summary,
)
from tigrbl_auth_release_certification.release_posture import (
    DisclosureRule,
    ProvenanceRequirement,
    TransportPosture,
    build_disclosure_rules,
    build_phase6_delivery_summary,
    build_release_provenance_requirements,
    build_transport_postures,
    disclose_jwe_admin,
    disclose_jwe_public,
    disclose_jws_admin,
    disclose_jws_public,
    disclose_jwks_admin,
    disclose_jwks_public,
    disclose_jwt_admin,
    disclose_jwt_public,
    explain_schema_publicly,
    redact_schema_for_admin,
)


ADMIN_NAVIGATION: tuple[str, ...] = (
    "dashboard",
    "configuration",
    "tenants",
    "clients",
    "identities",
    "sessions",
    "tokens",
    "consents",
    "audit",
    "keys-jwks",
    "tenant-jwks",
    "profile-certification",
    "rbac",
    "abac",
    "policy-simulation",
)

SECRET_TOKENS: tuple[str, ...] = (
    "secret",
    "password",
    "token",
    "private_key",
    "client_secret",
    "jwt_secret",
)


class AdminAuthorizationError(PermissionError):
    """Raised when the admin shell is requested without administrator access."""


@dataclass(frozen=True, slots=True)
class AdminConsoleShellBoundaryFeature:
    feature_id: str
    category: str
    runtime_objects: tuple[str, ...]
    guarded_capabilities: tuple[str, ...]


PRIORITY1_ADMIN_CONSOLE_SHELL_FEATURES: tuple[AdminConsoleShellBoundaryFeature, ...] = (
    AdminConsoleShellBoundaryFeature(
        "feat:uix-admin-console-shell",
        "shell",
        ("AdminConsoleShell", "AdminShellState", "ADMIN_NAVIGATION"),
        ("navigation", "environment-banner", "diagnostic-redaction"),
    ),
    AdminConsoleShellBoundaryFeature(
        "feat:uix-admin-auth-session",
        "session",
        ("AdminSession", "AdminPrincipal", "AdminAuthorizationError"),
        ("authenticated-admin-required", "scope-or-role-authorization"),
    ),
    AdminConsoleShellBoundaryFeature(
        "feat:uix-tenant-profile-selector",
        "tenant-profile",
        ("TenantProfileSelection", "AdminConsoleShell.golden_path"),
        ("tenant-context", "deployment-profile", "surface-set-selection"),
    ),
)


def priority1_admin_console_shell_boundary_manifest() -> dict[str, dict[str, Any]]:
    return {
        feature.feature_id: {
            "category": feature.category,
            "runtime_objects": list(feature.runtime_objects),
            "guarded_capabilities": list(feature.guarded_capabilities),
        }
        for feature in PRIORITY1_ADMIN_CONSOLE_SHELL_FEATURES
    }


def priority1_admin_console_shell_boundary_integrity() -> dict[str, Any]:
    manifest = priority1_admin_console_shell_boundary_manifest()
    categories = {row["category"] for row in manifest.values()}
    failures: list[str] = []
    if len(manifest) != 3:
        failures.append("priority 1 admin console shell boundary must track exactly 3 feature rows")
    for nav_item in ("dashboard", "tenants", "identities", "tenant-jwks"):
        if nav_item not in ADMIN_NAVIGATION:
            failures.append(f"missing admin navigation item {nav_item}")
    for required in ("shell", "session", "tenant-profile"):
        if required not in categories:
            failures.append(f"missing category {required}")
    return {
        "passed": not failures,
        "feature_count": len(manifest),
        "categories": sorted(categories),
        "failures": failures,
    }


@dataclass(frozen=True, slots=True)
class AdminPrincipal:
    subject: str
    roles: tuple[str, ...] = ()
    scopes: tuple[str, ...] = ()

    @property
    def is_admin(self) -> bool:
        return "admin" in self.roles or "tigrbl_auth:admin" in self.scopes


@dataclass(frozen=True, slots=True)
class AdminSession:
    session_id: str
    principal: AdminPrincipal | None
    authenticated: bool
    expires_at: datetime | None = None

    def require_admin(self) -> AdminPrincipal:
        if not self.authenticated or self.principal is None:
            raise AdminAuthorizationError("authenticated admin session required")
        if not self.principal.is_admin:
            raise AdminAuthorizationError("administrator authorization required")
        return self.principal


@dataclass(frozen=True, slots=True)
class TenantProfileSelection:
    tenant_id: str
    deployment_profile: str
    surface_sets: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class UnsafeStateWarning:
    code: str
    message: str


@dataclass(frozen=True, slots=True)
class ReadinessDashboard:
    status: str
    sections: Mapping[str, str]
    warnings: tuple[UnsafeStateWarning, ...]
    diagnostics: Mapping[str, Any]


ENTERPRISE_READINESS_FEATURES: dict[str, dict[str, tuple[str, ...] | str]] = {
    "feat:uix-enterprise-readiness-dashboard": {
        "surface": "readiness-dashboard",
        "runtime_objects": ("ReadinessDashboard", "UnsafeStateWarning", "build_readiness_dashboard"),
        "guarded_capabilities": ("healthy-degraded-blocked-status", "section-status", "warning-projection"),
    },
    "feat:uix-redacted-config-viewer": {
        "surface": "redacted-config-viewer",
        "runtime_objects": ("redact_sensitive_values", "SECRET_TOKENS", "ReadinessDashboard.diagnostics"),
        "guarded_capabilities": ("secret-redaction", "nested-redaction", "non-secret-preservation"),
    },
}


def enterprise_readiness_boundary_manifest() -> dict[str, dict[str, Any]]:
    return {
        feature_id: {
            "surface": str(row["surface"]),
            "runtime_objects": list(row["runtime_objects"]),
            "guarded_capabilities": list(row["guarded_capabilities"]),
        }
        for feature_id, row in ENTERPRISE_READINESS_FEATURES.items()
    }


def enterprise_readiness_boundary_integrity() -> dict[str, Any]:
    manifest = enterprise_readiness_boundary_manifest()
    failures: list[str] = []
    if len(manifest) != 2:
        failures.append("priority 1 enterprise readiness boundary must track exactly 2 feature rows")
    for token in ("secret", "password", "token", "client_secret", "jwt_secret"):
        if token not in SECRET_TOKENS:
            failures.append(f"missing redaction token {token}")
    for required_surface in ("readiness-dashboard", "redacted-config-viewer"):
        if required_surface not in {row["surface"] for row in manifest.values()}:
            failures.append(f"missing surface {required_surface}")
    return {
        "passed": not failures,
        "feature_count": len(manifest),
        "surfaces": [row["surface"] for row in manifest.values()],
        "failures": failures,
    }


@dataclass(frozen=True, slots=True)
class AdminShellState:
    principal_subject: str
    tenant_id: str
    deployment_profile: str
    issuer: str
    environment_label: str
    navigation: tuple[str, ...]
    active_surface_sets: tuple[str, ...]
    warnings: tuple[UnsafeStateWarning, ...]
    diagnostics: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "principal_subject": self.principal_subject,
            "tenant_id": self.tenant_id,
            "deployment_profile": self.deployment_profile,
            "issuer": self.issuer,
            "environment_label": self.environment_label,
            "navigation": list(self.navigation),
            "active_surface_sets": list(self.active_surface_sets),
            "warnings": [
                {"code": warning.code, "message": warning.message}
                for warning in self.warnings
            ],
            "diagnostics": dict(self.diagnostics),
        }


