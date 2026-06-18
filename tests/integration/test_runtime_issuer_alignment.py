from __future__ import annotations

from types import SimpleNamespace
from urllib.parse import parse_qs, urlparse
from uuid import UUID, uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tigrbl_auth import decode_jwt
from tigrbl_auth.api.app import build_app
from tigrbl_auth.config.deployment import DEFAULT_VALUES, resolve_deployment
from tigrbl_auth.crypto import hash_pw
from tigrbl_auth.db import get_db as legacy_get_db
from tigrbl_auth.tables import Client, Tenant, User
from tigrbl_auth.tables import get_db as tables_get_db
from tigrbl_auth.tables.engine import get_db as engine_get_db
from tigrbl_auth.rfc.rfc7636_pkce import makeCodeChallenge, makeCodeVerifier


pytestmark = pytest.mark.integration


def _settings(tmp_path) -> SimpleNamespace:
    values = dict(DEFAULT_VALUES)
    values.update(
        deployment_profile="production",
        issuer="https://issuer-alignment.example.test",
        protected_resource_identifier="https://issuer-alignment.example.test/resource",
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


@pytest.mark.asyncio
async def test_authorization_code_tokens_match_runtime_discovery_issuer(
    db_session: AsyncSession, monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    settings_obj = _settings(tmp_path)
    deployment = resolve_deployment(settings_obj, profile="production", plugin_mode="public-only")
    app = build_app(settings_obj, deployment=deployment)
    _override_db(app, db_session)

    tenant = Tenant(slug=f"issuer-{uuid4().hex[:8]}", name="Issuer Tenant", email=f"issuer-{uuid4().hex[:8]}@example.com")
    db_session.add(tenant)
    await db_session.commit()

    user = User(
        tenant_id=tenant.id,
        username="issuer-user",
        email="issuer-user@example.com",
        password_hash=hash_pw("Passw0rd!"),
    )
    db_session.add(user)
    await db_session.commit()

    client_id = str(uuid4())
    client = Client.new(
        tenant_id=tenant.id,
        client_id=client_id,
        client_secret="secret",
        redirects=["https://client.example.com/cb"],
    )
    db_session.add(client)
    await db_session.commit()

    async with AsyncClient(transport=ASGITransport(app=app), base_url=deployment.issuer) as client_http:
        discovery = await client_http.get("/.well-known/openid-configuration")
        assert discovery.status_code == 200
        discovery_issuer = discovery.json()["issuer"]

        login_resp = await client_http.post(
            "/login",
            json={"identifier": "issuer-user", "password": "Passw0rd!"},
        )
        assert login_resp.status_code == 200

        verifier = makeCodeVerifier()
        challenge = makeCodeChallenge(verifier)
        authorize_params = {
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": "https://client.example.com/cb",
            "scope": "openid",
            "state": "issuer-state",
            "code_challenge": challenge,
            "code_challenge_method": "S256",
        }
        authorize_resp = await client_http.get("/authorize", params=authorize_params, follow_redirects=False)
        assert authorize_resp.status_code in {302, 307}
        code = parse_qs(urlparse(authorize_resp.headers["location"]).query)["code"][0]
        assert UUID(code)

        token_resp = await client_http.post(
            "/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": "https://client.example.com/cb",
                "client_id": client_id,
                "code_verifier": verifier,
            },
        )
        assert token_resp.status_code == 200, token_resp.text
        payload = token_resp.json()

    access_claims = decode_jwt(payload["access_token"])
    id_claims = decode_jwt(payload["id_token"])
    assert discovery_issuer == deployment.issuer
    assert access_claims["iss"] == discovery_issuer
    assert id_claims["iss"] == discovery_issuer
