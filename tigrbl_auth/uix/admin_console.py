from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Mapping


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
