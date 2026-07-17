"""Tests for OAuth 2.0 token endpoint compliance with RFC 6749 §5.2."""

import pytest
import pytest_asyncio
from http import HTTPStatus as status
from httpx import ASGITransport, AsyncClient, BasicAuth
from unittest.mock import AsyncMock

from tigrbl_identity_storage_runtime.engine import get_db
from tigrbl import TigrblApp
from tigrbl_auth_backend_app_core.surfaces.auth_flows import router
from tigrbl_identity_runtime.deployment import resolve_deployment
from tigrbl_identity_runtime.settings import settings
from tigrbl_secret_hashing_bcrypt_provider import BcryptSecretHasher

CLIENT_ID = "00000000-0000-0000-0000-000000000000"
AUTH = BasicAuth(CLIENT_ID, "secret")


class DummyClient:
    id = CLIENT_ID
    tenant_id = "tenant"
    is_active = True
    client_secret_hash = BcryptSecretHasher(rounds=4).hash_secret("secret").encoded


class DummyDB:
    pass

@pytest_asyncio.fixture()
async def client(monkeypatch):
    app = TigrblApp()
    app.state.tigrbl_auth_deployment = resolve_deployment(
        settings, flag_overrides={"require_tls": False}
    )
    app.include_router(router)
    app.router.dependency_overrides[get_db] = lambda: DummyDB()
    monkeypatch.setattr(
        "tigrbl_identity_server.token_runtime.read_handler_record",
        AsyncMock(return_value=DummyClient()),
    )
    monkeypatch.setattr(
        "tigrbl_identity_server.token_runtime.first_handler_record",
        AsyncMock(return_value=None),
    )
    monkeypatch.setattr(
        "tigrbl_identity_server.token_runtime.issue_token_pair_records",
        AsyncMock(return_value=("access-token", "refresh-token")),
    )
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.fixture()
def enable_rfc6749():
    original = settings.enable_rfc6749
    settings.enable_rfc6749 = True
    try:
        yield
    finally:
        settings.enable_rfc6749 = original


@pytest.mark.unit
@pytest.mark.asyncio
async def test_missing_grant_type_returns_invalid_request(client, enable_rfc6749):
    """RFC 6749 §5.2: grant_type is required."""
    data = {"username": "user", "password": "pass"}
    resp = await client.post("/token", data=data, auth=AUTH)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json()["error"] == "invalid_request"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_unsupported_grant_type_returns_error(client, enable_rfc6749):
    """RFC 6749 §5.2: unsupported_grant_type is returned for unknown grants."""
    data = {
        "username": "user",
        "password": "pass",
        "grant_type": "unknown",
    }
    resp = await client.post("/token", data=data, auth=AUTH)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json()["error"] == "unsupported_grant_type"


@pytest.mark.unit
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        {"grant_type": "password", "username": "user"},
        {"grant_type": "password", "password": "pass"},
    ],
)
async def test_password_grant_requires_username_and_password(
    client, data, enable_rfc6749
):
    """RFC 6749 §4.3: username and password parameters are required."""
    resp = await client.post("/token", data=data, auth=AUTH)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json()["error"] == "invalid_request"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_password_grant_rejects_failed_capability_authentication(
    client,
    enable_rfc6749,
    monkeypatch,
):
    monkeypatch.setattr(
        "tigrbl_identity_server.token_request.authenticate_password",
        AsyncMock(return_value=None),
    )

    resp = await client.post(
        "/token",
        data={
            "grant_type": "password",
            "username": "user",
            "password": "wrong",
        },
        auth=AUTH,
    )

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json()["error"] == "invalid_grant"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_authorization_code_grant_requires_code(client, enable_rfc6749):
    """RFC 6749 §4.1.3: code and redirect_uri are required."""
    data = {
        "grant_type": "authorization_code",
        "redirect_uri": "https://c",
        "client_id": CLIENT_ID,
    }
    resp = await client.post("/token", data=data, auth=AUTH)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json()["error"] == "invalid_request"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_unsupported_grant_type_when_disabled(client):
    """Without RFC 6749 enforcement framework validation is returned."""
    original = settings.enable_rfc6749
    settings.enable_rfc6749 = False
    try:
        data = {
            "username": "user",
            "password": "pass",
            "grant_type": "unknown",
        }
        resp = await client.post("/token", data=data, auth=AUTH)
    finally:
        settings.enable_rfc6749 = original
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = resp.json()["detail"]
    assert detail[0]["loc"][-1] == "grant_type"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_client_credentials_grant_returns_token(client, enable_rfc6749):
    """Client credentials grant should return tokens when valid."""
    data = {"grant_type": "client_credentials"}
    resp = await client.post("/token", data=data, auth=AUTH)
    assert resp.status_code == status.HTTP_200_OK
    body = resp.json()
    assert "access_token" in body
    assert "refresh_token" in body
    assert body["token_type"] == "bearer"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_token_endpoint_requires_client_auth(client):
    """The token endpoint must reject requests without client authentication."""
    resp = await client.post("/token", data={"grant_type": "authorization_code"})
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    assert resp.json()["error"] == "invalid_client"
