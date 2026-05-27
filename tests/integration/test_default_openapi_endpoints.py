"""Regression coverage for the Swagger "default" section."""

from __future__ import annotations

from http import HTTPStatus as status
from pathlib import Path
from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tigrbl_auth.app import app
from tigrbl_auth.crypto import hash_pw
from tigrbl_auth.orm import Tenant, User
from tigrbl_auth.services._operator_store import OperationContext
from tigrbl_auth.services.operator_service import create_resource


EXPECTED_DEFAULT_OPERATIONS = {
    ("post", "/login"),
    ("get", "/authorize"),
    ("post", "/token"),
    ("post", "/register"),
    ("get", "/register/{client_id}"),
    ("put", "/register/{client_id}"),
    ("delete", "/register/{client_id}"),
    ("post", "/revoke"),
    ("get", "/logout"),
    ("post", "/logout"),
    ("get", "/userinfo"),
    ("post", "/introspect"),
}


def _default_operations() -> set[tuple[str, str]]:
    openapi = app.openapi()
    operations: set[tuple[str, str]] = set()
    for path, path_item in openapi["paths"].items():
        for method, operation in path_item.items():
            if not isinstance(operation, dict):
                continue
            if operation.get("tags"):
                continue
            operations.add((method, path))
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
    create_resource(
        OperationContext(
            repo_root=Path.cwd(),
            command="tenant.create",
            resource="tenant",
            actor="integration-test",
            profile="integration",
            tenant=tenant.slug,
        ),
        record_id=tenant.slug,
        patch={"name": tenant.name, "enabled": True, "sql_tenant_id": str(tenant.id)},
        if_exists="update",
    )
    return tenant


@pytest.mark.integration
def test_openapi_default_section_matches_expected_untagged_operations() -> None:
    assert _default_operations() == EXPECTED_DEFAULT_OPERATIONS


@pytest.mark.integration
@pytest.mark.asyncio
async def test_default_endpoints_cover_runtime_behavior(
    async_client: AsyncClient,
    db_session: AsyncSession,
    enable_rfc7009,
    enable_rfc7662,
) -> None:
    tenant = await _create_tenant(db_session, "default-openapi")
    user = User(
        tenant_id=tenant.id,
        username="default-user",
        email="default-user@example.com",
        password_hash=hash_pw("TestPassword123!"),
    )
    db_session.add(user)
    await db_session.commit()

    register_response = await async_client.post(
        "/register",
        json={
            "tenant_slug": tenant.slug,
            "redirect_uris": ["https://default.example/callback"],
            "client_name": "Default Coverage Client",
        },
    )
    assert register_response.status_code == status.HTTP_200_OK
    registration = register_response.json()
    client_id = registration["client_id"]
    registration_token = registration["registration_access_token"]
    registration_headers = {"Authorization": f"Bearer {registration_token}"}

    legacy_register = await async_client.post("/client/register", json={})
    assert legacy_register.status_code == status.HTTP_404_NOT_FOUND

    authorize_response = await async_client.get("/authorize")
    assert authorize_response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in authorize_response.json()["detail"]

    login_response = await async_client.post(
        "/login",
        json={"identifier": "default-user", "password": "TestPassword123!"},
    )
    assert login_response.status_code == status.HTTP_200_OK

    token_response = await async_client.post("/token", data={})
    assert token_response.status_code == status.HTTP_401_UNAUTHORIZED
    assert token_response.json()["error"] == "invalid_client"

    get_registration = await async_client.get(
        f"/register/{client_id}",
        headers=registration_headers,
    )
    assert get_registration.status_code == status.HTTP_200_OK
    assert get_registration.json()["client_id"] == client_id

    update_payload = {"client_name": "Updated Default Coverage Client"}
    put_registration = await async_client.put(
        f"/register/{client_id}",
        headers=registration_headers,
        json=update_payload,
    )
    assert put_registration.status_code == status.HTTP_200_OK
    assert put_registration.json()["client_name"] == "Updated Default Coverage Client"

    legacy_get = await async_client.get(f"/client/{client_id}", headers=registration_headers)
    legacy_put = await async_client.put(
        f"/client/{client_id}",
        headers=registration_headers,
        json={"client_name": "Legacy Put Client"},
    )
    legacy_patch = await async_client.patch(
        f"/client/{client_id}",
        headers=registration_headers,
        json={"client_name": "Legacy Patch Client"},
    )
    assert legacy_get.status_code == status.HTTP_404_NOT_FOUND
    assert legacy_put.status_code == status.HTTP_404_NOT_FOUND
    assert legacy_patch.status_code == status.HTTP_404_NOT_FOUND

    revoke_response = await async_client.post("/revoke", data={"token": "tok-default"})
    assert revoke_response.status_code == status.HTTP_200_OK
    assert revoke_response.json() == {"revoked": True}

    revoke_legacy_response = await async_client.post(
        "/revoked_tokens/revoke",
        data={"token": "tok-default-legacy"},
    )
    assert revoke_legacy_response.status_code == status.HTTP_404_NOT_FOUND

    logout_get = await async_client.get("/logout")
    assert logout_get.status_code == status.HTTP_200_OK
    assert logout_get.json()["status"] in {"logged_out", "no_active_session"}

    userinfo_response = await async_client.get("/userinfo")
    assert userinfo_response.status_code == status.HTTP_401_UNAUTHORIZED

    introspect_response = await async_client.post(
        "/introspect",
        data={"token": "unknown-token"},
        auth=(client_id, registration["client_secret"]),
    )
    assert introspect_response.status_code == status.HTTP_200_OK
    assert introspect_response.json() == {"active": False}

    delete_registration = await async_client.delete(
        f"/register/{client_id}",
        headers=registration_headers,
    )
    assert delete_registration.status_code == status.HTTP_200_OK
    assert delete_registration.json() == {"status": "deleted", "client_id": client_id}

    legacy_delete = await async_client.delete(
        f"/client/{client_id}",
        headers=registration_headers,
    )
    assert legacy_delete.status_code == status.HTTP_404_NOT_FOUND

    relogin_response = await async_client.post(
        "/login",
        json={"identifier": "default-user", "password": "TestPassword123!"},
    )
    assert relogin_response.status_code == status.HTTP_200_OK

    logout_post = await async_client.post("/logout")
    assert logout_post.status_code == status.HTTP_200_OK
    assert logout_post.json()["status"] in {"logged_out", "no_active_session"}
