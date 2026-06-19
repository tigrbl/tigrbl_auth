from __future__ import annotations

def _openapi_operation(path: str, method: str, meta: dict[str, Any], deployment: Any) -> dict[str, Any]:
    policy = runtime_security_profile(deployment)
    operation_id = path.strip("/").replace("/", "_").replace(".", "_").replace("-", "_").replace("{", "").replace("}", "")
    op: dict[str, Any] = {
        "operationId": f"{method}_{operation_id or 'root'}",
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
    if "{tenant_slug}" in path:
        op["parameters"] = [
            {"name": "tenant_slug", "in": "path", "required": True, "schema": {"type": "string"}}
        ]
    elif "{realm_slug}" in path:
        op["parameters"] = [
            {"name": "realm_slug", "in": "path", "required": True, "schema": {"type": "string"}}
        ]
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
                            "tls_client_auth_subject_dn": {"type": "string"},
                            "tls_client_auth_san_dns": {"type": "string"},
                            "tls_client_auth_san_uri": {"type": "string"},
                            "tls_client_auth_san_ip": {"type": "string"},
                            "tls_client_auth_san_email": {"type": "string"},
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
                                "tls_client_auth_subject_dn": {"type": "string"},
                                "tls_client_auth_san_dns": {"type": "string"},
                                "tls_client_auth_san_uri": {"type": "string"},
                                "tls_client_auth_san_ip": {"type": "string"},
                                "tls_client_auth_san_email": {"type": "string"},
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
    elif path in {"/.well-known/openid-configuration", TENANT_OPENID_CONFIGURATION_PATH, REALM_OPENID_CONFIGURATION_PATH}:
        op["responses"]["200"]["content"] = _json_content("#/components/schemas/DiscoveryDocument")
    elif path == "/.well-known/oauth-authorization-server":
        op["responses"]["200"]["content"] = _json_content("#/components/schemas/AuthorizationServerMetadata")
    elif path == "/.well-known/oauth-protected-resource":
        op["responses"]["200"]["content"] = _json_content("#/components/schemas/ProtectedResourceMetadata")
    elif path in {"/.well-known/jwks.json", TENANT_JWKS_PATH, REALM_JWKS_PATH}:
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
