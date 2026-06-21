from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from http import HTTPStatus
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tigrbl_auth.api.app import build_app
from tigrbl_auth.api.surfaces import TABLE_RESOURCES, admin_resource_path_prefixes
from tigrbl_auth.api.surfaces import surface_api as composed_surface_api
from tigrbl_auth.config.deployment import DEFAULT_VALUES, resolve_deployment
from tigrbl_auth.crypto import hash_pw
from tigrbl_auth.db import get_db as legacy_get_db
from tigrbl_auth.tables import Tenant, User
from tigrbl_identity_server.routers.surface import surface_api as legacy_surface_api
from tigrbl_auth.runtime.engine_resolver import (
    register_api_provider,
    resolve_api_provider,
    resolve_default_provider,
    set_default_provider,
)
from tigrbl_identity_storage.operator_store import OperationContext
from tigrbl_auth.services.operator_service import create_resource
from tigrbl_auth.services.session_service import observe_token_response
from tigrbl_auth.tables import AuditEvent, Client, Consent, RestOltpTable, get_db as tables_get_db
from tigrbl_auth.tables.engine import get_db as engine_get_db


pytestmark = pytest.mark.integration


def _settings(tmp_path: Path) -> SimpleNamespace:
    values = dict(DEFAULT_VALUES)
    values.update(
        deployment_profile="baseline",
        issuer="https://admin.example.test",
        protected_resource_identifier="https://admin.example.test/resource",
        require_tls=False,
        admin_api_key="test-admin-key",
        admin_api_key_dir=str(tmp_path),
    )
    return SimpleNamespace(**values)


def _override_db(app: object, session: AsyncSession) -> None:
    def _dependency_override():
        return session

    for dependency in (legacy_get_db, tables_get_db, engine_get_db):
        app.router.dependency_overrides[dependency] = _dependency_override
        app.dependency_overrides[dependency] = _dependency_override


async def _ensure_runtime_tables(provider: Any) -> None:
    setattr(legacy_surface_api, "_ddl_executed", False)
    initialize = getattr(legacy_surface_api, "initialize", None)
    if callable(initialize):
        await initialize()
    raw_engine, _ = provider.ensure()

    def _create_runtime_tables(sync_conn):
        RestOltpTable.metadata.create_all(bind=sync_conn, checkfirst=True)

    begin_ctx = raw_engine.begin()
    if hasattr(begin_ctx, "__aenter__"):
        async with begin_ctx as conn:
            await conn.run_sync(_create_runtime_tables)
    else:
        with begin_ctx as conn:
            _create_runtime_tables(conn)


@asynccontextmanager
async def _admin_client(tmp_path: Path, db_session: AsyncSession, test_db_engine):
    settings_obj = _settings(tmp_path)
    deployment = resolve_deployment(settings_obj, plugin_mode="mixed")
    app = build_app(settings_obj, deployment=deployment)
    provider = test_db_engine.provider
    original_legacy_surface = resolve_api_provider(legacy_surface_api)
    original_composed_surface = resolve_api_provider(composed_surface_api)
    original_app = resolve_api_provider(app)
    original_default_provider = resolve_default_provider()
    register_api_provider(legacy_surface_api, provider)
    register_api_provider(composed_surface_api, provider)
    register_api_provider(app, provider)
    set_default_provider(provider)
    await _ensure_runtime_tables(provider)
    _override_db(app, db_session)
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url=deployment.issuer) as client:
            yield client, deployment
    finally:
        register_api_provider(legacy_surface_api, original_legacy_surface or provider)
        register_api_provider(composed_surface_api, original_composed_surface or provider)
        register_api_provider(app, original_app or provider)
        if original_default_provider is not None:
            set_default_provider(original_default_provider)
        setattr(legacy_surface_api, "_ddl_executed", False)


async def _seed_db_records(db_session: AsyncSession) -> dict[str, str]:
    suffix = uuid4().hex[:8]
    tenant = Tenant(
        slug=f"admin-{suffix}",
        name=f"Admin Tenant {suffix}",
        email=f"admin-{suffix}@example.com",
    )
    db_session.add(tenant)
    await db_session.commit()

    user = User(
        tenant_id=tenant.id,
        username=f"admin-user-{suffix}",
        email=f"admin-user-{suffix}@example.com",
        password_hash=hash_pw("TestPassword123!"),
    )
    db_session.add(user)
    await db_session.commit()

    client = Client.new(
        tenant_id=tenant.id,
        client_id=str(uuid4()),
        client_secret="client-secret-12345",
        redirects=[f"https://client-{suffix}.example.test/callback"],
    )
    client.grant_types = "authorization_code refresh_token"
    client.response_types = "code"
    db_session.add(client)
    await db_session.commit()

    consent = Consent(
        tenant_id=tenant.id,
        user_id=user.id,
        client_id=client.id,
        scope="openid profile",
        claims={"sub": str(user.id)},
        state="active",
        granted_at=datetime.now(timezone.utc),
    )
    db_session.add(consent)

    audit = AuditEvent(
        tenant_id=tenant.id,
        actor_user_id=user.id,
        actor_client_id=client.id,
        event_type="test.audit",
        target_type="client",
        target_id=str(client.id),
        outcome="success",
        details={"source": "integration-test"},
        occurred_at=datetime.now(timezone.utc),
    )
    db_session.add(audit)
    await db_session.commit()

    return {
        "tenant_id": str(tenant.id),
        "user_id": str(user.id),
        "client_id": str(client.id),
    }


def _seed_operator_records(seed_ids: dict[str, str], deployment) -> None:
    repo_root = Path.cwd()
    tenant_id = seed_ids["tenant_id"]
    client_id = seed_ids["client_id"]
    user_id = seed_ids["user_id"]

    create_resource(
        OperationContext(
            repo_root=repo_root,
            command="seed-session",
            resource="session",
            actor="integration-test",
            profile=deployment.profile,
            tenant=tenant_id,
            issuer=deployment.issuer,
        ),
        record_id="session-integration",
        patch={
            "user_id": user_id,
            "tenant_id": tenant_id,
            "username": "integration-user",
            "client_id": client_id,
            "auth_time": datetime.now(timezone.utc).isoformat(),
            "session_state": "active",
            "metadata": {"source": "integration-test"},
        },
        if_exists="update",
    )

    create_resource(
        OperationContext(
            repo_root=repo_root,
            command="seed-key",
            resource="keys",
            actor="integration-test",
            profile=deployment.profile,
            tenant=tenant_id,
            issuer=deployment.issuer,
        ),
        record_id="kid-integration",
        patch={
            "kid": "kid-integration",
            "label": "integration-key",
            "alg": "EdDSA",
            "use": "sig",
            "kty": "OKP",
            "curve": "Ed25519",
        },
        if_exists="update",
    )

    observe_token_response(
        repo_root,
        access_token="rpc-access-token",
        actor="integration-test",
        tenant=tenant_id,
        issuer=deployment.issuer,
        details={
            "client_id": client_id,
            "subject": user_id,
            "scope": "openid profile",
        },
    )


def _admin_rest_operations(openapi: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    prefixes = admin_resource_path_prefixes()
    operations: dict[tuple[str, str], dict[str, Any]] = {}
    for path, path_item in openapi.get("paths", {}).items():
        if not any(path == prefix or path.startswith(f"{prefix}/") for prefix in prefixes):
            continue
        for method, operation in path_item.items():
            if isinstance(operation, dict):
                operations[(method.lower(), path)] = operation
    return operations


def _rpc_table_methods(openrpc: dict[str, Any]) -> dict[str, dict[str, Any]]:
    prefixes = admin_resource_path_prefixes()
    resource_names = {resource.__name__ for resource in TABLE_RESOURCES}
    methods: dict[str, dict[str, Any]] = {}
    for item in openrpc.get("methods", []):
        method_name = str(item["name"])
        if method_name.split(".", 1)[0] not in resource_names:
            continue
        bindings = item.get("x-tigrbl-surface", {}).get("bindings", [])
        has_table_binding = any(
            binding.get("proto") == "http.rest"
            and isinstance(binding.get("path"), str)
            and any(
                binding["path"] == prefix or binding["path"].startswith(f"{prefix}/")
                for prefix in prefixes
            )
            for binding in bindings
        )
        if has_table_binding:
            methods[method_name] = item
    return methods


async def _exercise_rest_operation(
    client: AsyncClient,
    method: str,
    path: str,
    headers: dict[str, str],
    operation: dict[str, Any],
    openapi: dict[str, Any],
) -> None:
    fake_uuid = "00000000-0000-0000-0000-000000000099"
    concrete_path = path.replace("{id}", fake_uuid).replace("{item_id}", fake_uuid)

    if "{id}" not in path and "{item_id}" not in path:
        if method == "get":
            response = await client.get(concrete_path, headers=headers)
            assert response.status_code == HTTPStatus.OK, response.text
            assert isinstance(response.json(), list)
            return
        if method == "post":
            response = await client.post(concrete_path, headers=headers, json={})
            assert response.status_code in {
                HTTPStatus.OK,
                HTTPStatus.CREATED,
                HTTPStatus.BAD_REQUEST,
                HTTPStatus.UNPROCESSABLE_ENTITY,
            }, response.text
            return
        if method == "delete":
            response = await client.delete(concrete_path, headers=headers)
            assert response.status_code in {
                HTTPStatus.OK,
                HTTPStatus.NO_CONTENT,
                HTTPStatus.BAD_REQUEST,
                HTTPStatus.NOT_FOUND,
                HTTPStatus.UNPROCESSABLE_ENTITY,
                HTTPStatus.NOT_IMPLEMENTED,
            }, response.text
            return
    else:
        if method == "get":
            response = await client.get(concrete_path, headers=headers)
            assert response.status_code in {HTTPStatus.NOT_FOUND, HTTPStatus.UNPROCESSABLE_ENTITY}, response.text
            return
        if method in {"patch", "put", "post"}:
            response = await client.request(
                method.upper(),
                concrete_path,
                headers=headers,
                json=_rest_request_payload(operation, openapi),
            )
            assert response.status_code in {
                HTTPStatus.OK,
                HTTPStatus.BAD_REQUEST,
                HTTPStatus.CONFLICT,
                HTTPStatus.NOT_FOUND,
                HTTPStatus.UNPROCESSABLE_ENTITY,
                HTTPStatus.INTERNAL_SERVER_ERROR,
            }, response.text
            return
        if method == "delete":
            response = await client.delete(concrete_path, headers=headers)
            assert response.status_code in {HTTPStatus.OK, HTTPStatus.NOT_FOUND, HTTPStatus.UNPROCESSABLE_ENTITY}, response.text
            return

    raise AssertionError(f"Unhandled REST admin operation: {method.upper()} {path}")


def _sample_schema_value(schema: dict[str, Any]) -> Any:
    any_of = schema.get("anyOf")
    if isinstance(any_of, list) and any_of:
        preferred = next(
            (candidate for candidate in any_of if candidate.get("type") != "null"),
            any_of[0],
        )
        return _sample_schema_value(preferred)
    one_of = schema.get("oneOf")
    if isinstance(one_of, list) and one_of:
        return _sample_schema_value(one_of[0])
    examples = schema.get("examples")
    if isinstance(examples, list) and examples:
        return examples[0]
    if "default" in schema and schema["default"] is not None:
        return schema["default"]

    schema_type = schema.get("type")
    schema_format = schema.get("format")
    if schema_format == "uuid":
        return "00000000-0000-0000-0000-000000000099"
    if schema_format == "date-time":
        return datetime.now(timezone.utc).isoformat()
    if schema_type == "string":
        return "integration-test"
    if schema_type == "integer":
        return 1
    if schema_type == "number":
        return 1
    if schema_type == "boolean":
        return True
    if schema_type == "array":
        item_schema = schema.get("items", {})
        return [_sample_schema_value(item_schema if isinstance(item_schema, dict) else {})]
    if schema_type == "object" or "properties" in schema:
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        payload: dict[str, Any] = {}
        for name in required:
            prop_schema = properties.get(name, {})
            payload[str(name)] = _sample_schema_value(prop_schema if isinstance(prop_schema, dict) else {})
        return payload
    return {}


def _resolve_schema_ref(openapi: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    current = schema
    while isinstance(current, dict) and "$ref" in current:
        ref = str(current["$ref"])
        prefix = "#/components/schemas/"
        if not ref.startswith(prefix):
            break
        name = ref[len(prefix) :]
        current = openapi.get("components", {}).get("schemas", {}).get(name, {})
    return current if isinstance(current, dict) else {}


def _rest_request_payload(operation: dict[str, Any], openapi: dict[str, Any] | None = None) -> dict[str, Any]:
    request_body = operation.get("requestBody", {})
    content = request_body.get("content", {})
    schema = (
        content.get("application/json", {}).get("schema")
        or content.get("application/*+json", {}).get("schema")
        or {}
    )
    if openapi is not None:
        schema = _resolve_schema_ref(openapi, schema if isinstance(schema, dict) else {})
    return _sample_schema_value(schema if isinstance(schema, dict) else {})


def _build_rpc_params(method_schema: dict[str, Any]) -> dict[str, Any]:
    params = method_schema.get("params", [])
    if not params:
        return {}
    schema = params[0].get("schema", {})
    return _sample_schema_value(schema if isinstance(schema, dict) else {})


async def _invoke_rpc(
    client: AsyncClient,
    headers: dict[str, str],
    method_name: str,
    params: dict[str, Any],
) -> dict[str, Any]:
    response = await client.post(
        "/rpc",
        headers=headers,
        json={"jsonrpc": "2.0", "method": method_name, "params": params, "id": method_name},
    )
    if response.status_code == HTTPStatus.NO_CONTENT and not response.text:
        return {"jsonrpc": "2.0", "result": None, "id": method_name}
    assert response.status_code == HTTPStatus.OK, response.text
    payload = response.json()
    assert payload["jsonrpc"] == "2.0"
    return payload


@pytest.mark.asyncio
async def test_admin_rest_table_endpoints_are_all_exercised(
    tmp_path,
    db_session: AsyncSession,
    test_db_engine,
) -> None:
    async with _admin_client(tmp_path, db_session, test_db_engine) as (client, _deployment):
        openapi = (await client.get("/openapi.json")).json()
        operations = _admin_rest_operations(openapi)
        headers = {"X-API-Key": "test-admin-key"}

        observed: set[tuple[str, str]] = set()
        for method, path in sorted(operations):
            await _exercise_rest_operation(client, method, path, headers, operations[(method, path)], openapi)
            observed.add((method, path))

    assert observed == set(operations)
    assert len({resource.__name__ for resource in TABLE_RESOURCES}) == len(TABLE_RESOURCES)


@pytest.mark.asyncio
async def test_admin_jsonrpc_table_methods_are_all_exercised(
    tmp_path,
    db_session: AsyncSession,
    test_db_engine,
) -> None:
    async with _admin_client(tmp_path, db_session, test_db_engine) as (client, deployment):
        seed_ids = await _seed_db_records(db_session)
        _seed_operator_records(seed_ids, deployment)
        openrpc = (await client.get("/openrpc.json")).json()
        methods = _rpc_table_methods(openrpc)
        headers = {"Authorization": "Bearer test-admin-key"}

        observed: set[str] = set()
        for method_name in sorted(methods):
            payload = await _invoke_rpc(client, headers, method_name, {})
            if payload.get("error", {}).get("code") == -32603:
                payload = await _invoke_rpc(
                    client,
                    headers,
                    method_name,
                    _build_rpc_params(methods[method_name]),
                )
            observed.add(method_name)
            if "error" in payload:
                assert payload["error"]["code"] != -32603, payload
            else:
                assert "result" in payload, payload

    assert observed == set(methods)
    assert observed
