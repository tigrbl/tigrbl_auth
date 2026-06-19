from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Mapping

from tigrbl_user_plane_contracts.trust_domains import (
    RealmTrustDomainAuthority,
    TenantTrustDomainAuthority,
)

TENANT_OPENID_CONFIGURATION_PATH = "/tenants/{tenant_slug}/.well-known/openid-configuration"
TENANT_JWKS_PATH = "/tenants/{tenant_slug}/.well-known/jwks.json"
REALM_OPENID_CONFIGURATION_PATH = "/realms/{realm_slug}/.well-known/openid-configuration"
REALM_JWKS_PATH = "/realms/{realm_slug}/.well-known/jwks.json"


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


def _deployment_value(deployment: object, name: str, default: str | None = None) -> str:
    value = getattr(deployment, name, default)
    if value is None:
        raise ValueError(f"deployment.{name} is required")
    return str(value)


def resolve_tenant_trust_domain_authority(deployment: object, tenant_slug: str) -> TenantTrustDomainAuthority:
    root_issuer = _deployment_value(deployment, "issuer")
    issuer = tenant_issuer(root_issuer, tenant_slug)
    jwks_path = tenant_jwks_path(tenant_slug)
    protected_resource_identifier = (
        f"{_deployment_value(deployment, 'protected_resource_identifier', root_issuer).rstrip('/')}/tenants/{tenant_slug}"
    )
    return TenantTrustDomainAuthority(
        tenant_slug=tenant_slug,
        issuer=issuer,
        jwks_uri=f"{root_issuer.rstrip('/')}{jwks_path}",
        jwks_path=jwks_path,
        subject_namespace=f"{tenant_slug}:subjects",
        protected_resource_identifier=protected_resource_identifier,
        signing_scope=f"tenant:{tenant_slug}",
        accepted_issuers=(issuer,),
        verification_scope=(issuer, protected_resource_identifier),
    )


def resolve_realm_trust_domain_authority(deployment: object, realm_slug: str) -> RealmTrustDomainAuthority:
    root_issuer = _deployment_value(deployment, "issuer")
    issuer = realm_issuer(root_issuer, realm_slug)
    jwks_path = realm_jwks_path(realm_slug)
    protected_resource_identifier = (
        f"{_deployment_value(deployment, 'protected_resource_identifier', root_issuer).rstrip('/')}/realms/{realm_slug}"
    )
    return RealmTrustDomainAuthority(
        realm_slug=realm_slug,
        issuer=issuer,
        jwks_uri=f"{root_issuer.rstrip('/')}{jwks_path}",
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
    record_path = Path(repo_root) / ".operator-state" / "tenant" / f"{tenant_slug}.json"
    if not record_path.exists():
        return None
    import json

    record = json.loads(record_path.read_text(encoding="utf-8"))
    if record is None:
        return None
    status = str(record.get("status") or "").lower()
    if status in {"deleted", "disabled", "revoked"}:
        return None
    if record.get("enabled") is False:
        return None
    return record


def tenant_deployment(deployment: object, tenant_slug: str) -> object:
    authority = resolve_tenant_trust_domain_authority(deployment, tenant_slug)
    try:
        return replace(
            deployment,
            issuer=authority.issuer,
            protected_resource_identifier=authority.protected_resource_identifier,
        )
    except TypeError:
        values = dict(getattr(deployment, "__dict__", {}))
        values["issuer"] = authority.issuer
        values["protected_resource_identifier"] = authority.protected_resource_identifier
        return SimpleNamespace(**values)


def realm_deployment(deployment: object, realm_slug: str) -> object:
    authority = resolve_realm_trust_domain_authority(deployment, realm_slug)
    try:
        return replace(
            deployment,
            issuer=authority.issuer,
            protected_resource_identifier=authority.protected_resource_identifier,
        )
    except TypeError:
        values = dict(getattr(deployment, "__dict__", {}))
        values["issuer"] = authority.issuer
        values["protected_resource_identifier"] = authority.protected_resource_identifier
        return SimpleNamespace(**values)


def build_tenant_openid_config(deployment: object, tenant_slug: str) -> dict[str, Any]:
    authority = resolve_tenant_trust_domain_authority(deployment, tenant_slug)
    root = _deployment_value(deployment, "issuer")
    base = root.rstrip("/")
    return {
        "issuer": authority.issuer,
        "authorization_endpoint": f"{base}/authorize",
        "token_endpoint": f"{base}/token",
        "jwks_uri": authority.jwks_uri,
        "userinfo_endpoint": f"{base}/userinfo",
        "response_types_supported": ["code"],
        "subject_types_supported": ["public"],
        "id_token_signing_alg_values_supported": list(getattr(deployment, "id_token_algs", ("ES256",))),
        "scopes_supported": ["openid", "profile", "email"],
        "tigrbl_auth_subject_namespace": authority.subject_namespace,
        "tigrbl_auth_signing_scope": authority.signing_scope,
    }


def build_realm_openid_config(deployment: object, realm_slug: str) -> dict[str, Any]:
    authority = resolve_realm_trust_domain_authority(deployment, realm_slug)
    root = _deployment_value(deployment, "issuer")
    base = root.rstrip("/")
    return {
        "issuer": authority.issuer,
        "authorization_endpoint": f"{base}/authorize",
        "token_endpoint": f"{base}/token",
        "jwks_uri": authority.jwks_uri,
        "userinfo_endpoint": f"{base}/userinfo",
        "response_types_supported": ["code"],
        "subject_types_supported": ["public"],
        "id_token_signing_alg_values_supported": list(getattr(deployment, "id_token_algs", ("ES256",))),
        "scopes_supported": ["openid", "profile", "email"],
        "tigrbl_auth_subject_namespace": authority.subject_namespace,
        "tigrbl_auth_signing_scope": authority.signing_scope,
    }


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
    "TENANT_JWKS_PATH",
    "TENANT_OPENID_CONFIGURATION_PATH",
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
    "tenant_trust_domain_authority_from_root_issuer",
    "tenant_deployment",
    "tenant_issuer",
    "tenant_jwks_path",
    "tenant_openid_configuration_path",
]
