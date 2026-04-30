from __future__ import annotations

from contextlib import asynccontextmanager
from http import HTTPStatus
from types import SimpleNamespace
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tigrbl_auth.api.app import build_app
from tigrbl_auth.config.deployment import DEFAULT_VALUES, VALID_PROFILES, resolve_deployment
from tigrbl_auth.crypto import hash_pw
from tigrbl_auth.db import get_db as legacy_get_db
from tigrbl_auth.orm import Tenant, User
from tigrbl_auth.tables import get_db as tables_get_db
from tigrbl_auth.tables.engine import get_db as engine_get_db


pytestmark = pytest.mark.integration


def _profile_settings(profile: str, tmp_path) -> SimpleNamespace:
    values = dict(DEFAULT_VALUES)
    issuer = f"https://{profile}.example.test"
    values.update(
        deployment_profile=profile,
        issuer=issuer,
        protected_resource_identifier=f"{issuer}/resource",
        require_tls=False,
        admin_api_key="test-admin-key",
        admin_api_key_dir=str(tmp_path),
    )
    return SimpleNamespace(**values)


def _apply_runtime_settings(monkeypatch: pytest.MonkeyPatch, settings_obj: SimpleNamespace, deployment) -> None:
    from tigrbl_auth.runtime_cfg import settings as runtime_settings

    for name, value in vars(settings_obj).items():
        if hasattr(runtime_settings, name):
            monkeypatch.setattr(runtime_settings, name, value)
    for name, value in deployment.flags.items():
        if hasattr(runtime_settings, name):
            monkeypatch.setattr(runtime_settings, name, value)


def _override_db(app: object, session: AsyncSession) -> None:
    def _dependency_override():
        return session

    app.router.dependency_overrides[legacy_get_db] = _dependency_override
    app.dependency_overrides[legacy_get_db] = _dependency_override
    app.router.dependency_overrides[tables_get_db] = _dependency_override
    app.dependency_overrides[tables_get_db] = _dependency_override
    app.router.dependency_overrides[engine_get_db] = _dependency_override
    app.dependency_overrides[engine_get_db] = _dependency_override


@asynccontextmanager
async def _profile_client(
    profile: str,
    tmp_path,
    db_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
):
    settings_obj = _profile_settings(profile, tmp_path)
    deployment = resolve_deployment(settings_obj, profile=profile, plugin_mode="public-only")
    _apply_runtime_settings(monkeypatch, settings_obj, deployment)
    app = build_app(settings_obj, deployment=deployment)
    _override_db(app, db_session)
    async with AsyncClient(transport=ASGITransport(app=app), base_url=deployment.issuer) as client:
        yield client, deployment


def _documented_operations(openapi: dict) -> set[tuple[str, str]]:
    operations: set[tuple[str, str]] = set()
    for path, path_item in openapi.get("paths", {}).items():
        for method, operation in path_item.items():
            if isinstance(operation, dict):
                operations.add((method.lower(), path))
    return operations


async def _create_tenant(db_session: AsyncSession, label: str) -> Tenant:
    suffix = uuid4().hex[:8]
    tenant = Tenant(
        slug=f"{label}-{suffix}",
        name=f"{label.title()} Tenant",
        email=f"{label}-{suffix}@example.com",
    )
    db_session.add(tenant)
    await db_session.commit()
    return tenant


async def _seed_user(db_session: AsyncSession, tenant: Tenant, username: str, password: str) -> None:
    user = User(
        tenant_id=tenant.id,
        username=username,
        email=f"{username}@example.com",
        password_hash=hash_pw(password),
    )
    db_session.add(user)
    await db_session.commit()


async def _register_client(client: AsyncClient, tenant: Tenant, deployment) -> dict:
    payload = {
        "tenant_slug": tenant.slug,
        "redirect_uris": [f"https://{deployment.profile}.example.test/callback"],
        "client_name": f"{deployment.profile} integration client",
    }
    if deployment.profile == "fapi2-security":
        payload.update(
            token_endpoint_auth_method="private_key_jwt",
            token_endpoint_auth_signing_alg="EdDSA",
            jwks_uri="https://client.example.test/jwks.json",
        )
    response = await client.post(
        "/register",
        json=payload,
    )
    assert response.status_code == HTTPStatus.OK, response.text
    payload = response.json()
    assert payload["client_id"]
    assert payload["registration_access_token"]
    return payload


async def _exercise_profile_operations(
    client: AsyncClient,
    deployment,
    documented_operations: set[tuple[str, str]],
    tenant: Tenant,
    username: str,
    password: str,
) -> None:
    observed: set[tuple[str, str]] = set()
    registration: dict | None = None

    async def expect(method: str, path: str, **kwargs):
        response = await client.request(method.upper(), path, **kwargs)
        observed.add((method, path if "{" not in path else kwargs.pop("_template")))
        return response

    for discovery_path, required_field in (
        ("/.well-known/openid-configuration", "issuer"),
        ("/.well-known/oauth-authorization-server", "issuer"),
        ("/.well-known/oauth-protected-resource", "resource"),
        ("/.well-known/jwks.json", "keys"),
    ):
        operation = ("get", discovery_path)
        if operation not in documented_operations:
            continue
        response = await client.get(discovery_path)
        observed.add(operation)
        assert response.status_code == HTTPStatus.OK, response.text
        payload = response.json()
        assert required_field in payload
        if required_field == "issuer":
            assert payload["issuer"] == deployment.issuer

    if ("post", "/login") in documented_operations:
        response = await client.post(
            "/login",
            json={"identifier": username, "password": password},
        )
        observed.add(("post", "/login"))
        assert response.status_code == HTTPStatus.OK, response.text

    if ("get", "/authorize") in documented_operations:
        response = await client.get("/authorize")
        observed.add(("get", "/authorize"))
        assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
        assert "error" in str(response.json().get("detail"))

    if ("post", "/token") in documented_operations:
        response = await client.post("/token", data={})
        observed.add(("post", "/token"))
        assert response.status_code in {HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED}, response.text

    if ("post", "/register") in documented_operations:
        registration = await _register_client(client, tenant, deployment)
        observed.add(("post", "/register"))

    if ("post", "/client/register") in documented_operations:
        response = await client.post(
            "/client/register",
            json={
                "tenant_slug": tenant.slug,
                "redirect_uris": [f"https://legacy-{deployment.profile}.example.test/callback"],
            },
        )
        observed.add(("post", "/client/register"))
        assert response.status_code == HTTPStatus.BAD_REQUEST, response.text

    if registration is not None:
        client_id = registration["client_id"]
        headers = {"Authorization": f"Bearer {registration['registration_access_token']}"}

        if ("get", "/register/{client_id}") in documented_operations:
            response = await client.get(f"/register/{client_id}", headers=headers)
            observed.add(("get", "/register/{client_id}"))
            assert response.status_code == HTTPStatus.OK, response.text
            assert response.json()["client_id"] == client_id

        if ("put", "/register/{client_id}") in documented_operations:
            response = await client.put(
                f"/register/{client_id}",
                headers=headers,
                json={"client_name": f"{deployment.profile} updated client"},
            )
            observed.add(("put", "/register/{client_id}"))
            assert response.status_code == HTTPStatus.OK, response.text
            assert response.json()["client_name"] == f"{deployment.profile} updated client"

        if ("get", "/client/{client_id}") in documented_operations:
            response = await client.get(f"/client/{client_id}", headers=headers)
            observed.add(("get", "/client/{client_id}"))
            assert response.status_code == HTTPStatus.OK, response.text
            assert response.json()["client_id"] == client_id

        if ("put", "/client/{client_id}") in documented_operations:
            response = await client.put(
                f"/client/{client_id}",
                headers=headers,
                json={"client_name": f"{deployment.profile} legacy put client"},
            )
            observed.add(("put", "/client/{client_id}"))
            assert response.status_code == HTTPStatus.OK, response.text

        if ("patch", "/client/{client_id}") in documented_operations:
            response = await client.patch(
                f"/client/{client_id}",
                headers=headers,
                json={"client_name": f"{deployment.profile} legacy patch client"},
            )
            observed.add(("patch", "/client/{client_id}"))
            assert response.status_code == HTTPStatus.OK, response.text

        if ("delete", "/client/{client_id}") in documented_operations:
            response = await client.delete(f"/client/{client_id}", headers=headers)
            observed.add(("delete", "/client/{client_id}"))
            assert response.status_code == HTTPStatus.OK, response.text

            if ("delete", "/register/{client_id}") in documented_operations:
                registration = await _register_client(client, tenant, deployment)
                client_id = registration["client_id"]
                headers = {"Authorization": f"Bearer {registration['registration_access_token']}"}

        if ("delete", "/register/{client_id}") in documented_operations:
            response = await client.delete(f"/register/{client_id}", headers=headers)
            observed.add(("delete", "/register/{client_id}"))
            assert response.status_code == HTTPStatus.OK, response.text

    if ("post", "/revoke") in documented_operations:
        response = await client.post("/revoke", data={"token": f"{deployment.profile}-token"})
        observed.add(("post", "/revoke"))
        assert response.status_code == HTTPStatus.OK, response.text
        assert response.json() == {"revoked": True}

    if ("post", "/revoked_tokens/revoke") in documented_operations:
        response = await client.post("/revoked_tokens/revoke", data={"token": f"{deployment.profile}-legacy-token"})
        observed.add(("post", "/revoked_tokens/revoke"))
        assert response.status_code == HTTPStatus.OK, response.text
        assert response.json() == {"revoked": True}

    if ("get", "/userinfo") in documented_operations:
        response = await client.get("/userinfo")
        observed.add(("get", "/userinfo"))
        assert response.status_code == HTTPStatus.UNAUTHORIZED, response.text

    if ("post", "/introspect") in documented_operations:
        response = await client.post("/introspect", data={"token": "unknown-token"})
        observed.add(("post", "/introspect"))
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.UNAUTHORIZED}, response.text
        if response.status_code == HTTPStatus.OK:
            assert response.json() == {"active": False}

    if ("post", "/device_authorization") in documented_operations:
        response = await client.post("/device_authorization", data={})
        observed.add(("post", "/device_authorization"))
        assert response.status_code in {
            HTTPStatus.BAD_REQUEST,
            HTTPStatus.UNAUTHORIZED,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        }, response.text

    if ("post", "/par") in documented_operations:
        response = await client.post("/par", data={})
        observed.add(("post", "/par"))
        assert response.status_code in {
            HTTPStatus.BAD_REQUEST,
            HTTPStatus.UNAUTHORIZED,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        }, response.text

    if ("post", "/token/exchange") in documented_operations:
        response = await client.post("/token/exchange", data={})
        observed.add(("post", "/token/exchange"))
        assert response.status_code in {
            HTTPStatus.BAD_REQUEST,
            HTTPStatus.UNAUTHORIZED,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        }, response.text

    if ("get", "/logout") in documented_operations:
        response = await client.get("/logout")
        observed.add(("get", "/logout"))
        assert response.status_code == HTTPStatus.OK, response.text

    if ("post", "/logout") in documented_operations:
        response = await client.post("/logout")
        observed.add(("post", "/logout"))
        assert response.status_code == HTTPStatus.OK, response.text

    assert observed == documented_operations


@pytest.mark.asyncio
@pytest.mark.parametrize("profile", VALID_PROFILES)
async def test_profile_openapi_includes_all_active_contract_routes(
    profile: str,
    tmp_path,
    db_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async with _profile_client(profile, tmp_path, db_session, monkeypatch) as (client, deployment):
        response = await client.get("/openapi.json")

    assert response.status_code == HTTPStatus.OK, response.text
    payload = response.json()
    paths = set(payload.get("paths", {}))
    assert set(deployment.active_contract_routes).issubset(paths)


@pytest.mark.asyncio
@pytest.mark.parametrize("profile", VALID_PROFILES)
async def test_profile_documented_endpoints_behave_as_expected(
    profile: str,
    tmp_path,
    db_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tenant = await _create_tenant(db_session, f"profile-{profile}")
    username = f"{profile}-user"
    password = "TestPassword123!"
    await _seed_user(db_session, tenant, username, password)

    async with _profile_client(profile, tmp_path, db_session, monkeypatch) as (client, deployment):
        openapi = (await client.get("/openapi.json")).json()
        documented_operations = _documented_operations(openapi)
        await _exercise_profile_operations(
            client,
            deployment,
            documented_operations,
            tenant,
            username,
            password,
        )
