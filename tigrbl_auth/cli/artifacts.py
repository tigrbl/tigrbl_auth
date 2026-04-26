from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from pydantic.version import VERSION as PYDANTIC_VERSION

from tigrbl_auth.api.rpc import iter_active_rpc_methods
from tigrbl_auth.config.deployment import ROUTE_REGISTRY, resolve_deployment
from tigrbl_auth.security.admin_gate import ADMIN_SECURITY_REQUIREMENT, ADMIN_SECURITY_SCHEMES
from tigrbl_auth.standards.http.well_known import WELL_KNOWN_ENDPOINTS
from tigrbl_auth.standards.oidc.discovery_metadata import build_openid_config
from tigrbl_auth.standards.oauth2.assertion_framework import build_assertion_contract_examples
from tigrbl_auth.standards.oauth2.jwt_client_auth import build_client_assertion_contract_examples
from tigrbl_auth.standards.oauth2.rfc8414_metadata import JWKS_PATH
from tigrbl_auth.standards.oauth2.rfc9700 import runtime_security_profile


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
    return resolve_deployment(
        None,
        profile=profile,
        surface_sets=tuple(surface_sets or ()),
        protocol_slices=tuple(protocol_slices or ()),
        extensions=tuple(extensions or ()),
        plugin_mode=plugin_mode,
        runtime_style=runtime_style,
        flag_overrides=overrides,
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


def _openapi_operation(path: str, method: str, meta: dict[str, Any], deployment: Any) -> dict[str, Any]:
    policy = runtime_security_profile(deployment)
    op: dict[str, Any] = {
        "operationId": f"{method}_{path.strip('/').replace('/', '_').replace('.', '_').replace('-', '_') or 'root'}",
        "summary": meta.get("summary", path),
        "tags": list(meta.get("tags", [])),
        "responses": {"200": {"description": "Success", "content": _json_content("#/components/schemas/GenericResult")}},
        "x-required-flags": list(meta.get("flags", [])),
        "x-runtime-profile": {
            "profile": deployment.profile,
            "allowed_grant_types": list(policy.allowed_grant_types),
            "allowed_response_types": list(policy.allowed_response_types),
            "par_required": policy.par_required,
            "sender_constraint_required": policy.sender_constraint_required,
            "dpop_supported": policy.dpop_supported,
            "mtls_supported": policy.mtls_supported,
            "resource_indicators_supported": policy.resource_indicators_supported,
            "request_objects_supported": policy.request_objects_supported,
            "rich_authorization_requests_supported": policy.rich_authorization_requests_supported,
            "query_bearer_disabled": policy.query_bearer_disabled,
            "form_bearer_disabled": policy.form_bearer_disabled,
            "jwt_access_token_profile_supported": deployment.flag_enabled("enable_rfc9068"),
        },
    }
    if path == "/authorize":
        op["parameters"] = [
            {"name": "response_type", "in": "query", "required": True, "schema": {"type": "string", "enum": list(policy.allowed_response_types)}},
            {"name": "client_id", "in": "query", "required": True, "schema": {"type": "string"}},
            {"name": "redirect_uri", "in": "query", "required": True, "schema": {"type": "string", "format": "uri"}},
            {"name": "scope", "in": "query", "required": False, "schema": {"type": "string"}},
            {"name": "response_mode", "in": "query", "required": False, "schema": {"type": "string", "enum": list(policy.allowed_response_modes)}},
            {"name": "state", "in": "query", "required": False, "schema": {"type": "string"}},
            {"name": "nonce", "in": "query", "required": False, "schema": {"type": "string"}},
            {"name": "request", "in": "query", "required": False, "schema": {"type": "string"}},
            {"name": "code_challenge", "in": "query", "required": policy.pkce_required_for_all_clients, "schema": {"type": "string"}},
            {"name": "code_challenge_method", "in": "query", "required": False, "schema": {"type": "string", "enum": ["S256"]}},
            {"name": "request_uri", "in": "query", "required": policy.par_required, "schema": {"type": "string"}},
            {"name": "authorization_details", "in": "query", "required": False, "schema": {"type": "string"}},
            {"name": "resource", "in": "query", "required": False, "schema": {"type": "string", "format": "uri"}},
        ]
        authz_schema: dict[str, Any] = {"$ref": "#/components/schemas/AuthorizationResponse"}
        if deployment.flag_enabled("enable_rfc9207"):
            authz_schema = {"allOf": [{"$ref": "#/components/schemas/AuthorizationResponse"}, {"type": "object", "required": ["iss"]}]}
        op["responses"]["200"]["content"] = {"application/json": {"schema": authz_schema}}
    elif path == "/token":
        grant_types = list(policy.allowed_grant_types)
        properties = {
            "grant_type": {"type": "string", "enum": grant_types},
            "code": {"type": "string"},
            "device_code": {"type": "string"},
            "redirect_uri": {"type": "string", "format": "uri"},
            "client_id": {"type": "string"},
            "client_secret": {"type": "string"},
            "client_assertion": {"type": "string"},
            "client_assertion_type": {"type": "string"},
            "assertion": {"type": "string"},
            "code_verifier": {"type": "string"},
            "refresh_token": {"type": "string"},
            "username": {"type": "string"},
            "password": {"type": "string"},
            "scope": {"type": "string"},
            "audience": {"type": "string", "format": "uri"},
            "resource": {"type": "string", "format": "uri"},
        }
        token_examples: dict[str, Any] = {}
        token_endpoint_audience = f"{deployment.issuer}/token"
        assertion_examples = build_assertion_contract_examples(token_endpoint_audience)
        if assertion_examples:
            token_examples["jwt_bearer_grant"] = {
                "summary": "RFC 7521 JWT bearer assertion grant",
                "value": assertion_examples[0],
            }
        client_assertion_examples = build_client_assertion_contract_examples(token_endpoint_audience)
        if client_assertion_examples:
            token_examples["jwt_client_auth"] = {
                "summary": "RFC 7523 private_key_jwt token endpoint authentication",
                "value": client_assertion_examples[0],
            }
        form_content = _form_content(["grant_type"], properties)
        if token_examples:
            form_content["application/x-www-form-urlencoded"]["examples"] = token_examples
        op["requestBody"] = {"required": True, "content": form_content}
        op["responses"]["200"]["content"] = _json_content("#/components/schemas/TokenResponse")
        parameters: list[dict[str, Any]] = []
        if policy.dpop_supported:
            parameters.append({"name": "DPoP", "in": "header", "required": policy.sender_constraint_required, "schema": {"type": "string"}})
        if policy.mtls_supported:
            parameters.append({"name": "X-Client-Cert-SHA256", "in": "header", "required": False, "schema": {"type": "string"}})
        if parameters:
            op["parameters"] = parameters
    elif path == "/userinfo":
        op["security"] = [{"bearerAuth": []}]
        op["responses"]["200"]["content"] = _json_content("#/components/schemas/UserInfoResponse")
    elif path == "/introspect":
        op["requestBody"] = {"required": True, "content": _form_content(["token"], {"token": {"type": "string"}, "token_type_hint": {"type": "string"}})}
        op["responses"]["200"]["content"] = _json_content("#/components/schemas/IntrospectionResponse")
    elif path == "/register":
        op["requestBody"] = {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "required": ["redirect_uris"],
                        "properties": {
                            "tenant_slug": {"type": "string"},
                            "redirect_uris": {"type": "array", "items": {"type": "string", "format": "uri"}},
                            "grant_types": {"type": "array", "items": {"type": "string"}},
                            "response_types": {"type": "array", "items": {"type": "string"}},
                            "token_endpoint_auth_method": {"type": "string"},
                            "tls_client_certificate_thumbprint": {"type": "string"},
                            "self_signed_tls_client_certificate_thumbprint": {"type": "string"},
                            "scope": {"type": "string"},
                            "client_name": {"type": "string"},
                            "client_uri": {"type": "string", "format": "uri"},
                            "jwks_uri": {"type": "string", "format": "uri"},
                            "contacts": {"type": "array", "items": {"type": "string", "format": "email"}},
                            "software_id": {"type": "string"},
                            "software_version": {"type": "string"},
                            "post_logout_redirect_uris": {"type": "array", "items": {"type": "string", "format": "uri"}},
                            "frontchannel_logout_uri": {"type": "string", "format": "uri"},
                            "frontchannel_logout_session_required": {"type": "boolean"},
                            "backchannel_logout_uri": {"type": "string", "format": "uri"},
                            "backchannel_logout_session_required": {"type": "boolean"},
                        },
                    }
                }
            },
        }
        op["responses"]["200"]["content"] = _json_content("#/components/schemas/DynamicClientRegistrationResponse")
    elif path == "/register/{client_id}":
        op["parameters"] = [
            {"name": "client_id", "in": "path", "required": True, "schema": {"type": "string"}},
            {"name": "Authorization", "in": "header", "required": True, "schema": {"type": "string"}},
        ]
        if method.lower() == "put":
            op["requestBody"] = {
                "required": False,
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "tenant_slug": {"type": "string"},
                                "redirect_uris": {"type": "array", "items": {"type": "string", "format": "uri"}},
                                "grant_types": {"type": "array", "items": {"type": "string"}},
                                "response_types": {"type": "array", "items": {"type": "string"}},
                                "token_endpoint_auth_method": {"type": "string"},
                                "tls_client_certificate_thumbprint": {"type": "string"},
                                "self_signed_tls_client_certificate_thumbprint": {"type": "string"},
                                "scope": {"type": "string"},
                                "client_name": {"type": "string"},
                                "client_uri": {"type": "string", "format": "uri"},
                                "jwks_uri": {"type": "string", "format": "uri"},
                                "contacts": {"type": "array", "items": {"type": "string", "format": "email"}},
                                "software_id": {"type": "string"},
                                "software_version": {"type": "string"},
                                "post_logout_redirect_uris": {"type": "array", "items": {"type": "string", "format": "uri"}},
                                "frontchannel_logout_uri": {"type": "string", "format": "uri"},
                                "frontchannel_logout_session_required": {"type": "boolean"},
                                "backchannel_logout_uri": {"type": "string", "format": "uri"},
                                "backchannel_logout_session_required": {"type": "boolean"},
                            },
                        }
                    }
                },
            }
            op["responses"]["200"]["content"] = _json_content("#/components/schemas/DynamicClientRegistrationResponse")
        elif method.lower() == "delete":
            op["responses"]["200"]["content"] = _json_content("#/components/schemas/RegistrationManagementDeleteResponse")
        else:
            op["responses"]["200"]["content"] = _json_content("#/components/schemas/DynamicClientRegistrationResponse")
    elif path == "/revoke":
        op["requestBody"] = {"required": True, "content": _form_content(["token"], {"token": {"type": "string"}, "token_type_hint": {"type": "string"}})}
        op["responses"]["200"]["content"] = _json_content("#/components/schemas/RevocationResponse")
    elif path == "/logout":
        op["responses"]["200"]["content"] = _json_content("#/components/schemas/LogoutResponse")
        if method.lower() == "get":
            op["parameters"] = [
                {"name": "id_token_hint", "in": "query", "required": False, "schema": {"type": "string"}},
                {"name": "post_logout_redirect_uri", "in": "query", "required": False, "schema": {"type": "string", "format": "uri"}},
                {"name": "state", "in": "query", "required": False, "schema": {"type": "string"}},
                {"name": "sid", "in": "query", "required": False, "schema": {"type": "string"}},
                {"name": "client_id", "in": "query", "required": False, "schema": {"type": "string"}},
            ]
        else:
            op["requestBody"] = {
                "required": False,
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "id_token_hint": {"type": "string"},
                                "post_logout_redirect_uri": {"type": "string", "format": "uri"},
                                "state": {"type": "string"},
                                "sid": {"type": "string"},
                                "client_id": {"type": "string"},
                            },
                        }
                    },
                    **_form_content([], {
                        "id_token_hint": {"type": "string"},
                        "post_logout_redirect_uri": {"type": "string", "format": "uri"},
                        "state": {"type": "string"},
                        "sid": {"type": "string"},
                        "client_id": {"type": "string"},
                    }),
                },
            }
    elif path == "/device_authorization":
        op["requestBody"] = {"required": True, "content": _form_content(["client_id"], {"client_id": {"type": "string"}, "scope": {"type": "string"}, "audience": {"type": "string"}, "resource": {"type": "array", "items": {"type": "string", "format": "uri"}}})}
        op["responses"]["200"]["content"] = _json_content("#/components/schemas/DeviceAuthorizationResponse")
    elif path == "/par":
        op["requestBody"] = {"required": True, "content": _form_content(["client_id"], {"client_id": {"type": "string"}, "request": {"type": "string"}, "response_type": {"type": "string", "enum": list(policy.allowed_response_types)}, "redirect_uri": {"type": "string", "format": "uri"}, "scope": {"type": "string"}, "state": {"type": "string"}, "nonce": {"type": "string"}, "code_challenge": {"type": "string"}, "code_challenge_method": {"type": "string"}, "resource": {"type": "array", "items": {"type": "string", "format": "uri"}}, "authorization_details": {"type": "string"}})}
        op["responses"]["200"]["content"] = _json_content("#/components/schemas/PushedAuthorizationResponse")
    elif path == "/token/exchange":
        op["requestBody"] = {"required": True, "content": _form_content(["grant_type", "subject_token", "subject_token_type"], {"grant_type": {"type": "string"}, "subject_token": {"type": "string"}, "subject_token_type": {"type": "string"}, "requested_token_type": {"type": "string"}, "audience": {"type": "string"}, "resource": {"type": "array", "items": {"type": "string", "format": "uri"}}})}
        op["responses"]["200"]["content"] = _json_content("#/components/schemas/TokenResponse")
        parameters = []
        if policy.dpop_supported:
            parameters.append({"name": "DPoP", "in": "header", "required": policy.sender_constraint_required, "schema": {"type": "string"}})
        if policy.mtls_supported:
            parameters.append({"name": "X-Client-Cert-SHA256", "in": "header", "required": False, "schema": {"type": "string"}})
        if parameters:
            op["parameters"] = parameters
    elif path == "/.well-known/openid-configuration":
        op["responses"]["200"]["content"] = _json_content("#/components/schemas/DiscoveryDocument")
    elif path == "/.well-known/oauth-authorization-server":
        op["responses"]["200"]["content"] = _json_content("#/components/schemas/AuthorizationServerMetadata")
    elif path == "/.well-known/oauth-protected-resource":
        op["responses"]["200"]["content"] = _json_content("#/components/schemas/ProtectedResourceMetadata")
    elif path == "/.well-known/jwks.json":
        op["responses"]["200"]["content"] = _json_content("#/components/schemas/JwksDocument")
    return op


def build_openapi_contract(deployment: Any, *, version: str) -> dict[str, Any]:
    public_paths: dict[str, Any] = {}
    for path in deployment.active_routes:
        meta = ROUTE_REGISTRY.get(path, {})
        if meta.get("surface_set") != "public-rest":
            continue
        operations: dict[str, Any] = {}
        for method in meta.get("methods", ()):  # type: ignore[union-attr]
            operations[str(method)] = _openapi_operation(path, str(method), meta, deployment)
        public_paths[path] = operations

    security_schemes: dict[str, Any] = {}
    if deployment.flag_enabled("enable_rfc6750"):
        security_schemes["bearerAuth"] = {"type": "http", "scheme": "bearer"}
    if deployment.flag_enabled("enable_rfc6749"):
        security_schemes["oauth2"] = {
            "type": "oauth2",
            "flows": {
                "authorizationCode": {
                    "authorizationUrl": f"{deployment.issuer}/authorize",
                    "tokenUrl": f"{deployment.issuer}/token",
                    "scopes": {"openid": "OpenID Connect scope", "profile": "Profile claims"},
                }
            },
        }
    if deployment.flag_enabled("enable_oidc_discovery"):
        security_schemes["openIdConnect"] = {"type": "openIdConnect", "openIdConnectUrl": f"{deployment.issuer}/.well-known/openid-configuration"}

    return {
        "openapi": "3.1.0",
        "info": {
            "title": "tigrbl_auth public auth server",
            "version": version,
            "description": "Generated public contract filtered by the effective deployment boundary.",
        },
        "servers": [{"url": deployment.issuer}],
        "paths": public_paths,
        "components": {"securitySchemes": security_schemes, "schemas": _schema_components()},
        "x-tigrbl-auth": {
            "profile": deployment.profile,
            "plugin_mode": deployment.plugin_mode,
            "runtime_style": deployment.runtime_style,
            "surface_sets": list(deployment.surface_sets),
            "protocol_slices": list(deployment.protocol_slices),
            "extensions": list(deployment.extensions),
            "active_targets": list(deployment.active_targets),
            "strict_boundary_enforcement": deployment.strict_boundary_enforcement,
        },
    }


def write_openapi_contract(repo_root: Path, deployment: Any, *, profile_label: str = "active") -> Path:
    version = _current_version(repo_root)
    contract = build_openapi_contract(deployment, version=version)
    if profile_label == "active":
        json_path = repo_root / "specs" / "openapi" / "tigrbl_auth.public.openapi.json"
        yaml_path = repo_root / "specs" / "openapi" / "tigrbl_auth.public.openapi.yaml"
    else:
        json_path = repo_root / "specs" / "openapi" / "profiles" / profile_label / "tigrbl_auth.public.openapi.json"
        yaml_path = repo_root / "specs" / "openapi" / "profiles" / profile_label / "tigrbl_auth.public.openapi.yaml"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")
    yaml_path.write_text(yaml.safe_dump(contract, sort_keys=False), encoding="utf-8")
    if profile_label == "active":
        summary = repo_root / "docs" / "compliance" / "openapi_contract_summary.md"
        lines = [
            "# OpenAPI Contract Summary",
            "",
            f"- Title: `{contract['info']['title']}`",
            f"- Version: `{contract['info']['version']}`",
            f"- Profile: `{deployment.profile}`",
            f"- Surface sets: `{', '.join(deployment.surface_sets) or 'none'}`",
            f"- Path count: `{len(contract['paths'])}`",
            f"- Schema count: `{len(contract['components']['schemas'])}`",
            "",
            "## Paths",
            "",
        ]
        for path, item in contract["paths"].items():
            lines.append(f"- `{path}` → `{', '.join(sorted(item.keys()))}`")
        summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path


def _rewrite_openrpc_refs(payload: Any) -> Any:
    if isinstance(payload, dict):
        rewritten = {}
        for key, value in payload.items():
            if key == "$ref" and isinstance(value, str) and value.startswith("#/$defs/"):
                rewritten[key] = value.replace("#/$defs/", "#/components/schemas/")
            else:
                rewritten[key] = _rewrite_openrpc_refs(value)
        return rewritten
    if isinstance(payload, list):
        return [_rewrite_openrpc_refs(item) for item in payload]
    return payload


def _merge_openrpc_defs(schema: dict[str, Any], components: dict[str, Any]) -> dict[str, Any]:
    pending = list((schema.pop("$defs", {}) or {}).items())
    while pending:
        name, item = pending.pop(0)
        item = _rewrite_openrpc_refs(dict(item))
        nested = item.pop("$defs", {}) or {}
        pending.extend(list(nested.items()))
        components.setdefault(name, item)
    return _rewrite_openrpc_refs(schema)


def _collect_model_schema(model: Any, components: dict[str, Any]) -> dict[str, Any]:
    name = getattr(model, "__name__", str(model))
    if name not in components:
        if hasattr(model, "model_json_schema"):
            schema = model.model_json_schema(ref_template="#/components/schemas/{model}")
        elif hasattr(model, "schema"):
            schema = model.schema(ref_template="#/components/schemas/{model}")
        else:
            schema = {"title": name, "type": "object", "additionalProperties": True}
        components[name] = _merge_openrpc_defs(schema, components)
    return {"$ref": f"#/components/schemas/{name}"}


def _openrpc_params_from_model(model: Any, components: dict[str, Any]) -> list[dict[str, Any]]:
    model_fields = getattr(model, "model_fields", None)
    if not model_fields and PYDANTIC_VERSION.startswith("1."):
        model_fields = getattr(model, "__fields__", None)
    if not model_fields:
        return []
    schema_ref = _collect_model_schema(model, components)
    model_name = schema_ref["$ref"].split("/")[-1]
    model_schema = components.get(model_name, {})
    properties = dict(model_schema.get("properties", {}))
    required = set(model_schema.get("required", []))
    return [
        {"name": field_name, "required": field_name in required, "schema": properties.get(field_name, {"type": "string"})}
        for field_name in properties
    ]


def build_openrpc_contract(deployment: Any, *, version: str) -> dict[str, Any]:
    methods: list[dict[str, Any]] = []
    components: dict[str, Any] = {}
    if deployment.surface_enabled("admin-rpc"):
        for definition in iter_active_rpc_methods(deployment):
            methods.append(
                {
                    "name": definition.name,
                    "summary": definition.summary,
                    "description": definition.description,
                    "tags": list(definition.tags),
                    "paramStructure": "by-name",
                    "params": _openrpc_params_from_model(definition.params_model, components),
                    "result": {
                        "name": "result",
                        "schema": _collect_model_schema(definition.result_model, components),
                    },
                    "security": ADMIN_SECURITY_REQUIREMENT,
                    "x-tigrbl-auth": {
                        "owner_module": definition.owner_module,
                        "required_flags": list(definition.required_flags),
                        "surface_set": definition.surface_set,
                        "since_phase": definition.since_phase,
                    },
                }
            )
    contract = {
        "openrpc": "1.4.2",
        "info": {
            "title": "tigrbl_auth admin/control-plane",
            "version": version,
            "description": "Generated admin/control-plane contract derived from implementation-backed RPC registration and filtered by the effective deployment boundary.",
        },
        "servers": [{"name": "admin-rpc", "url": f"{deployment.issuer}/rpc"}],
        "methods": methods,
        "x-tigrbl-auth": {
            "profile": deployment.profile,
            "plugin_mode": deployment.plugin_mode,
            "runtime_style": deployment.runtime_style,
            "surface_sets": list(deployment.surface_sets),
            "strict_boundary_enforcement": deployment.strict_boundary_enforcement,
            "generation_mode": "implementation-backed-rpc-registry",
        },
    }
    contract_components: dict[str, Any] = {}
    if components:
        contract_components["schemas"] = components
    if deployment.surface_enabled("admin-rpc"):
        contract_components["securitySchemes"] = ADMIN_SECURITY_SCHEMES
    if contract_components:
        contract["components"] = contract_components
    return contract


def write_openrpc_contract(repo_root: Path, deployment: Any, *, profile_label: str = "active") -> Path:
    version = _current_version(repo_root)
    contract = build_openrpc_contract(deployment, version=version)
    if profile_label == "active":
        path = repo_root / "specs" / "openrpc" / "tigrbl_auth.admin.openrpc.json"
    else:
        path = repo_root / "specs" / "openrpc" / "profiles" / profile_label / "tigrbl_auth.admin.openrpc.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")
    if profile_label == "active":
        summary = repo_root / "docs" / "compliance" / "openrpc_contract_summary.md"
        lines = [
            "# OpenRPC Contract Summary",
            "",
            f"- Title: `{contract['info']['title']}`",
            f"- Version: `{contract['info']['version']}`",
            f"- Profile: `{deployment.profile}`",
            f"- Method count: `{len(contract['methods'])}`",
            f"- Schema count: `{len(contract.get('components', {}).get('schemas', {}))}`",
            "",
            "## Methods",
            "",
        ]
        for method in contract["methods"]:
            owner = method.get("x-tigrbl-auth", {}).get("owner_module", "unknown")
            lines.append(f"- `{method['name']}` — {method['summary']} (`{owner}`)")
        summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def build_jwks_snapshot(deployment: Any, *, profile_label: str = "active") -> dict[str, Any]:
    return {
        "keys": [],
        "profile": deployment.profile,
        "profile_label": profile_label,
        "issuer": deployment.issuer,
        "generated_from": "tigrbl_auth.cli.artifacts.write_discovery_artifacts",
    }


def build_protected_resource_metadata_snapshot(deployment: Any) -> dict[str, Any]:
    methods = ["header"]
    if bool(deployment.flags.get("enable_rfc6750_form", False)):
        methods.append("body")
    if bool(deployment.flags.get("enable_rfc6750_query", False)):
        methods.append("query")
    return {
        "resource": deployment.protected_resource_identifier,
        "authorization_servers": [deployment.issuer],
        "jwks_uri": f"{deployment.issuer}{JWKS_PATH}",
        "bearer_methods_supported": methods,
        "resource_documentation": f"{deployment.issuer}/docs/resource-metadata",
        "scopes_supported": ["openid", "profile", "email"],
        "active_targets": list(deployment.active_targets),
    }


def build_discovery_artifacts(deployment: Any, *, profile_label: str = "active") -> dict[str, dict[str, Any]]:
    artifacts = {
        "openid-configuration.json": build_openid_config(deployment),
        "oauth-authorization-server.json": build_openid_config(deployment),
        "jwks.json": build_jwks_snapshot(deployment, profile_label=profile_label),
    }
    protected_resource_path = WELL_KNOWN_ENDPOINTS["oauth_protected_resource"]
    if deployment.discovery_route_enabled(protected_resource_path):
        artifacts["oauth-protected-resource.json"] = build_protected_resource_metadata_snapshot(deployment)
    return artifacts


def write_discovery_artifacts(repo_root: Path, deployment: Any, *, profile_label: str = "active") -> dict[str, Path]:
    profile_dir = repo_root / "specs" / "discovery" / "profiles" / profile_label
    profile_dir.mkdir(parents=True, exist_ok=True)
    artifacts = build_discovery_artifacts(deployment, profile_label=profile_label)
    written: dict[str, Path] = {}
    for filename, payload in artifacts.items():
        path = profile_dir / filename
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        written[filename] = path
    protected_path = profile_dir / "oauth-protected-resource.json"
    if "oauth-protected-resource.json" not in artifacts and protected_path.exists():
        protected_path.unlink()
    return written


def build_effective_claims_manifest(repo_root: Path, deployment: Any, *, profile_label: str = "active") -> dict[str, Any]:
    declared = _load_yaml(repo_root / "compliance" / "claims" / "declared-target-claims.yaml")
    claim_set = declared.get("claim_set", {})
    profile_order = {"baseline": 0, "production": 1, "hardening": 2, "fapi2-security": 3, "peer-claim": 4}
    current_rank = profile_order.get(deployment.profile, 0)
    claims = []
    boundary_exclusions = {"OpenRPC 1.4.x admin/control-plane contract", "RFC 9728"} if profile_label == "active" else set()
    for claim in claim_set.get("claims", []):
        target = str(claim.get("target"))
        if target in boundary_exclusions:
            continue
        claim_profile = str(claim.get("profile", "baseline"))
        if target not in deployment.active_targets:
            continue
        if profile_order.get(claim_profile, 99) > current_rank:
            continue
        claims.append(claim)
    return {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "profile_label": profile_label,
        "effective_deployment": deployment.to_manifest(),
        "claim_set": {
            "current_repository_tier": claim_set.get("current_repository_tier", 0),
            "phase": claim_set.get("phase", "P3"),
            "claims": claims,
        },
    }


def write_effective_claims_manifest(repo_root: Path, deployment: Any, *, profile_label: str = "active") -> Path:
    manifest = build_effective_claims_manifest(repo_root, deployment, profile_label=profile_label)
    path = repo_root / "compliance" / "claims" / f"effective-target-claims.{profile_label}.yaml"
    _write_yaml(path, manifest)
    return path


def build_effective_evidence_manifest(repo_root: Path, deployment: Any, *, profile_label: str = "active") -> dict[str, Any]:
    target_to_evidence = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-evidence.yaml")
    claims_manifest = build_effective_claims_manifest(repo_root, deployment, profile_label=profile_label)
    claims = claims_manifest.get("claim_set", {}).get("claims", [])
    bundles = []
    missing_refs = []
    for claim in claims:
        target = str(claim.get("target"))
        refs = list(target_to_evidence.get(target, []))
        if not refs:
            missing_refs.append(target)
        bundles.append({"target": target, "tier": int(claim.get("tier", 0)), "refs": refs})
    return {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "profile_label": profile_label,
        "effective_deployment": deployment.to_manifest(),
        "bundle_manifest": {
            "bundles": bundles,
            "missing_refs": missing_refs,
        },
    }


def write_effective_evidence_manifest(repo_root: Path, deployment: Any, *, profile_label: str = "active") -> Path:
    manifest = build_effective_evidence_manifest(repo_root, deployment, profile_label=profile_label)
    path = repo_root / "compliance" / "evidence" / f"effective-release-evidence.{profile_label}.yaml"
    _write_yaml(path, manifest)
    return path
