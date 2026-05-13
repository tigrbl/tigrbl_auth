"""Integration coverage for the default auth HTTP surface."""

from __future__ import annotations

from http import HTTPStatus as status
from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient, BasicAuth
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tigrbl_auth.crypto import hash_pw
from tigrbl_auth.orm import Client, ClientRegistration, Tenant, User
from tigrbl_auth.services.persistence import get_token_record_async
from tigrbl_auth.services.token_service import JWTCoder, issue_persisted_token_pair


def _unique_tenant(label: str) -> Tenant:
    suffix = uuid4().hex[:8]
    return Tenant(
        slug=f"{label}-{suffix}",
        name=f"{label.title()} Tenant",
        email=f"{label}-{suffix}@example.com",
    )


async def _create_tenant(db_session: AsyncSession, label: str) -> Tenant:
    tenant = _unique_tenant(label)
    db_session.add(tenant)
    await db_session.commit()
    return tenant


async def _create_user(
    db_session: AsyncSession,
    tenant: Tenant,
    *,
    username: str,
    email: str,
    password: str = "TestPassword123!",
    is_active: bool = True,
) -> User:
    user = User(
        tenant_id=tenant.id,
        username=username,
        email=email,
        password_hash=hash_pw(password),
        is_active=is_active,
    )
    db_session.add(user)
    await db_session.commit()
    return user


async def _create_confidential_client(
    db_session: AsyncSession,
    tenant: Tenant,
    *,
    secret: str = "client-secret",
) -> Client:
    client = Client.new(
        tenant_id=tenant.id,
        client_id=str(uuid4()),
        client_secret=secret,
        redirects=["https://client.example/callback"],
    )
    db_session.add(client)
    await db_session.commit()
    return client


async def _register_client(async_client: AsyncClient, tenant_slug: str) -> dict[str, object]:
    response = await async_client.post(
        "/register",
        json={
            "tenant_slug": tenant_slug,
            "redirect_uris": ["https://client.example/callback"],
            "client_name": "Example Client",
            "scope": "openid profile email",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    return response.json()


@pytest.mark.integration
class TestRegistrationFlow:
    async def test_register_client_success(
        self, async_client: AsyncClient, db_session: AsyncSession
    ) -> None:
        tenant = await _create_tenant(db_session, "register")

        response_data = await _register_client(async_client, tenant.slug)

        assert response_data["redirect_uris"] == ["https://client.example/callback"]
        assert response_data["grant_types"] == ["authorization_code"]
        assert response_data["response_types"] == ["code"]
        assert response_data["token_endpoint_auth_method"] == "client_secret_basic"
        assert response_data["registration_access_token"]
        assert response_data["registration_client_uri"].endswith(
            f"/register/{response_data['client_id']}"
        )
        client_uuid = UUID(str(response_data["client_id"]))

        client = await db_session.scalar(
            select(Client).where(Client.id == client_uuid)
        )
        registration = await db_session.scalar(
            select(ClientRegistration).where(
                ClientRegistration.client_id == client_uuid
            )
        )
        assert client is not None
        assert registration is not None

    async def test_register_client_rejects_unknown_tenant(
        self, async_client: AsyncClient
    ) -> None:
        response = await async_client.post(
            "/register",
            json={"tenant_slug": "missing-tenant", "redirect_uris": ["https://client.example/callback"]},
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "tenant not found"

    async def test_register_client_requires_https_redirects(
        self, async_client: AsyncClient, db_session: AsyncSession
    ) -> None:
        tenant = await _create_tenant(db_session, "register-https")

        response = await async_client.post(
            "/register",
            json={"tenant_slug": tenant.slug, "redirect_uris": ["http://client.example/callback"]},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "redirect_uris must use https"

    async def test_legacy_register_path_is_explicitly_unsupported(
        self, async_client: AsyncClient, db_session: AsyncSession
    ) -> None:
        tenant = await _create_tenant(db_session, "register-legacy")

        response = await async_client.post(
            "/client/register",
            json={"tenant_slug": tenant.slug, "redirect_uris": ["https://client.example/callback"]},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "use /register" in response.json()["detail"]


@pytest.mark.integration
class TestLoginFlow:
    async def test_login_with_username_password(
        self, async_client: AsyncClient, db_session: AsyncSession
    ) -> None:
        tenant = await _create_tenant(db_session, "login-user")
        user = await _create_user(
            db_session,
            tenant,
            username="testuser",
            email="testuser@example.com",
        )

        response = await async_client.post(
            "/login",
            json={"identifier": "testuser", "password": "TestPassword123!"},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["token_type"] == "bearer"
        assert data["session_id"]
        assert async_client.cookies.get("sid") is not None

        payload = JWTCoder.default().decode(data["access_token"])
        assert payload["sub"] == str(user.id)
        assert payload["tid"] == str(tenant.id)

    async def test_login_with_email_password(
        self, async_client: AsyncClient, db_session: AsyncSession
    ) -> None:
        tenant = await _create_tenant(db_session, "login-email")
        await _create_user(
            db_session,
            tenant,
            username="emailuser",
            email="emailuser@example.com",
        )

        response = await async_client.post(
            "/login",
            json={"identifier": "emailuser@example.com", "password": "TestPassword123!"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["token_type"] == "bearer"

    async def test_login_rejects_invalid_credentials(
        self, async_client: AsyncClient, db_session: AsyncSession
    ) -> None:
        tenant = await _create_tenant(db_session, "login-invalid")
        await _create_user(
            db_session,
            tenant,
            username="invaliduser",
            email="invaliduser@example.com",
        )

        response = await async_client.post(
            "/login",
            json={"identifier": "invaliduser", "password": "WrongPassword!"},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "invalid credentials"

    async def test_login_rejects_inactive_user(
        self, async_client: AsyncClient, db_session: AsyncSession
    ) -> None:
        tenant = await _create_tenant(db_session, "login-inactive")
        await _create_user(
            db_session,
            tenant,
            username="inactiveuser",
            email="inactiveuser@example.com",
            is_active=False,
        )

        response = await async_client.post(
            "/login",
            json={"identifier": "inactiveuser", "password": "TestPassword123!"},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "invalid credentials"


@pytest.mark.integration
class TestTokenEndpoint:
    async def test_password_grant_with_client_basic_auth(
        self, async_client: AsyncClient, db_session: AsyncSession
    ) -> None:
        tenant = await _create_tenant(db_session, "token-password")
        await _create_user(
            db_session,
            tenant,
            username="grantuser",
            email="grantuser@example.com",
        )
        client = await _create_confidential_client(
            db_session,
            tenant,
            secret="password-secret",
        )

        response = await async_client.post(
            "/token",
            data={
                "grant_type": "password",
                "username": "grantuser",
                "password": "TestPassword123!",
            },
            auth=BasicAuth(str(client.id), "password-secret"),
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["token_type"] == "bearer"

    async def test_refresh_with_valid_token(
        self, async_client: AsyncClient, db_session: AsyncSession
    ) -> None:
        tenant = await _create_tenant(db_session, "token-refresh")
        user = await _create_user(
            db_session,
            tenant,
            username="refreshuser",
            email="refreshuser@example.com",
        )
        client = await _create_confidential_client(
            db_session,
            tenant,
            secret="refresh-secret",
        )

        jwt_coder = JWTCoder.default()
        access_token, refresh_token = await issue_persisted_token_pair(
            jwt=jwt_coder,
            sub=str(user.id),
            tid=str(tenant.id),
            client_id=str(client.id),
        )

        response = await async_client.post(
            "/token",
            data={"grant_type": "refresh_token", "refresh_token": refresh_token},
            auth=BasicAuth(str(client.id), "refresh-secret"),
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["token_type"] == "bearer"
        assert data["access_token"] != access_token
        assert data["refresh_token"] != refresh_token

        used_record = await get_token_record_async(refresh_token)
        successor_record = await get_token_record_async(data["refresh_token"])
        assert used_record is not None
        assert successor_record is not None
        assert used_record.used_at is not None
        assert used_record.refresh_successor_hash == successor_record.token_hash
        assert successor_record.refresh_parent_hash == used_record.token_hash
        assert successor_record.refresh_family_id == used_record.refresh_family_id

    async def test_refresh_with_invalid_token(
        self, async_client: AsyncClient, db_session: AsyncSession
    ) -> None:
        tenant = await _create_tenant(db_session, "token-invalid")
        client = await _create_confidential_client(
            db_session,
            tenant,
            secret="invalid-secret",
        )

        response = await async_client.post(
            "/token",
            data={"grant_type": "refresh_token", "refresh_token": "invalid.token.here"},
            auth=BasicAuth(str(client.id), "invalid-secret"),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["error"] == "invalid_grant"

    async def test_refresh_reuse_revokes_the_entire_family(
        self, async_client: AsyncClient, db_session: AsyncSession
    ) -> None:
        tenant = await _create_tenant(db_session, "token-reuse")
        user = await _create_user(
            db_session,
            tenant,
            username="familyuser",
            email="familyuser@example.com",
        )
        client = await _create_confidential_client(
            db_session,
            tenant,
            secret="family-secret",
        )

        jwt_coder = JWTCoder.default()
        _, refresh_token = await issue_persisted_token_pair(
            jwt=jwt_coder,
            sub=str(user.id),
            tid=str(tenant.id),
            client_id=str(client.id),
        )

        request = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        first = await async_client.post(
            "/token",
            data=request,
            auth=BasicAuth(str(client.id), "family-secret"),
        )
        assert first.status_code == status.HTTP_200_OK

        replay = await async_client.post(
            "/token",
            data=request,
            auth=BasicAuth(str(client.id), "family-secret"),
        )
        assert replay.status_code == status.HTTP_400_BAD_REQUEST
        assert replay.json()["error"] == "invalid_grant"

        child_refresh = first.json()["refresh_token"]
        reused_record = await get_token_record_async(refresh_token)
        child_record = await get_token_record_async(child_refresh)
        assert reused_record is not None and reused_record.reuse_detected_at is not None
        assert child_record is not None and child_record.revoked_reason == "refresh_token_reuse_detected"


@pytest.mark.integration
class TestLogoutEndpoint:
    async def test_logout_post_clears_session_cookie(
        self, async_client: AsyncClient, db_session: AsyncSession
    ) -> None:
        tenant = await _create_tenant(db_session, "logout-post")
        await _create_user(
            db_session,
            tenant,
            username="logoutuser",
            email="logoutuser@example.com",
        )

        login_response = await async_client.post(
            "/login",
            json={"identifier": "logoutuser", "password": "TestPassword123!"},
        )
        assert login_response.status_code == status.HTTP_200_OK
        assert async_client.cookies.get("sid") is not None

        logout_response = await async_client.post("/logout")

        assert logout_response.status_code == status.HTTP_200_OK
        assert logout_response.json()["status"] == "logged_out"
        assert async_client.cookies.get("sid") is None


@pytest.mark.integration
class TestIntrospectionEndpoint:
    async def test_introspect_valid_access_token(
        self, async_client: AsyncClient, db_session: AsyncSession, enable_rfc7662
    ) -> None:
        tenant = await _create_tenant(db_session, "introspect-valid")
        user = await _create_user(
            db_session,
            tenant,
            username="introspectuser",
            email="introspectuser@example.com",
        )
        client = await _create_confidential_client(db_session, tenant)

        access_token, _ = await issue_persisted_token_pair(
            jwt=JWTCoder.default(),
            sub=str(user.id),
            tid=str(tenant.id),
            client_id=str(client.id),
        )

        response = await async_client.post(
            "/introspect",
            data={"token": access_token},
            auth=BasicAuth(str(client.id), "client-secret"),
        )

        assert response.status_code == status.HTTP_200_OK
        payload = response.json()
        assert payload["active"] is True
        assert payload["sub"] == str(user.id)
        assert payload["tid"] == str(tenant.id)

    async def test_introspect_invalid_token(
        self, async_client: AsyncClient, db_session: AsyncSession, enable_rfc7662
    ) -> None:
        tenant = await _create_tenant(db_session, "introspect-invalid")
        client = await _create_confidential_client(db_session, tenant, secret="invalid-token-secret")
        response = await async_client.post(
            "/introspect",
            data={"token": "invalid-token"},
            auth=BasicAuth(str(client.id), "invalid-token-secret"),
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"active": False}


@pytest.mark.integration
async def test_authentication_helpers() -> None:
    from tigrbl_auth.crypto import verify_pw

    password = "TestPassword123!"
    hashed = hash_pw(password)

    assert verify_pw(password, hashed) is True
    assert verify_pw("wrong", hashed) is False
