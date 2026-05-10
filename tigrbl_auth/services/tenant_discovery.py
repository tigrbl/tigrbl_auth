from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any, Mapping

from tigrbl_auth.config.deployment import ResolvedDeployment
from tigrbl_auth.services.operator_service import get_record
from tigrbl_auth.standards.oidc.discovery_metadata import build_openid_config

TENANT_OPENID_CONFIGURATION_PATH = "/tenants/{tenant_slug}/.well-known/openid-configuration"
TENANT_JWKS_PATH = "/tenants/{tenant_slug}/.well-known/jwks.json"


def tenant_issuer(root_issuer: str, tenant_slug: str) -> str:
    return f"{root_issuer.rstrip('/')}/tenants/{tenant_slug}"


def tenant_jwks_path(tenant_slug: str) -> str:
    return TENANT_JWKS_PATH.format(tenant_slug=tenant_slug)


def tenant_openid_configuration_path(tenant_slug: str) -> str:
    return TENANT_OPENID_CONFIGURATION_PATH.format(tenant_slug=tenant_slug)


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
    return replace(deployment, issuer=tenant_issuer(deployment.issuer, tenant_slug))


def build_tenant_openid_config(deployment: ResolvedDeployment, tenant_slug: str) -> dict[str, Any]:
    tenant_scoped = tenant_deployment(deployment, tenant_slug)
    config = build_openid_config(tenant_scoped)
    config["issuer"] = tenant_scoped.issuer
    config["jwks_uri"] = f"{deployment.issuer}{tenant_jwks_path(tenant_slug)}"
    return config


def require_tenant_issuer(payload: Mapping[str, Any], *, root_issuer: str, tenant_slug: str) -> None:
    expected = tenant_issuer(root_issuer, tenant_slug)
    actual = str(payload.get("iss") or "")
    if actual != expected:
        raise ValueError(f"tenant token issuer mismatch: expected {expected!r}, got {actual!r}")


__all__ = [
    "TENANT_JWKS_PATH",
    "TENANT_OPENID_CONFIGURATION_PATH",
    "build_tenant_openid_config",
    "enabled_tenant_record",
    "require_tenant_issuer",
    "tenant_deployment",
    "tenant_issuer",
    "tenant_jwks_path",
    "tenant_openid_configuration_path",
]
