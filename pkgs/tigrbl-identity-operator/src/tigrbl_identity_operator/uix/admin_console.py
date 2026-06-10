from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Mapping

from tigrbl_identity_policy.control_plane import (
    ABACAdministration,
    ADMIN_CLIENT_FIELDS,
    AdminPolicyBoundaryFeature,
    AttributePolicy,
    DELEGATED_MUTABLE_CLIENT_FIELDS,
    DELEGATED_VISIBLE_CLIENT_FIELDS,
    DelegatedAdminScope,
    DelegatedAdministration,
    DynamicCondition,
    PolicyDecision,
    PolicyEngine,
    PHASE3_ADMIN_POLICY_FEATURES,
    PUBLIC_CLIENT_FIELDS,
    RBACAdministration,
    Role,
    ServiceIdentityAuthentication,
    ServiceIdentityRegistry,
    assert_client_mutation_authority,
    build_compliance_report,
    expose_client_record,
    filter_visible_tenants,
    phase3_admin_policy_boundary_integrity,
    phase3_admin_policy_boundary_manifest,
    simulate_policy,
)
from tigrbl_identity_policy.invariants import (
    AuthorizationInvariant,
    InvariantEvaluation,
    InvariantRegistry,
    InvariantSeverity,
    InvariantViolation,
    VerificationMethod,
    default_authorization_invariant_registry,
)
from tigrbl_identity_policy.governance_extension import (
    AccessReviewWorkflow,
    EntitlementManager,
    GovernanceExtensionBoundaryFeature,
    PHASE5_GOVERNANCE_EXTENSION_FEATURES,
    PluginRuntimeRegistry,
    SDKEcosystemCatalog,
    ScimPatchOperation,
    ScimProvisioningPlane,
    build_phase5_delivery_summary,
    phase5_governance_extension_boundary_integrity,
    phase5_governance_extension_boundary_manifest,
)
from tigrbl_identity_policy.release_posture import (
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


class AdminConsoleShell:
    def __init__(
        self,
        *,
        issuer: str,
        environment_label: str,
        navigation: tuple[str, ...] = ADMIN_NAVIGATION,
    ) -> None:
        self.issuer = issuer
        self.environment_label = environment_label
        self.navigation = navigation

    def render(
        self,
        *,
        session: AdminSession,
        selection: TenantProfileSelection,
        readiness: Mapping[str, bool],
        diagnostics: Mapping[str, Any] | None = None,
    ) -> AdminShellState:
        principal = session.require_admin()
        redacted_diagnostics = redact_sensitive_values(diagnostics or {})
        return AdminShellState(
            principal_subject=principal.subject,
            tenant_id=selection.tenant_id,
            deployment_profile=selection.deployment_profile,
            issuer=self.issuer,
            environment_label=self.environment_label,
            navigation=self.navigation,
            active_surface_sets=selection.surface_sets,
            warnings=tuple(_warnings_for(readiness)),
            diagnostics=redacted_diagnostics,
        )

    def golden_path(
        self,
        *,
        session: AdminSession,
        initial_selection: TenantProfileSelection,
        next_selection: TenantProfileSelection,
    ) -> dict[str, Any]:
        principal = session.require_admin()
        now = datetime.now(tz=timezone.utc).isoformat()
        return {
            "principal_subject": principal.subject,
            "events": [
                {"event": "admin.session.accepted", "at": now},
                {"event": "admin.dashboard.rendered", "tenant_id": initial_selection.tenant_id},
                {
                    "event": "admin.context.selected",
                    "tenant_id": next_selection.tenant_id,
                    "deployment_profile": next_selection.deployment_profile,
                },
                {"event": "admin.audit.recorded", "action": "context.selected"},
            ],
        }


RESOURCE_VIEW_METHODS: dict[str, tuple[str, ...]] = {
    "tenants": ("tenant.list", "tenant.show"),
    "clients": ("client.list", "client.show"),
    "identities": ("identity.list", "identity.show"),
    "sessions": ("session.list", "session.show"),
    "tokens": ("token.list", "token.inspect"),
    "consents": ("consent.list", "consent.show"),
    "audit": ("audit.list", "audit.export"),
    "keys-jwks": ("keys.list", "jwks.show"),
    "profile-certification": ("profile.show", "target.list", "claims.show", "evidence.status"),
}

ADMINISTRATIVE_RESOURCE_VIEW_FEATURES: dict[str, str] = {
    "feat:uix-tenant-admin-view": "tenants",
    "feat:uix-client-admin-view": "clients",
    "feat:uix-identity-admin-view": "identities",
    "feat:uix-session-admin-view": "sessions",
    "feat:uix-token-admin-view": "tokens",
    "feat:uix-consent-admin-view": "consents",
    "feat:uix-audit-admin-view": "audit",
    "feat:uix-keys-jwks-admin-view": "keys-jwks",
    "feat:uix-profile-certification-view": "profile-certification",
}

RESOURCE_VIEW_STATES: tuple[str, ...] = (
    "empty",
    "loading",
    "error",
    "filtered",
    "detail",
)

SAFE_MUTATION_METHODS: dict[str, str] = {
    "revoke-session": "session.terminate",
    "revoke-token": "token.inspect",
    "revoke-consent": "consent.revoke",
    "lock-identity": "identity.show",
    "toggle-tenant": "tenant.show",
    "toggle-client": "client.show",
    "rotate-key": "keys.rotate",
    "publish-jwks": "jwks.show",
    "update-client-registration": "client.registration.upsert",
}

ADMINISTRATIVE_SAFE_MUTATION_FEATURES: dict[str, str] = {
    "feat:uix-safe-mutation-revoke-session": "revoke-session",
    "feat:uix-safe-mutation-revoke-token": "revoke-token",
    "feat:uix-safe-mutation-revoke-consent": "revoke-consent",
    "feat:uix-safe-mutation-lock-identity": "lock-identity",
    "feat:uix-safe-mutation-toggle-tenant": "toggle-tenant",
    "feat:uix-safe-mutation-toggle-client": "toggle-client",
    "feat:uix-safe-mutation-rotate-key": "rotate-key",
    "feat:uix-safe-mutation-publish-jwks": "publish-jwks",
    "feat:uix-safe-mutation-update-client-registration": "update-client-registration",
}


def administrative_safe_mutations_boundary_manifest() -> dict[str, dict[str, Any]]:
    return {
        feature_id: {
            "action": action,
            "required_method": SAFE_MUTATION_METHODS[action],
            "runtime_objects": ["SafeMutationRequest", "SafeMutationResult", "execute_safe_mutation"],
            "guarded_capabilities": ["explicit-confirmation", "audit-outcome", "executor-failure-reporting"],
        }
        for feature_id, action in ADMINISTRATIVE_SAFE_MUTATION_FEATURES.items()
    }


def administrative_safe_mutations_boundary_integrity() -> dict[str, Any]:
    manifest = administrative_safe_mutations_boundary_manifest()
    failures: list[str] = []
    if len(manifest) != 9:
        failures.append("priority 1 administrative safe mutations boundary must track exactly 9 feature rows")
    for feature_id, action in ADMINISTRATIVE_SAFE_MUTATION_FEATURES.items():
        if action not in SAFE_MUTATION_METHODS:
            failures.append(f"{feature_id} maps to missing safe mutation action {action}")
        elif not SAFE_MUTATION_METHODS[action]:
            failures.append(f"{action} has no required OpenRPC method")
    return {
        "passed": not failures,
        "feature_count": len(manifest),
        "actions": list(ADMINISTRATIVE_SAFE_MUTATION_FEATURES.values()),
        "failures": failures,
    }


@dataclass(frozen=True, slots=True)
class ResourceView:
    name: str
    required_methods: tuple[str, ...]
    missing_methods: tuple[str, ...]
    states: tuple[str, ...] = RESOURCE_VIEW_STATES

    @property
    def backed(self) -> bool:
        return not self.missing_methods


def administrative_resource_views_boundary_manifest() -> dict[str, dict[str, Any]]:
    return {
        feature_id: {
            "view": view_name,
            "runtime_objects": ["ResourceView", "RESOURCE_VIEW_METHODS", "build_resource_views"],
            "required_methods": list(RESOURCE_VIEW_METHODS[view_name]),
            "states": list(RESOURCE_VIEW_STATES),
        }
        for feature_id, view_name in ADMINISTRATIVE_RESOURCE_VIEW_FEATURES.items()
    }


def administrative_resource_views_boundary_integrity() -> dict[str, Any]:
    manifest = administrative_resource_views_boundary_manifest()
    failures: list[str] = []
    if len(manifest) != 9:
        failures.append("priority 1 administrative resource views boundary must track exactly 9 feature rows")
    for feature_id, view_name in ADMINISTRATIVE_RESOURCE_VIEW_FEATURES.items():
        if view_name not in RESOURCE_VIEW_METHODS:
            failures.append(f"{feature_id} maps to missing view {view_name}")
        elif not RESOURCE_VIEW_METHODS[view_name]:
            failures.append(f"{view_name} has no required OpenRPC methods")
    for state in ("empty", "loading", "error", "filtered", "detail"):
        if state not in RESOURCE_VIEW_STATES:
            failures.append(f"missing resource view state {state}")
    return {
        "passed": not failures,
        "feature_count": len(manifest),
        "views": list(ADMINISTRATIVE_RESOURCE_VIEW_FEATURES.values()),
        "failures": failures,
    }


@dataclass(frozen=True, slots=True)
class TenantJwksPublicationKey:
    kid: str
    alg: str
    kty: str
    use: str
    lifecycle: str
    public: bool
    crv: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    rotated_at: str | None = None
    retired_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "kid": self.kid,
            "alg": self.alg,
            "kty": self.kty,
            "use": self.use,
            "crv": self.crv,
            "lifecycle": self.lifecycle,
            "public": self.public,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "rotated_at": self.rotated_at,
            "retired_at": self.retired_at,
        }


@dataclass(frozen=True, slots=True)
class TenantJwksPublicationView:
    tenant_slug: str
    issuer: str
    jwks_uri: str
    publication_status: str
    keys: tuple[TenantJwksPublicationKey, ...]
    parity_indicator: str

    def keys_by_lifecycle(self) -> dict[str, tuple[TenantJwksPublicationKey, ...]]:
        return {
            lifecycle: tuple(key for key in self.keys if key.lifecycle == lifecycle)
            for lifecycle in ("active", "next", "retired")
        }

    def to_dict(self) -> dict[str, Any]:
        grouped = self.keys_by_lifecycle()
        return {
            "tenant_slug": self.tenant_slug,
            "issuer": self.issuer,
            "jwks_uri": self.jwks_uri,
            "publication_status": self.publication_status,
            "parity_indicator": self.parity_indicator,
            "keys": [key.to_dict() for key in self.keys],
            "keys_by_lifecycle": {
                lifecycle: [key.to_dict() for key in keys]
                for lifecycle, keys in grouped.items()
            },
        }


@dataclass(frozen=True, slots=True)
class SafeMutationRequest:
    action: str
    target_id: str
    confirmed: bool = False
    confirmation_text: str = ""


@dataclass(frozen=True, slots=True)
class SafeMutationResult:
    action: str
    target_id: str
    status: str
    required_method: str | None
    audit_event: Mapping[str, Any]
    error: str | None = None


def build_resource_views(available_methods: set[str] | tuple[str, ...] | list[str]) -> dict[str, ResourceView]:
    available = set(available_methods)
    views: dict[str, ResourceView] = {}
    for name, required_methods in RESOURCE_VIEW_METHODS.items():
        missing = tuple(method for method in required_methods if method not in available)
        views[name] = ResourceView(name=name, required_methods=required_methods, missing_methods=missing)
    return views


def build_tenant_jwks_publication_view(
    *,
    root_issuer: str,
    tenant_slug: str,
    jwks: Mapping[str, Any],
    key_records: tuple[Mapping[str, Any], ...] | list[Mapping[str, Any]] = (),
    tenant_enabled: bool = True,
) -> TenantJwksPublicationView:
    issuer = f"{root_issuer.rstrip('/')}/tenants/{tenant_slug}"
    jwks_uri = f"{root_issuer.rstrip('/')}/tenants/{tenant_slug}/.well-known/jwks.json"
    public_keys = {
        str(key.get("kid")): key
        for key in jwks.get("keys", [])
        if isinstance(key, Mapping) and key.get("kid") not in {None, ""}
    }
    rows: dict[str, TenantJwksPublicationKey] = {}

    for kid, key in public_keys.items():
        lifecycle = str(key.get("status") or "active").lower()
        rows[kid] = TenantJwksPublicationKey(
            kid=kid,
            alg=str(key.get("alg") or ""),
            kty=str(key.get("kty") or ""),
            use=str(key.get("use") or ""),
            crv=str(key.get("crv")) if key.get("crv") not in {None, ""} else None,
            lifecycle=lifecycle,
            public=True,
        )

    for record in key_records:
        data = record.get("data") or record.get("metadata") or {}
        if not isinstance(data, Mapping):
            data = {}
        kid = str(data.get("kid") or record.get("kid") or record.get("id") or "")
        if not kid:
            continue
        record_tenant = record.get("tenant") or record.get("tenant_slug") or data.get("tenant") or data.get("tenant_slug")
        if record_tenant not in {None, ""} and str(record_tenant) != tenant_slug:
            continue
        if record_tenant in {None, ""} and kid not in public_keys:
            continue
        lifecycle = str(data.get("publication_status") or record.get("status") or data.get("status") or "active").lower()
        if lifecycle not in {"active", "next", "retired"}:
            lifecycle = "active" if rows.get(kid, None) and rows[kid].public else lifecycle
        if lifecycle == "retired" or kid not in rows:
            rows[kid] = TenantJwksPublicationKey(
                kid=kid,
                alg=str(data.get("alg") or record.get("alg") or ""),
                kty=str(data.get("kty") or record.get("kty") or ""),
                use=str(data.get("use") or record.get("use") or ""),
                crv=str(data.get("crv") or data.get("curve")) if (data.get("crv") or data.get("curve")) else None,
                lifecycle=lifecycle,
                public=kid in public_keys,
                created_at=str(record.get("created_at")) if record.get("created_at") else None,
                updated_at=str(record.get("updated_at")) if record.get("updated_at") else None,
                rotated_at=str(data.get("rotated_at")) if data.get("rotated_at") else None,
                retired_at=str(data.get("retired_at")) if data.get("retired_at") else None,
            )

    ordered = tuple(sorted(rows.values(), key=lambda key: ({"active": 0, "next": 1, "retired": 2}.get(key.lifecycle, 3), key.kid)))
    status = "published" if tenant_enabled and public_keys else "not_published"
    return TenantJwksPublicationView(
        tenant_slug=tenant_slug,
        issuer=issuer,
        jwks_uri=jwks_uri,
        publication_status=status,
        keys=ordered,
        parity_indicator=f"Matches GET /tenants/{tenant_slug}/.well-known/jwks.json",
    )


def build_readiness_dashboard(
    readiness: Mapping[str, bool],
    diagnostics: Mapping[str, Any] | None = None,
) -> ReadinessDashboard:
    warnings = tuple(_warnings_for(readiness))
    if not warnings:
        status = "healthy"
    elif any(warning.code in {"admin_authorized", "contracts_valid", "migrations_current"} for warning in warnings):
        status = "blocked"
    else:
        status = "degraded"

    section_keys = {
        "runtime": "readiness_healthy",
        "database": "migrations_current",
        "issuer": "contracts_valid",
        "key_material": "openrpc_available",
        "admin_gate": "admin_authorized",
        "cookie_tls": "cookies_secure",
    }
    sections = {
        name: "ready" if bool(readiness.get(key, False)) else "blocked"
        for name, key in section_keys.items()
    }
    return ReadinessDashboard(
        status=status,
        sections=sections,
        warnings=warnings,
        diagnostics=redact_sensitive_values(diagnostics or {}),
    )


def execute_safe_mutation(
    request: SafeMutationRequest,
    *,
    executor: Callable[[SafeMutationRequest], Mapping[str, Any]] | None = None,
) -> SafeMutationResult:
    required_method = SAFE_MUTATION_METHODS.get(request.action)
    if required_method is None:
        raise ValueError(f"unknown safe mutation action {request.action!r}")
    expected_confirmation = f"{request.action}:{request.target_id}"
    audit_event = {
        "action": request.action,
        "target_id": request.target_id,
        "required_method": required_method,
    }
    if not request.confirmed or request.confirmation_text != expected_confirmation:
        return SafeMutationResult(
            action=request.action,
            target_id=request.target_id,
            status="confirmation_required",
            required_method=required_method,
            audit_event={**audit_event, "outcome": "blocked"},
            error="explicit confirmation required",
        )
    try:
        payload = dict(executor(request) if executor else {"ok": True})
    except Exception as exc:  # pragma: no cover - exception type is caller-owned.
        return SafeMutationResult(
            action=request.action,
            target_id=request.target_id,
            status="failed",
            required_method=required_method,
            audit_event={**audit_event, "outcome": "failed"},
            error=str(exc),
        )
    if payload.get("ok") is False:
        return SafeMutationResult(
            action=request.action,
            target_id=request.target_id,
            status="failed",
            required_method=required_method,
            audit_event={**audit_event, "outcome": "failed"},
            error=str(payload.get("error") or "mutation failed"),
        )
    return SafeMutationResult(
        action=request.action,
        target_id=request.target_id,
        status="executed",
        required_method=required_method,
        audit_event={**audit_event, "outcome": "executed"},
    )


def redact_sensitive_values(values: Mapping[str, Any]) -> dict[str, Any]:
    redacted: dict[str, Any] = {}
    for key, value in values.items():
        key_text = str(key)
        if _is_sensitive_key(key_text):
            redacted[key_text] = "[REDACTED]"
        elif isinstance(value, Mapping):
            redacted[key_text] = redact_sensitive_values(value)
        else:
            redacted[key_text] = value
    return redacted


def _is_sensitive_key(key: str) -> bool:
    normalized = key.lower().replace("-", "_")
    if normalized.startswith(("not_", "non_")):
        return False
    return any(normalized == token or normalized.endswith(f"_{token}") for token in SECRET_TOKENS)


def _warnings_for(readiness: Mapping[str, bool]) -> list[UnsafeStateWarning]:
    warning_messages = {
        "admin_authorized": "Administrator authorization is not active.",
        "readiness_healthy": "Readiness checks are degraded.",
        "contracts_valid": "Contract checks are failing.",
        "migrations_current": "Database migrations are not current.",
        "cookies_secure": "Cookie or TLS posture is unsafe.",
        "openrpc_available": "Required OpenRPC methods are unavailable.",
    }
    warnings: list[UnsafeStateWarning] = []
    for key, message in warning_messages.items():
        if not bool(readiness.get(key, False)):
            warnings.append(UnsafeStateWarning(code=key, message=message))
    return warnings
