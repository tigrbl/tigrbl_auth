"""Authorization policy service ports."""

from __future__ import annotations

from typing import Any, Callable, Iterable, Mapping, Protocol

from ..audit.policy import PolicyAuditEvent
from ..authority import Role
from ..delegation import DelegatedAdminScope
from ..invariants import (
    AuthorizationInvariant,
    InvariantEvaluation,
    InvariantViolation,
)
from ..authentication import ServiceIdentityAuthentication
from .conditions import DynamicCondition
from .decisions import PolicyDecision, PolicyTrace
from .requests import PolicyRequest
from .rules import PolicyRule


class PolicyDecisionEnginePort(Protocol):
    @property
    def traces(self) -> tuple[PolicyTrace, ...]: ...

    def decide_rbac(self, request: PolicyRequest) -> PolicyDecision: ...

    def decide_abac(self, request: PolicyRequest) -> PolicyDecision: ...

    def decide_pbac(self, request: PolicyRequest) -> PolicyDecision: ...

    def decide_delegation(self, request: PolicyRequest) -> PolicyDecision: ...

    def decide_admin(self, request: PolicyRequest) -> PolicyDecision: ...

    def evaluate(self, request: PolicyRequest) -> PolicyDecision: ...


class RuleEvaluatorPort(Protocol):
    def evaluate_rule(
        self, rule: PolicyRule, request: PolicyRequest, /
    ) -> PolicyDecision: ...


class ConditionEvaluatorPort(Protocol):
    def evaluate_condition(
        self, condition: DynamicCondition, request: PolicyRequest, /
    ) -> bool: ...


class AdminGatePort(Protocol):
    async def authorize_admin_action(
        self, request: PolicyRequest, /
    ) -> PolicyDecision: ...


class RBACAdministratorPort(Protocol):
    async def upsert_role(
        self,
        name: str,
        permissions: tuple[str, ...],
        *,
        tenant_id: str | None = None,
        denied_permissions: tuple[str, ...] = (),
        inherited_roles: tuple[str, ...] = (),
    ) -> Role: ...

    async def assign_role(
        self,
        subject: str,
        role_name: str,
        *,
        tenant_id: str | None = None,
    ) -> None: ...

    async def assignments_for(
        self,
        subject: str,
        tenant_id: str | None = None,
    ) -> tuple[str, ...]: ...

    async def list_roles(self, tenant_id: str | None = None) -> tuple[Role, ...]: ...

    async def effective_permissions(
        self,
        subject: str,
        tenant_id: str | None = None,
    ) -> tuple[str, ...]: ...

    async def decide(
        self,
        subject: str,
        permission: str,
        tenant_id: str | None = None,
    ) -> PolicyDecision: ...

    async def summary(self, tenant_id: str | None = None) -> dict[str, Any]: ...


class ABACAdministratorPort(Protocol):
    async def upsert_policy(
        self,
        name: str,
        *,
        permission: str,
        required_attributes: Mapping[str, Any],
        tenant_id: str | None = None,
        dynamic_conditions: Iterable[Any] = (),
        effect: str = "allow",
        client_id: str | None = None,
    ) -> Any: ...

    async def has_relevant_policy(
        self,
        permission: str,
        tenant_id: str | None = None,
        client_id: str | None = None,
    ) -> bool: ...

    async def decide(
        self,
        *,
        permission: str,
        attributes: Mapping[str, Any],
        tenant_id: str | None = None,
        client_id: str | None = None,
    ) -> PolicyDecision: ...

    async def list_policies(self) -> tuple[Any, ...]: ...

    async def summary(self) -> dict[str, Any]: ...


class DelegatedAdministratorPort(Protocol):
    async def grant_scope(
        self,
        subject: str,
        *,
        tenant_ids: Iterable[str],
        permissions: Iterable[str],
        visible_client_fields: Iterable[str] = ...,
        mutable_client_fields: Iterable[str] = ...,
        service_identity_permissions: Iterable[str] = (),
    ) -> DelegatedAdminScope: ...

    async def revoke_scope(self, subject: str) -> DelegatedAdminScope | None: ...

    async def scope_for(self, subject: str) -> DelegatedAdminScope | None: ...

    async def authorize(
        self,
        subject: str,
        *,
        tenant_id: str,
        permission: str,
        patch_fields: Iterable[str] = (),
    ) -> PolicyDecision: ...

    async def visible_tenant_ids(
        self,
        subject: str,
        tenant_ids: Iterable[str],
    ) -> tuple[str, ...]: ...

    async def visible_client_fields_for(self, subject: str) -> tuple[str, ...]: ...

    async def summary(self) -> dict[str, Any]: ...


class PolicyEnginePort(Protocol):
    @property
    def audit_events(self) -> tuple[PolicyAuditEvent, ...]: ...

    async def evaluate(
        self,
        *,
        subject: str,
        permission: str,
        tenant_id: str,
        attributes: Mapping[str, Any],
        actor_type: str = "user",
        client_id: str | None = None,
        service_auth: ServiceIdentityAuthentication | None = None,
        patch_fields: Iterable[str] = (),
    ) -> PolicyDecision: ...

    async def compliance_report(
        self,
        *,
        service_registry: Any,
        tenants: Iterable[Mapping[str, Any]],
        clients: Iterable[Mapping[str, Any]],
    ) -> dict[str, Any]: ...


class ServiceIdentityRegistryPort(Protocol):
    @property
    def services(self) -> Mapping[str, Any]: ...

    @property
    def credentials(self) -> Mapping[str, Any]: ...

    def register_service(
        self,
        service_id: str,
        *,
        tenant_id: str,
        name: str,
        scopes: Iterable[str],
        enabled: bool = True,
    ) -> Any: ...

    def disable_service(self, service_id: str) -> Any: ...

    def issue_credential(
        self,
        service_id: str,
        *,
        label: str,
        raw_key: str | None = None,
        expires_at: str | None = None,
    ) -> Any: ...

    def revoke_credential(self, credential_id: str) -> Any: ...

    def authenticate(
        self,
        raw_key: str,
        *,
        tenant_id: str,
        required_permission: str | None = None,
    ) -> ServiceIdentityAuthentication: ...

    def summary(self) -> dict[str, Any]: ...


class InvariantEvaluator(Protocol):
    def __call__(
        self,
        invariant: AuthorizationInvariant,
    ) -> bool | InvariantEvaluation: ...


class InvariantRegistryPort(Protocol):
    @property
    def invariants(self) -> Mapping[str, AuthorizationInvariant]: ...

    def register(self, invariant: AuthorizationInvariant) -> AuthorizationInvariant: ...

    def get(self, invariant_id: str) -> AuthorizationInvariant: ...

    def list(
        self,
        *,
        property_family: str | None = None,
        enabled_only: bool = False,
        tags: Iterable[str] = (),
    ) -> tuple[AuthorizationInvariant, ...]: ...

    def evaluate(
        self,
        invariant_id: str,
        evaluator: Callable[[AuthorizationInvariant], bool | InvariantEvaluation],
    ) -> InvariantEvaluation: ...

    def violations(
        self,
        evaluations: Iterable[InvariantEvaluation],
    ) -> tuple[InvariantViolation, ...]: ...


__all__ = [
    "ABACAdministratorPort",
    "AdminGatePort",
    "ConditionEvaluatorPort",
    "DelegatedAdministratorPort",
    "InvariantEvaluator",
    "InvariantRegistryPort",
    "PolicyDecisionEnginePort",
    "PolicyEnginePort",
    "RBACAdministratorPort",
    "RuleEvaluatorPort",
    "ServiceIdentityRegistryPort",
]
