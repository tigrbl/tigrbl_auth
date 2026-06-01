from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Mapping

from tigrbl_auth.config.deployment import ResolvedDeployment
from tigrbl_auth.services.operator_service import get_record
from tigrbl_auth.standards.oidc.discovery_metadata import build_openid_config

TENANT_OPENID_CONFIGURATION_PATH = "/tenants/{tenant_slug}/.well-known/openid-configuration"
TENANT_JWKS_PATH = "/tenants/{tenant_slug}/.well-known/jwks.json"
REALM_OPENID_CONFIGURATION_PATH = "/realms/{realm_slug}/.well-known/openid-configuration"
REALM_JWKS_PATH = "/realms/{realm_slug}/.well-known/jwks.json"


@dataclass(frozen=True, slots=True)
class TenantTrustDomainAuthority:
    tenant_slug: str
    issuer: str
    jwks_uri: str
    jwks_path: str
    subject_namespace: str
    protected_resource_identifier: str
    signing_scope: str
    accepted_issuers: tuple[str, ...]
    verification_scope: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RealmTrustDomainAuthority:
    realm_slug: str
    issuer: str
    jwks_uri: str
    jwks_path: str
    subject_namespace: str
    protected_resource_identifier: str
    signing_scope: str
    accepted_issuers: tuple[str, ...]
    verification_scope: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TenantPublicDiscoveryBoundaryFeature:
    feature_id: str
    category: str
    runtime_objects: tuple[str, ...]
    guarded_capabilities: tuple[str, ...]


TENANT_PUBLIC_DISCOVERY_FEATURES: tuple[TenantPublicDiscoveryBoundaryFeature, ...] = (
    TenantPublicDiscoveryBoundaryFeature("feat:tenant-scoped-issuer-boundary", "tenant-issuer", ("TenantTrustDomainAuthority", "tenant_issuer"), ("issuer-boundary", "tenant-scope")),
    TenantPublicDiscoveryBoundaryFeature("feat:route-tenant-openid-configuration", "route", ("build_tenant_openid_config", "TENANT_OPENID_CONFIGURATION_PATH"), ("route-enabled", "tenant-exists")),
    TenantPublicDiscoveryBoundaryFeature("feat:route-tenant-jwks-json", "route", ("TENANT_JWKS_PATH", "build_operator_jwks_payload"), ("route-enabled", "tenant-exists")),
    TenantPublicDiscoveryBoundaryFeature("feat:tenant-discovery-jwks-uri", "discovery-document", ("build_tenant_openid_config", "tenant_jwks_path"), ("jwks-uri", "issuer-root")),
    TenantPublicDiscoveryBoundaryFeature("feat:tenant-jwks-key-filtering", "jwks", ("build_operator_jwks_payload",), ("tenant-filtering", "public-key-only")),
    TenantPublicDiscoveryBoundaryFeature("feat:tenant-jwks-rotation-visibility", "jwks", ("build_operator_jwks_payload",), ("active-visible", "next-visible", "retired-hidden")),
    TenantPublicDiscoveryBoundaryFeature("feat:tenant-public-discovery-disabled-policy", "route-policy", ("enabled_tenant_record",), ("disabled-tenant-404", "missing-tenant-404")),
    TenantPublicDiscoveryBoundaryFeature("feat:operator-tenant-jwks-runtime-parity", "operator-parity", ("publish_jwks_document", "build_operator_jwks_payload"), ("runtime-payload-parity",)),
    TenantPublicDiscoveryBoundaryFeature("feat:openapi-tenant-discovery-routes", "contract", ("TENANT_OPENID_CONFIGURATION_PATH", "TENANT_JWKS_PATH"), ("openapi-route-parameters",)),
    TenantPublicDiscoveryBoundaryFeature("feat:discovery-snapshot-tenant-profile-artifacts", "snapshot", ("write_discovery_artifacts", "build_tenant_openid_config"), ("tenant-profile-artifacts",)),
    TenantPublicDiscoveryBoundaryFeature("feat:tenant-issuer-token-validation-contract", "validation", ("require_tenant_issuer", "TenantTrustDomainAuthority"), ("accepted-issuer-only",)),
    TenantPublicDiscoveryBoundaryFeature("feat:tenant-jwks-cross-tenant-leakage-guard", "leakage-guard", ("build_operator_jwks_payload", "build_tenant_openid_config"), ("cross-tenant-redaction", "tenant-path-isolation")),
)


def tenant_public_discovery_boundary_manifest() -> dict[str, dict[str, Any]]:
    return {
        feature.feature_id: {
            "category": feature.category,
            "runtime_objects": list(feature.runtime_objects),
            "guarded_capabilities": list(feature.guarded_capabilities),
        }
        for feature in TENANT_PUBLIC_DISCOVERY_FEATURES
    }


def tenant_public_discovery_boundary_integrity() -> dict[str, Any]:
    manifest = tenant_public_discovery_boundary_manifest()
    categories = {row["category"] for row in manifest.values()}
    failures: list[str] = []
    if len(manifest) != 12:
        failures.append("tenant public discovery boundary must track exactly 12 feature rows")
    if TENANT_OPENID_CONFIGURATION_PATH != "/tenants/{tenant_slug}/.well-known/openid-configuration":
        failures.append("tenant OpenID configuration path drifted")
    if TENANT_JWKS_PATH != "/tenants/{tenant_slug}/.well-known/jwks.json":
        failures.append("tenant JWKS path drifted")
    for required in ("tenant-issuer", "route", "jwks", "operator-parity", "contract", "snapshot", "validation", "leakage-guard"):
        if required not in categories:
            failures.append(f"missing category {required}")
    return {
        "passed": not failures,
        "feature_count": len(manifest),
        "categories": sorted(categories),
        "failures": failures,
    }


def tenant_issuer(root_issuer: str, tenant_slug: str) -> str:
    return f"{root_issuer.rstrip('/')}/tenants/{tenant_slug}"


def realm_issuer(root_issuer: str, realm_slug: str) -> str:
    return f"{root_issuer.rstrip('/')}/realms/{realm_slug}"


def realm_jwks_path(realm_slug: str) -> str:
    return REALM_JWKS_PATH.format(realm_slug=realm_slug)


def realm_openid_configuration_path(realm_slug: str) -> str:
    return REALM_OPENID_CONFIGURATION_PATH.format(realm_slug=realm_slug)


def tenant_jwks_path(tenant_slug: str) -> str:
    return TENANT_JWKS_PATH.format(tenant_slug=tenant_slug)


def tenant_openid_configuration_path(tenant_slug: str) -> str:
    return TENANT_OPENID_CONFIGURATION_PATH.format(tenant_slug=tenant_slug)


def resolve_tenant_trust_domain_authority(deployment: ResolvedDeployment, tenant_slug: str) -> TenantTrustDomainAuthority:
    issuer = tenant_issuer(deployment.issuer, tenant_slug)
    jwks_path = tenant_jwks_path(tenant_slug)
    protected_resource_identifier = f"{str(deployment.protected_resource_identifier).rstrip('/')}/tenants/{tenant_slug}"
    return TenantTrustDomainAuthority(
        tenant_slug=tenant_slug,
        issuer=issuer,
        jwks_uri=f"{str(deployment.issuer).rstrip('/')}{jwks_path}",
        jwks_path=jwks_path,
        subject_namespace=f"{tenant_slug}:subjects",
        protected_resource_identifier=protected_resource_identifier,
        signing_scope=f"tenant:{tenant_slug}",
        accepted_issuers=(issuer,),
        verification_scope=(issuer, protected_resource_identifier),
    )


def resolve_realm_trust_domain_authority(deployment: ResolvedDeployment, realm_slug: str) -> RealmTrustDomainAuthority:
    issuer = realm_issuer(deployment.issuer, realm_slug)
    jwks_path = realm_jwks_path(realm_slug)
    protected_resource_identifier = f"{str(deployment.protected_resource_identifier).rstrip('/')}/realms/{realm_slug}"
    return RealmTrustDomainAuthority(
        realm_slug=realm_slug,
        issuer=issuer,
        jwks_uri=f"{str(deployment.issuer).rstrip('/')}{jwks_path}",
        jwks_path=jwks_path,
        subject_namespace=f"realm:{realm_slug}:subjects",
        protected_resource_identifier=protected_resource_identifier,
        signing_scope=f"realm:{realm_slug}",
        accepted_issuers=(issuer,),
        verification_scope=(issuer, protected_resource_identifier),
    )


def tenant_trust_domain_authority_from_root_issuer(
    root_issuer: str,
    tenant_slug: str,
    *,
    protected_resource_identifier: str | None = None,
) -> TenantTrustDomainAuthority:
    issuer = tenant_issuer(root_issuer, tenant_slug)
    jwks_path = tenant_jwks_path(tenant_slug)
    resource_base = protected_resource_identifier or f"{str(root_issuer).rstrip('/')}/resource"
    resource = f"{str(resource_base).rstrip('/')}/tenants/{tenant_slug}"
    return TenantTrustDomainAuthority(
        tenant_slug=tenant_slug,
        issuer=issuer,
        jwks_uri=f"{str(root_issuer).rstrip('/')}{jwks_path}",
        jwks_path=jwks_path,
        subject_namespace=f"{tenant_slug}:subjects",
        protected_resource_identifier=resource,
        signing_scope=f"tenant:{tenant_slug}",
        accepted_issuers=(issuer,),
        verification_scope=(issuer, resource),
    )


def enabled_tenant_record(repo_root: Path, tenant_slug: str) -> dict[str, Any] | None:
    record = get_record(repo_root, "tenant", tenant_slug)
    if record is None:
        return None
    status = str(record.get("status") or "").lower()
    if status in {"deleted", "disabled", "revoked"}:
        return None
    if record.get("enabled") is False:
        return None
    return record


def tenant_deployment(deployment: ResolvedDeployment, tenant_slug: str) -> ResolvedDeployment:
    authority = resolve_tenant_trust_domain_authority(deployment, tenant_slug)
    return replace(
        deployment,
        issuer=authority.issuer,
        protected_resource_identifier=authority.protected_resource_identifier,
    )


def realm_deployment(deployment: ResolvedDeployment, realm_slug: str) -> ResolvedDeployment:
    authority = resolve_realm_trust_domain_authority(deployment, realm_slug)
    return replace(
        deployment,
        issuer=authority.issuer,
        protected_resource_identifier=authority.protected_resource_identifier,
    )


def build_tenant_openid_config(deployment: ResolvedDeployment, tenant_slug: str) -> dict[str, Any]:
    authority = resolve_tenant_trust_domain_authority(deployment, tenant_slug)
    tenant_scoped = tenant_deployment(deployment, tenant_slug)
    config = build_openid_config(tenant_scoped)
    config["issuer"] = authority.issuer
    config["jwks_uri"] = authority.jwks_uri
    config["tigrbl_auth_subject_namespace"] = authority.subject_namespace
    config["tigrbl_auth_signing_scope"] = authority.signing_scope
    return config


def build_realm_openid_config(deployment: ResolvedDeployment, realm_slug: str) -> dict[str, Any]:
    authority = resolve_realm_trust_domain_authority(deployment, realm_slug)
    realm_scoped = realm_deployment(deployment, realm_slug)
    config = build_openid_config(realm_scoped)
    config["issuer"] = authority.issuer
    config["jwks_uri"] = authority.jwks_uri
    config["tigrbl_auth_subject_namespace"] = authority.subject_namespace
    config["tigrbl_auth_signing_scope"] = authority.signing_scope
    return config


def require_tenant_issuer(payload: Mapping[str, Any], *, root_issuer: str, tenant_slug: str) -> None:
    authority = tenant_trust_domain_authority_from_root_issuer(root_issuer, tenant_slug)
    actual = str(payload.get("iss") or "")
    if actual not in set(authority.accepted_issuers):
        raise ValueError(f"tenant token issuer mismatch: expected {authority.issuer!r}, got {actual!r}")


__all__ = [
    "REALM_JWKS_PATH",
    "REALM_OPENID_CONFIGURATION_PATH",
    "RealmTrustDomainAuthority",
    "TenantTrustDomainAuthority",
    "TenantPublicDiscoveryBoundaryFeature",
    "TENANT_JWKS_PATH",
    "TENANT_OPENID_CONFIGURATION_PATH",
    "TENANT_PUBLIC_DISCOVERY_FEATURES",
    "build_realm_openid_config",
    "build_tenant_openid_config",
    "enabled_tenant_record",
    "require_tenant_issuer",
    "realm_deployment",
    "realm_issuer",
    "realm_jwks_path",
    "realm_openid_configuration_path",
    "resolve_realm_trust_domain_authority",
    "resolve_tenant_trust_domain_authority",
    "tenant_public_discovery_boundary_integrity",
    "tenant_public_discovery_boundary_manifest",
    "tenant_trust_domain_authority_from_root_issuer",
    "tenant_deployment",
    "tenant_issuer",
    "tenant_jwks_path",
    "tenant_openid_configuration_path",
]
