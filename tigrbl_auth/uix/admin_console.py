from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Callable, Mapping


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
        now = datetime.now(tz=UTC).isoformat()
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


@dataclass(frozen=True, slots=True)
class ResourceView:
    name: str
    required_methods: tuple[str, ...]
    missing_methods: tuple[str, ...]
    states: tuple[str, ...] = RESOURCE_VIEW_STATES

    @property
    def backed(self) -> bool:
        return not self.missing_methods


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


@dataclass(frozen=True, slots=True)
class Role:
    name: str
    permissions: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AttributePolicy:
    name: str
    permission: str
    required_attributes: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    allowed: bool
    reason: str
    matched: tuple[str, ...] = ()


class RBACAdministration:
    def __init__(self) -> None:
        self._roles: dict[str, Role] = {}
        self._assignments: dict[str, set[str]] = {}

    @property
    def roles(self) -> Mapping[str, Role]:
        return dict(self._roles)

    @property
    def assignments(self) -> Mapping[str, tuple[str, ...]]:
        return {subject: tuple(sorted(roles)) for subject, roles in self._assignments.items()}

    def upsert_role(self, name: str, permissions: tuple[str, ...]) -> Role:
        if not name or not permissions:
            raise ValueError("role name and permissions are required")
        role = Role(name=name, permissions=tuple(sorted(set(permissions))))
        self._roles[name] = role
        return role

    def assign_role(self, subject: str, role_name: str) -> None:
        if role_name not in self._roles:
            raise KeyError(f"unknown role {role_name!r}")
        self._assignments.setdefault(subject, set()).add(role_name)

    def decide(self, subject: str, permission: str) -> PolicyDecision:
        matched = tuple(
            role_name
            for role_name in sorted(self._assignments.get(subject, set()))
            if permission in self._roles[role_name].permissions
        )
        if matched:
            return PolicyDecision(True, "permission granted by assigned role", matched)
        return PolicyDecision(False, "permission denied by RBAC role assignments", ())


class ABACAdministration:
    def __init__(self) -> None:
        self._policies: dict[str, AttributePolicy] = {}

    @property
    def policies(self) -> Mapping[str, AttributePolicy]:
        return dict(self._policies)

    def upsert_policy(
        self,
        name: str,
        *,
        permission: str,
        required_attributes: Mapping[str, Any],
    ) -> AttributePolicy:
        if not name or not permission or not required_attributes:
            raise ValueError("policy name, permission, and attributes are required")
        policy = AttributePolicy(
            name=name,
            permission=permission,
            required_attributes=dict(required_attributes),
        )
        self._policies[name] = policy
        return policy

    def decide(self, *, permission: str, attributes: Mapping[str, Any]) -> PolicyDecision:
        matched: list[str] = []
        for policy in self._policies.values():
            if policy.permission != permission:
                continue
            if all(attributes.get(key) == value for key, value in policy.required_attributes.items()):
                matched.append(policy.name)
        if matched:
            return PolicyDecision(True, "permission granted by matching attributes", tuple(sorted(matched)))
        return PolicyDecision(False, "permission denied by ABAC attributes", ())


def build_resource_views(available_methods: set[str] | tuple[str, ...] | list[str]) -> dict[str, ResourceView]:
    available = set(available_methods)
    views: dict[str, ResourceView] = {}
    for name, required_methods in RESOURCE_VIEW_METHODS.items():
        missing = tuple(method for method in required_methods if method not in available)
        views[name] = ResourceView(name=name, required_methods=required_methods, missing_methods=missing)
    return views


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


def simulate_policy(
    *,
    rbac: RBACAdministration,
    abac: ABACAdministration,
    subject: str,
    permission: str,
    attributes: Mapping[str, Any],
) -> PolicyDecision:
    rbac_decision = rbac.decide(subject, permission)
    abac_decision = abac.decide(permission=permission, attributes=attributes)
    if rbac_decision.allowed and abac_decision.allowed:
        return PolicyDecision(
            True,
            "permission granted by RBAC assignment and ABAC attributes",
            rbac_decision.matched + abac_decision.matched,
        )
    reasons = [rbac_decision.reason, abac_decision.reason]
    return PolicyDecision(False, "; ".join(reasons), rbac_decision.matched + abac_decision.matched)


def redact_sensitive_values(values: Mapping[str, Any]) -> dict[str, Any]:
    redacted: dict[str, Any] = {}
    for key, value in values.items():
        key_text = str(key)
        if any(token in key_text.lower() for token in SECRET_TOKENS):
            redacted[key_text] = "[REDACTED]"
        elif isinstance(value, Mapping):
            redacted[key_text] = redact_sensitive_values(value)
        else:
            redacted[key_text] = value
    return redacted


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
