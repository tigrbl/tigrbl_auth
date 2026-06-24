from __future__ import annotations
# ruff: noqa: F403,F405

from .shell_state import *

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
        from .runtime_actions import _warnings_for, redact_sensitive_values

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


