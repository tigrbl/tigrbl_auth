"""OIDC discovery and JWKS orchestration without HTTP route ownership."""

from __future__ import annotations

import asyncio
import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from tigrbl.runtime.status import HTTPException, status
from tigrbl_auth_protocol_oauth.standards.authorization_server_metadata import (
    ISSUER,
    JWKS_PATH,
)
from tigrbl_auth_protocol_oidc.jwks_service import build_jwks_document
from tigrbl_auth_protocol_oidc.standards.discovery_metadata import (
    build_openid_config,
)
from tigrbl_auth_protocol_oidc.tenant_discovery import (
    REALM_JWKS_PATH,
    REALM_OPENID_CONFIGURATION_PATH,
    TENANT_JWKS_PATH,
    TENANT_OPENID_CONFIGURATION_PATH,
    build_realm_openid_config,
    build_tenant_openid_config,
)
from tigrbl_identity_runtime.deployment import (
    ResolvedDeployment,
    deployment_from_request,
    resolve_deployment,
)
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_storage.tables import Realm, Tenant
from tigrbl_identity_storage.tables.operator_record import OperatorRecord
from tigrbl_identity_storage_runtime.ops.common import first_record
from tigrbl_identity_storage_runtime.resource_service import (
    build_operator_jwks_payload,
    get_record,
)


def _settings_signature(
    settings_obj: object | None = None,
    *,
    profile: str | None = None,
    flag_overrides: dict[str, Any] | None = None,
) -> str:
    deployment = resolve_deployment(
        settings_obj or settings,
        profile=profile,
        flag_overrides=flag_overrides,
    )
    return json.dumps(deployment.to_manifest(), sort_keys=True)


def _build_openid_config(
    settings_obj: object | ResolvedDeployment | None = None,
    *,
    profile: str | None = None,
    flag_overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_openid_config(
        settings_obj or settings,
        profile=profile,
        flag_overrides=flag_overrides,
    )


@lru_cache(maxsize=8)
def _cached_openid_config(signature: str) -> dict[str, Any]:
    try:
        manifest = json.loads(signature)
        if isinstance(manifest, dict):
            return _build_openid_config(ResolvedDeployment(**manifest))
    except Exception:
        pass
    return _build_openid_config()


def refresh_discovery_cache() -> None:
    _cached_openid_config.cache_clear()


async def _operator_record(
    *,
    db: object | None,
    resource: str,
    record_id: str,
) -> dict[str, Any] | None:
    if db is None:
        return await asyncio.to_thread(get_record, Path.cwd(), resource, record_id)
    try:
        records = await OperatorRecord.load_records(db, resource)
    except Exception:
        return await asyncio.to_thread(get_record, Path.cwd(), resource, record_id)
    return records.get(str(record_id))


def _tenant_record_enabled(record: dict[str, Any] | None) -> bool:
    if record is None:
        return False
    if str(record.get("status") or "").lower() in {
        "deleted",
        "disabled",
        "revoked",
    }:
        return False
    return record.get("enabled") is not False


async def _tenant_exists(*, db: object | None, tenant_slug: str) -> bool:
    if tenant_slug == "public":
        return True
    operator_record = await _operator_record(
        db=db,
        resource="tenant",
        record_id=tenant_slug,
    )
    operator_fallback = _tenant_record_enabled(operator_record)
    if db is None:
        return operator_fallback
    try:
        tenant = await first_record(Tenant, db, {"slug": tenant_slug})
    except Exception:
        return operator_fallback
    return tenant is not None or operator_fallback


async def _realm_exists(*, db: object | None, realm_slug: str) -> bool:
    if realm_slug == "default":
        return True
    if db is None:
        return False
    try:
        realm = await first_record(Realm, db, {"slug": realm_slug})
    except Exception:
        return False
    return realm is not None


async def openid_configuration(request: object) -> dict[str, Any]:
    deployment = deployment_from_request(request, settings)
    if not deployment.route_enabled("/.well-known/openid-configuration"):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "OIDC discovery disabled")
    return build_openid_config(deployment)


async def tenant_openid_configuration(
    request: object,
    tenant_slug: str,
    db: object | None,
) -> dict[str, Any]:
    deployment = deployment_from_request(request, settings)
    if not deployment.route_enabled(TENANT_OPENID_CONFIGURATION_PATH):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Tenant OIDC discovery disabled",
        )
    if not await _tenant_exists(db=db, tenant_slug=tenant_slug):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")
    return build_tenant_openid_config(deployment, tenant_slug)


async def realm_openid_configuration(
    request: object,
    realm_slug: str,
    db: object | None,
) -> dict[str, Any]:
    deployment = deployment_from_request(request, settings)
    if not deployment.route_enabled(REALM_OPENID_CONFIGURATION_PATH):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Realm OIDC discovery disabled",
        )
    if not await _realm_exists(db=db, realm_slug=realm_slug):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Realm not found")
    return build_realm_openid_config(deployment, realm_slug)


async def jwks(request: object) -> dict[str, object]:
    deployment = deployment_from_request(request, settings)
    if not deployment.route_enabled(JWKS_PATH):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "JWKS publication disabled")
    return await build_jwks_document()


async def tenant_jwks(
    request: object,
    tenant_slug: str,
    db: object | None,
) -> dict[str, object]:
    deployment = deployment_from_request(request, settings)
    if not deployment.route_enabled(TENANT_JWKS_PATH):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Tenant JWKS publication disabled",
        )
    if not await _tenant_exists(db=db, tenant_slug=tenant_slug):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")
    return await asyncio.to_thread(
        build_operator_jwks_payload,
        Path.cwd(),
        tenant=tenant_slug,
    )


async def realm_jwks(
    request: object,
    realm_slug: str,
    db: object | None,
) -> dict[str, object]:
    deployment = deployment_from_request(request, settings)
    if not deployment.route_enabled(REALM_JWKS_PATH):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Realm JWKS publication disabled",
        )
    if not await _realm_exists(db=db, realm_slug=realm_slug):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Realm not found")
    return await asyncio.to_thread(
        build_operator_jwks_payload,
        Path.cwd(),
        tenant=realm_slug,
    )


__all__ = [
    "ISSUER",
    "JWKS_PATH",
    "_build_openid_config",
    "_cached_openid_config",
    "_settings_signature",
    "jwks",
    "openid_configuration",
    "realm_jwks",
    "realm_openid_configuration",
    "refresh_discovery_cache",
    "tenant_jwks",
    "tenant_openid_configuration",
]
