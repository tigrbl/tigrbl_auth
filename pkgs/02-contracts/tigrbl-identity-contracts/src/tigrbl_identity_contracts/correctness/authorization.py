from __future__ import annotations

from dataclasses import dataclass

from ..invariants import InvariantEvaluation


@dataclass(frozen=True, slots=True)
class SafetyPropertyResult:
    passed: bool
    evaluations: tuple[InvariantEvaluation, ...]
    failures: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ReferenceCatalog:
    subjects: tuple[str, ...] = ()
    tenants: tuple[str, ...] = ()
    realms: tuple[str, ...] = ()
    policies: tuple[str, ...] = ()
    delegations: tuple[str, ...] = ()
    trust_domains: tuple[str, ...] = ()
    authority_nodes: tuple[str, ...] = ()
    provenance_ids: tuple[str, ...] = ()
    policy_versions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for field_name in (
            "subjects",
            "tenants",
            "realms",
            "policies",
            "delegations",
            "trust_domains",
            "authority_nodes",
            "provenance_ids",
            "policy_versions",
        ):
            object.__setattr__(self, field_name, tuple(sorted(set(getattr(self, field_name)))))


@dataclass(frozen=True, slots=True)
class AuthorizationReference:
    ref_id: str
    ref_type: str
    target_id: str
    source_id: str = ""

    def __post_init__(self) -> None:
        if not self.ref_id or not self.ref_type or not self.target_id:
            raise ValueError("ref_id, ref_type, and target_id are required")


@dataclass(frozen=True, slots=True)
class IntegrityReport:
    passed: bool
    failures: tuple[str, ...]
    checked_count: int


@dataclass(frozen=True, slots=True)
class TrustEdge:
    edge_id: str
    issuer: str
    subject: str
    tenant_id: str
    trust_domain: str
    revoked: bool = False
    subject_tenant_id: str = ""
    subject_trust_domain: str = ""

    def __post_init__(self) -> None:
        if not self.edge_id or not self.issuer or not self.subject or not self.tenant_id or not self.trust_domain:
            raise ValueError("edge_id, issuer, subject, tenant_id, and trust_domain are required")


@dataclass(frozen=True, slots=True)
class TenantRealmIsolationReport:
    passed: bool
    subject: str
    failures: tuple[str, ...]
    checked_path_count: int
    expected_tenant_id: str = ""
    expected_realm: str = ""


__all__ = [
    "AuthorizationReference",
    "IntegrityReport",
    "ReferenceCatalog",
    "SafetyPropertyResult",
    "TenantRealmIsolationReport",
    "TrustEdge",
]
