from __future__ import annotations

import asyncio
import importlib.util
import sys
from pathlib import Path
from urllib.parse import urlencode
from uuid import uuid4

import httpx
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tigrbl_auth.crypto import hash_pw
from tigrbl_auth.config.settings import settings as runtime_settings
from tigrbl_identity_storage.tables.device_code._op import device_authorization_request
from tigrbl_auth.tables import Client, DeviceCode, Tenant, User
from tigrbl_auth.services.token_service import JWTCoder, issue_persisted_token_pair
from tigrbl_auth_protocol_oauth.standards.authorization_server_metadata import ISSUER


def _load_example_module(module_name: str, relative_path: str):
    repo_root = Path(__file__).resolve().parents[2]
    module_path = repo_root / relative_path
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _install_example_package_path() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    src_path = repo_root / "examples" / "acme_notes_cli" / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))


async def _create_tenant_user_and_client(db_session: AsyncSession) -> tuple[Tenant, User, Client]:
    suffix = uuid4().hex[:8]
    tenant = Tenant(
        slug=f"device-cli-{suffix}",
        name="Device CLI Tenant",
        email=f"device-cli-{suffix}@example.com",
    )
    db_session.add(tenant)
    await db_session.commit()

    user = User(
        tenant_id=tenant.id,
        username="device-user",
        email="device-user@example.com",
        password_hash=hash_pw("DevicePassword123!"),
    )
    db_session.add(user)

    client = Client.new(
        tenant_id=tenant.id,
        client_id=str(uuid4()),
        client_secret="device-client-secret",
        redirects=["https://acme-notes.example/callback"],
    )
    db_session.add(client)
    await db_session.commit()
    return tenant, user, client


class _OpsRequest:
    def __init__(self, path: str, *, body: bytes = b"", headers: dict[str, str] | None = None):
        self.body = body
        self.headers = headers or {}
        self.scope = {"scheme": "https"}
        self.url = httpx.URL(f"https://test{path}")


class _TigrblAuthDeviceFlowTransport(httpx.AsyncBaseTransport):
    def __init__(self, db_session: AsyncSession, *, client_id: str):
        self._db_session = db_session
        self._client_id = client_id
        self._device_code: str | None = None

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if request.method == "GET" and path == "/.well-known/oauth-authorization-server":
            return httpx.Response(
                200,
                json={
                    "issuer": "https://test",
                    "token_endpoint": "https://test/token",
                    "device_authorization_endpoint": "https://test/device_authorization",
                },
                request=request,
            )

        if request.method == "POST" and path == "/device_authorization":
            body = urlencode({"client_id": self._client_id, "scope": "openid profile email"}).encode("utf-8")
            ops_request = _OpsRequest(path, body=body, headers=dict(request.headers))
            payload = await device_authorization_request(request=ops_request, db=self._db_session)
            self._device_code = str(payload["device_code"])
            return httpx.Response(200, json=payload, request=request)

        if request.method == "POST" and path == "/token":
            row = await self._db_session.scalar(
                select(DeviceCode).where(DeviceCode.device_code == (self._device_code or ""))
            )
            if row is None:
                return httpx.Response(400, json={"error": "invalid_grant"}, request=request)
            if not getattr(row, "authorized", False) or getattr(row, "user_id", None) is None:
                return httpx.Response(400, json={"error": "authorization_pending"}, request=request)
            access_token, refresh_token = await issue_persisted_token_pair(
                jwt=JWTCoder.default(),
                sub=str(row.user_id),
                tid=str(row.tenant_id),
                client_id=str(row.client_id),
                scope=row.scope,
                issuer=ISSUER,
                audience=row.audience or row.resource,
            )
            return httpx.Response(
                200,
                json={
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "bearer",
                },
                request=request,
            )

        return httpx.Response(404, json={"detail": "not found"}, request=request)


@pytest.mark.example
@pytest.mark.integration
@pytest.mark.asyncio
async def test_python_cli_package_can_login_via_tigrbl_auth_device_flow(
    db_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_example_package_path()
    device_login = _load_example_module(
        "acme_notes_cli.device_login",
        "examples/acme_notes_cli/src/acme_notes_cli/device_login.py",
    )
    monkeypatch.setattr(runtime_settings, "deployment_profile", "hardening")
    monkeypatch.setattr(runtime_settings, "enable_rfc8628", True)

    tenant, user, client = await _create_tenant_user_and_client(db_session)
    transport = _TigrblAuthDeviceFlowTransport(db_session, client_id=str(client.id))
    async with httpx.AsyncClient(transport=transport, base_url="https://test") as async_client:
        consumer = device_login.DeviceLoginClient(
            issuer="https://test",
            client_id=str(client.id),
            scope="openid profile email",
            http_client=async_client,
        )

        device = await consumer.start()
        assert device.verification_uri_complete.endswith(device.user_code)

        row = await db_session.scalar(select(DeviceCode).where(DeviceCode.device_code == device.device_code))
        assert row is not None
        row.authorized = True
        row.user_id = user.id
        row.tenant_id = tenant.id
        await db_session.commit()
        tokens = await consumer.poll_for_tokens(
            device.device_code,
            interval=0,
            expires_in=device.expires_in,
        )

    assert "access_token" in tokens
    assert tokens["token_type"].lower() == "bearer"
