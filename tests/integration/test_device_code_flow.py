"""Integration test for Device Code (RFC 8628) flow on the canon tigrbl_auth app."""

import pytest
from http import HTTPStatus as status
from httpx import ASGITransport, AsyncClient
from uuid import uuid4

from tigrbl_auth_backend_app_core import build_app
from tigrbl_auth.config.deployment import resolve_deployment
from tigrbl_auth.db import get_db as legacy_get_db
from tigrbl_identity_jose.key_management import hash_pw
from tigrbl_auth.rfc.rfc8628 import approve_device_code
from tigrbl_auth.tables import Client, Tenant, User
from tigrbl_identity_storage_runtime.engine import get_db as tables_get_db
from tigrbl_auth.tables.engine import get_db as engine_get_db


@pytest.mark.integration
@pytest.mark.asyncio
async def test_device_code_flow(db_session) -> None:
    """Device code flow should exchange a code for an access token after approval."""
    tenant = Tenant(slug=f"tenant-{uuid4().hex[:8]}", name="Device Tenant", email="tenant@example.test")
    db_session.add(tenant)
    await db_session.flush()
    client_id = uuid4()
    client = Client.new(
        tenant_id=tenant.id,
        client_id=str(client_id),
        client_secret="device-client-secret",
        redirects=["https://client.example/callback"],
    )
    db_session.add(client)
    user = User(
        tenant_id=tenant.id,
        username=f"device-user-{uuid4().hex[:8]}",
        email=f"device-{uuid4().hex[:8]}@example.test",
        password_hash=hash_pw("DevicePass123!"),
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()

    deployment = resolve_deployment(
        profile="hardening",
        plugin_mode="public-only",
        flag_overrides={"enable_rfc9700": False},
    )
    app = build_app(deployment=deployment)

    def _override_db():
        return db_session

    for dependency in {legacy_get_db, tables_get_db, engine_get_db}:
        app.router.dependency_overrides[dependency] = _override_db
        app.dependency_overrides[dependency] = _override_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="https://test") as async_client:
        auth_resp = await async_client.post(
            "/device_authorization",
            data={"client_id": str(client_id), "scope": "openid"},
        )
        assert auth_resp.status_code == status.HTTP_200_OK
        data = auth_resp.json()
        device_code = data["device_code"]
        assert "user_code" in data

        payload = {
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "device_code": device_code,
            "client_id": str(client_id),
        }
        pending = await async_client.post("/token", data=payload)
        assert pending.status_code == status.HTTP_400_BAD_REQUEST
        assert pending.json()["error"] == "authorization_pending"

        await approve_device_code.__wrapped__(
            {"db": db_session, "payload": {"device_code": device_code, "sub": str(user.id), "tid": str(tenant.id)}}
        )
        success = await async_client.post("/token", data=payload)
        assert success.status_code == status.HTTP_200_OK
        token_data = success.json()
        assert "access_token" in token_data
        assert token_data["token_type"].lower() == "bearer"
