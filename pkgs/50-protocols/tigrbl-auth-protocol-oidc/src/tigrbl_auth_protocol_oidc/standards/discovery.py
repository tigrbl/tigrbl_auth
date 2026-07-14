"""Pure OIDC Discovery 1.0 metadata ownership and cached projections."""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any, Final

from tigrbl_auth_protocol_oauth.standards.authorization_server_metadata import (
    ISSUER,
    JWKS_PATH,
)
from tigrbl_identity_contracts.protocol_configuration import (
    protocol_settings as settings,
)
from tigrbl_identity_core.standards import StandardOwner, describe_owner
from tigrbl_identity_runtime.deployment import ResolvedDeployment, resolve_deployment

from .discovery_metadata import build_openid_config


OIDC_DISCOVERY_SPEC_URL: Final[str] = (
    "https://openid.net/specs/openid-connect-discovery-1_0.html"
)
OWNER = StandardOwner(
    label="OIDC Discovery 1.0",
    title="OpenID Connect Discovery 1.0",
    runtime_status="profile-aware-discovery-metadata",
    public_surface=("/.well-known/openid-configuration",),
    notes=(
        "Versioned metadata semantics only; HTTP publication and durable "
        "tenant/realm existence checks are composed above the protocol layer."
    ),
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


def describe() -> dict[str, object]:
    return describe_owner(
        OWNER,
        specification_version="1.0",
        jwks_publication=True,
        tenant_and_realm_profiles=True,
        spec_url=OIDC_DISCOVERY_SPEC_URL,
    )


__all__ = [
    "ISSUER",
    "JWKS_PATH",
    "OIDC_DISCOVERY_SPEC_URL",
    "OWNER",
    "_build_openid_config",
    "_cached_openid_config",
    "_settings_signature",
    "describe",
    "refresh_discovery_cache",
]
