"""Identity administration service ports."""

from __future__ import annotations

from typing import Any, Iterable, Mapping, Protocol

from .adaptive_access import (
    AccessDecisionRequest,
    AccessDecisionResponse,
    AnomalySignal,
    AuthTelemetryEvent,
    GraphDecision,
    RelationshipDefinition,
    RelationshipTuple,
    TrustDomain,
    TrustEdge,
    TrustPath,
)
from .admin_resources import AdminResource, AdminResourceKind, AdminResourceStatus
from .audit.admin import AdminAuditEvent
from .authentication import AuthenticationChallenge
from .federation import FederatedSession, IdentityProvider
from .policy.definitions import PolicyDefinition
from .policy.versions import PolicyVersion


class AdminControlPlanePort(Protocol):
    @property
    def audit_events(self) -> tuple[AdminAuditEvent, ...]: ...

    def get(
        self,
        kind: AdminResourceKind | str,
        resource_id: str,
        *,
        tenant_id: str,
    ) -> object: ...

    def metadata(
        self,
        kind: AdminResourceKind | str,
        resource_id: str,
        *,
        tenant_id: str,
    ) -> AdminResource: ...

    def list(self, kind: AdminResourceKind | str, *, tenant_id: str) -> tuple[object, ...]: ...

    def update(
        self,
        kind: AdminResourceKind | str,
        resource_id: str,
        *,
        actor: str,
        tenant_id: str,
        name: str | None = None,
        attributes: Mapping[str, Any] | None = None,
        status: AdminResourceStatus | str | None = None,
    ) -> object: ...

    def delete(
        self,
        kind: AdminResourceKind | str,
        resource_id: str,
        *,
        actor: str,
        tenant_id: str,
    ) -> AdminResource: ...


class RelationshipGraphPort(Protocol):
    @property
    def definitions(self) -> Mapping[tuple[str, str], RelationshipDefinition]: ...

    @property
    def tuples(self) -> tuple[RelationshipTuple, ...]: ...

    def define_relation(
        self,
        *,
        resource_type: str,
        relation: str,
        subject_types: Iterable[str],
    ) -> RelationshipDefinition: ...

    def add_tuple(
        self,
        *,
        resource_type: str,
        resource_id: str,
        relation: str,
        subject_type: str,
        subject_id: str,
        tenant_id: str,
    ) -> RelationshipTuple: ...

    def check_access(
        self,
        *,
        tenant_id: str,
        subject: str,
        relation: str,
        resource: str,
        max_depth: int = 5,
    ) -> GraphDecision: ...


class PolicyRegistryPort(Protocol):
    @property
    def definitions(self) -> Mapping[str, PolicyDefinition]: ...

    @property
    def versions(self) -> Mapping[str, PolicyVersion]: ...

    def create_policy(
        self,
        *,
        tenant_id: str,
        name: str,
        language: str = "tigrbl-conditions/v1",
    ) -> PolicyDefinition: ...

    def publish_version(
        self,
        *,
        policy_id: str,
        source: str,
        promote: bool = True,
    ) -> PolicyVersion: ...

    def promote_version(self, version_id: str) -> PolicyVersion: ...

    def rollback_policy(self, *, policy_id: str, version_id: str) -> PolicyVersion: ...

    def check_compatibility(
        self,
        *,
        left_version_id: str,
        right_version_id: str,
    ) -> bool: ...

    def access_decision(self, request: AccessDecisionRequest) -> AccessDecisionResponse: ...


class FederationRegistryPort(Protocol):
    @property
    def providers(self) -> Mapping[str, IdentityProvider]: ...

    def register_provider(self, **kwargs: Any) -> IdentityProvider: ...

    def rotate_provider_keys(self, provider_id: str) -> IdentityProvider: ...

    def normalize_claims(self, provider_id: str, claims: Mapping[str, Any]) -> dict[str, Any]: ...

    def bind_session(self, **kwargs: Any) -> FederatedSession: ...

    def summary(self) -> dict[str, Any]: ...


class TrustFederationGraphPort(Protocol):
    @property
    def domains(self) -> Mapping[str, TrustDomain]: ...

    @property
    def edges(self) -> tuple[TrustEdge, ...]: ...

    def add_domain(self, *, name: str, issuers: Iterable[str], clouds: Iterable[str]) -> TrustDomain: ...

    def add_edge(self, **kwargs: Any) -> TrustEdge: ...

    def revoke_edge(self, *, source_domain: str, target_domain: str) -> TrustEdge: ...

    def resolve_path(
        self,
        *,
        source_domain: str,
        target_domain: str,
        max_hops: int = 5,
    ) -> TrustPath: ...

    def map_cross_cloud_workload(self, **kwargs: Any) -> dict[str, Any]: ...


class AuthAnomalyDetectorPort(Protocol):
    @property
    def events(self) -> tuple[AuthTelemetryEvent, ...]: ...

    def record_event(self, **kwargs: Any) -> tuple[AuthTelemetryEvent, AnomalySignal | None]: ...

    def summary(self) -> dict[str, Any]: ...


class AdvancedAuthenticatorRegistryPort(Protocol):
    @property
    def passwordless_credentials(self) -> Mapping[str, Any]: ...

    @property
    def mfa_factors(self) -> Mapping[str, Any]: ...

    @property
    def webauthn_credentials(self) -> Mapping[str, Any]: ...

    def begin_passwordless_assertion(self, **kwargs: Any) -> tuple[AuthenticationChallenge, Any]: ...

    def complete_passwordless_assertion(self, **kwargs: Any) -> AuthenticationChallenge: ...

    def begin_mfa_challenge(self, **kwargs: Any) -> AuthenticationChallenge: ...

    def complete_mfa_challenge(self, **kwargs: Any) -> AuthenticationChallenge: ...

    def summary(self) -> dict[str, Any]: ...


__all__ = [
    "AdminControlPlanePort",
    "AdvancedAuthenticatorRegistryPort",
    "AuthAnomalyDetectorPort",
    "FederationRegistryPort",
    "PolicyRegistryPort",
    "RelationshipGraphPort",
    "TrustFederationGraphPort",
]
