import pytest
from uuid import uuid4
from urllib.parse import parse_qs, urlparse
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tba_auth.tables import Tenant, User, Client
from tba_auth.crypto import hash_pw


async def _prepare(db: AsyncSession) -> str:
    tenant = Tenant(slug="t1", name="T1", email="t1@example.com")
    db.add(tenant)
    await db.commit()
    user = User(
        tenant_id=tenant.id,
        username="alice",
        email="alice@example.com",
        password_hash=hash_pw("Passw0rd!"),
    )
    db.add(user)
    await db.commit()
    client = Client(
        tenant_id=tenant.id,
        id=uuid4(),
        client_secret_hash=hash_pw("secret"),
        redirect_uris="https://client.example.com/cb",
    )
    db.add(client)
    await db.commit()
    return str(client.id)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_authorize_token_flow(
    async_client: AsyncClient, db_session: AsyncSession
):
    client_id = await _prepare(db_session)
    login = await async_client.post(
        "/login", json={"identifier": "alice", "password": "Passw0rd!"}
    )
    assert login.status_code == 200, login.text
    params = {
        "response_type": "token",
        "client_id": client_id,
        "redirect_uri": "https://client.example.com/cb",
        "scope": "openid",
        "state": "xyz",
    }
    resp = await async_client.get("/authorize", params=params, follow_redirects=False)
    assert resp.status_code in {302, 307}
    qs = parse_qs(urlparse(resp.headers["location"]).fragment)
    assert "access_token" in qs
    assert qs.get("token_type", [None])[0] == "bearer"
    assert qs.get("state", [None])[0] == "xyz"
