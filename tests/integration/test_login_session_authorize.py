from __future__ import annotations

from http import HTTPStatus as status
from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tigrbl_auth.crypto import hash_pw
from tigrbl_auth.orm import AuthSession, Client, Tenant, User


@pytest.mark.integration
async def test_login_commits_browser_session_for_authorize(
    async_client: AsyncClient, db_session: AsyncSession
) -> None:
    tenant = Tenant(
        slug=f"login-authorize-{uuid4().hex[:8]}",
        name="Login Authorize Tenant",
        email="login-authorize@example.com",
    )
    db_session.add(tenant)
    await db_session.commit()

    user = User(
        tenant_id=tenant.id,
        username="authorize-user",
        email="authorize-user@example.com",
        password_hash=hash_pw("TestPassword123!"),
        is_active=True,
    )
    db_session.add(user)

    client = Client.new(
        tenant_id=tenant.id,
        client_id=str(uuid4()),
        client_secret="authorize-secret",
        redirects=["https://client.example/callback"],
    )
    db_session.add(client)
    await db_session.commit()

    login = await async_client.post(
        "/login",
        json={"identifier": user.email, "password": "TestPassword123!"},
    )
    assert login.status_code == status.HTTP_200_OK
    session_id = UUID(str(login.json()["session_id"]))
    assert async_client.cookies.get("sid") is not None

    session_row = await db_session.scalar(
        select(AuthSession).where(AuthSession.id == session_id)
    )
    assert session_row is not None
    assert session_row.user_id == user.id

    authorize = await async_client.get(
        "/authorize",
        params={
            "client_id": str(client.id),
            "redirect_uri": "https://client.example/callback",
            "response_type": "code",
            "scope": "openid profile email",
            "state": "login-session-state",
            "code_challenge": "a" * 43,
            "code_challenge_method": "S256",
            "nonce": "login-session-nonce",
        },
    )
    assert authorize.status_code in {
        status.HTTP_302_FOUND,
        status.HTTP_303_SEE_OTHER,
        status.HTTP_307_TEMPORARY_REDIRECT,
    }
    location = authorize.headers["location"]
    assert location.startswith("https://client.example/callback?")
    assert "code=" in location
    assert "state=login-session-state" in location
