from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from pydantic.version import VERSION as PYDANTIC_VERSION

from tigrbl_identity_runtime.deployment import ROUTE_REGISTRY, resolve_deployment
from tigrbl_identity_runtime.profile_loader import load_profile_reference
from tigrbl_identity_server.security.admin_gate import ADMIN_SECURITY_REQUIREMENT, ADMIN_SECURITY_SCHEMES
from tigrbl_identity_runtime.http_standards.well_known import WELL_KNOWN_ENDPOINTS
from tigrbl_auth_protocol_oidc.tenant_discovery import (
    REALM_JWKS_PATH,
    REALM_OPENID_CONFIGURATION_PATH,
    TENANT_JWKS_PATH,
    TENANT_OPENID_CONFIGURATION_PATH,
    build_tenant_openid_config,
    resolve_tenant_trust_domain_authority,
)
from tigrbl_auth_protocol_oidc.standards.discovery_metadata import build_openid_config
from tigrbl_auth_protocol_oauth.standards.assertion_framework import build_assertion_contract_examples
from tigrbl_auth_protocol_oauth.standards.jwt_client_auth import build_client_assertion_contract_examples
from tigrbl_auth_protocol_oauth.standards.authorization_server_metadata import JWKS_PATH
from tigrbl_auth_protocol_oauth.standards.oauth_security_bcp import runtime_security_profile


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _write_yaml(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def _current_version(repo_root: Path) -> str:
    pyproject = repo_root / "pyproject.toml"
    if not pyproject.exists():
        return "0.0.0-checkpoint"
    for line in pyproject.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("version") and "=" in line:
            return line.split("=", 1)[1].strip().strip('"')
    return "0.0.0-checkpoint"


def deployment_from_options(
    *,
    settings_obj: object | None = None,
    profile: str | None = None,
    surface_sets: list[str] | tuple[str, ...] | None = None,
    protocol_slices: list[str] | tuple[str, ...] | None = None,
    extensions: list[str] | tuple[str, ...] | None = None,
    plugin_mode: str | None = None,
    runtime_style: str | None = None,
    issuer: str | None = None,
    strict: bool | None = None,
) -> Any:
    overrides: dict[str, Any] = {}
    if issuer:
        overrides["issuer"] = issuer
    if strict is not None:
        overrides["strict_boundary_enforcement"] = strict
    profile_defaults = load_profile_reference(profile)
    if settings_obj is None:
        from tigrbl_identity_runtime.settings import settings as active_settings

        settings_obj = active_settings
    profile_surface_sets = profile_defaults.surface_sets if profile_defaults else ()
    if surface_sets is None and plugin_mode is not None and plugin_mode != profile_defaults.surface_plugin_mode:
        profile_surface_sets = ()
    return resolve_deployment(
        settings_obj,
        profile=profile_defaults.base_profile,
        surface_sets=tuple(surface_sets or profile_surface_sets),
        protocol_slices=tuple(protocol_slices or (profile_defaults.protocol_slices if profile_defaults else ())),
        extensions=tuple(extensions or (profile_defaults.extensions if profile_defaults else ())),
        plugin_mode=plugin_mode or (profile_defaults.surface_plugin_mode if profile_defaults else None),
        runtime_style=runtime_style,
        flag_overrides={**profile_defaults.flag_overrides(), **overrides},
        profile_source=profile_defaults.provenance(),
    )


def _json_content(schema_ref: str) -> dict[str, Any]:
    return {"application/json": {"schema": {"$ref": schema_ref}}}


def _form_content(required_fields: list[str], properties: dict[str, Any]) -> dict[str, Any]:
    return {
        "application/x-www-form-urlencoded": {
            "schema": {"type": "object", "required": required_fields, "properties": properties}
        }
    }


def _schema_components() -> dict[str, Any]:
    return {
        "Error": {
            "type": "object",
            "required": ["error"],
            "properties": {
                "error": {"type": "string"},
                "error_description": {"type": "string"},
                "error_uri": {"type": "string", "format": "uri"},
            },
        },
        "AuthorizationResponse": {
            "type": "object",
            "properties": {
                "code": {"type": "string"},
                "state": {"type": "string"},
                "iss": {"type": "string", "format": "uri"},
                "session_state": {"type": "string"},
            },
        },
        "TokenResponse": {
            "type": "object",
            "required": ["access_token", "token_type"],
            "properties": {
                "access_token": {"type": "string"},
                "token_type": {"type": "string", "description": "Bearer for unconstrained or mTLS-bound tokens; DPoP for proof-of-possession tokens."},
                "expires_in": {"type": "integer"},
                "refresh_token": {"type": "string"},
                "id_token": {"type": "string"},
                "scope": {"type": "string"},
            },
        },
        "IntrospectionResponse": {
            "type": "object",
            "required": ["active"],
            "properties": {
                "active": {"type": "boolean"},
                "scope": {"type": "string"},
                "client_id": {"type": "string"},
                "sub": {"type": "string"},
                "iss": {"type": "string", "format": "uri"},
                "exp": {"type": "integer"},
            },
        },
        "UserInfoResponse": {
            "type": "object",
            "required": ["sub"],
            "properties": {
                "sub": {"type": "string"},
                "name": {"type": "string"},
                "email": {"type": "string", "format": "email"},
                "preferred_username": {"type": "string"},
            },
        },
        "JwksDocument": {
            "type": "object",
            "required": ["keys"],
            "properties": {
                "keys": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "kid": {"type": "string"},
                            "kty": {"type": "string"},
                            "alg": {"type": "string"},
                            "use": {"type": "string"},
                        },
                    },
                }
            },
        },
        "DiscoveryDocument": {"type": "object", "additionalProperties": True},
        "AuthorizationServerMetadata": {"type": "object", "additionalProperties": True},
        "ProtectedResourceMetadata": {"type": "object", "additionalProperties": True},
        "RevocationResponse": {"type": "object", "properties": {"revoked": {"type": "boolean"}}},
        "DynamicClientRegistrationResponse": {
            "type": "object",
            "required": ["client_id", "redirect_uris", "grant_types", "response_types", "token_endpoint_auth_method"],
            "properties": {
                "client_id": {"type": "string"},
                "client_secret": {"type": "string"},
                "client_id_issued_at": {"type": "integer"},
                "client_secret_expires_at": {"type": "integer"},
                "redirect_uris": {"type": "array", "items": {"type": "string", "format": "uri"}},
                "grant_types": {"type": "array", "items": {"type": "string"}},
                "response_types": {"type": "array", "items": {"type": "string"}},
                "token_endpoint_auth_method": {"type": "string"},
                "tls_client_certificate_thumbprint": {"type": "string"},
                "self_signed_tls_client_certificate_thumbprint": {"type": "string"},
                "tls_client_auth_subject_dn": {"type": "string"},
                "tls_client_auth_san_dns": {"type": "string"},
                "tls_client_auth_san_uri": {"type": "string"},
                "tls_client_auth_san_ip": {"type": "string"},
                "tls_client_auth_san_email": {"type": "string"},
                "post_logout_redirect_uris": {"type": "array", "items": {"type": "string", "format": "uri"}},
                "frontchannel_logout_uri": {"type": "string", "format": "uri"},
                "frontchannel_logout_session_required": {"type": "boolean"},
                "backchannel_logout_uri": {"type": "string", "format": "uri"},
                "backchannel_logout_session_required": {"type": "boolean"},
                "registration_access_token": {"type": "string"},
                "registration_client_uri": {"type": "string", "format": "uri"},
            },
        },
        "RegistrationManagementDeleteResponse": {
            "type": "object",
            "required": ["status", "client_id"],
            "properties": {
                "status": {"type": "string"},
                "client_id": {"type": "string"},
            },
        },
        "LogoutResponse": {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "session_id": {"type": "string"},
                "logout_id": {"type": "string"},
                "post_logout_redirect_uri": {"type": "string", "format": "uri"},
                "state": {"type": "string"},
                "cookie_cleared": {"type": "boolean"},
                "cookie_policy": {"type": "object", "additionalProperties": True},
                "frontchannel_logout": {"type": "object", "additionalProperties": True},
                "backchannel_logout": {"type": "object", "additionalProperties": True},
                "frontchannel_delivery": {"type": "object", "additionalProperties": True},
                "backchannel_delivery": {"type": "object", "additionalProperties": True},
                "replay_protected": {"type": "boolean"},
            },
        },
        "DeviceAuthorizationResponse": {
            "type": "object",
            "required": ["device_code", "user_code", "verification_uri", "verification_uri_complete", "expires_in", "interval"],
            "properties": {
                "device_code": {"type": "string"},
                "user_code": {"type": "string"},
                "verification_uri": {"type": "string", "format": "uri"},
                "verification_uri_complete": {"type": "string", "format": "uri"},
                "expires_in": {"type": "integer"},
                "interval": {"type": "integer"},
            },
        },
        "PushedAuthorizationResponse": {
            "type": "object",
            "required": ["request_uri", "expires_in"],
            "properties": {
                "request_uri": {"type": "string"},
                "expires_in": {"type": "integer"},
            },
        },
        "GenericResult": {"type": "object", "additionalProperties": True},
    }
