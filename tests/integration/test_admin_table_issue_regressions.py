from __future__ import annotations

from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tigrbl_auth.crypto import hash_pw
from tigrbl_auth.tables import Client, LogoutState, PushedAuthorizationRequest
from tigrbl_auth.tables import RevokedToken, Tenant, TokenRecord, User

from tests.integration.test_admin_table_surfaces import _admin_client, _invoke_rpc


pytestmark = pytest.mark.integration


async def _create_isolated_tenant(db_session: AsyncSession, *, suffix: str) -> Tenant:
    tenant = Tenant(
        slug=f"tenant-{suffix}",
        name=f"Tenant {suffix}",
        email=f"tenant-{suffix}@example.com",
    )
    db_session.add(tenant)
    await db_session.commit()
    await db_session.refresh(tenant)
    return tenant


async def _create_isolated_user(db_session: AsyncSession, *, tenant_id, suffix: str) -> User:
    user = User(
        tenant_id=tenant_id,
        username=f"user-{suffix}",
        email=f"user-{suffix}@example.com",
        password_hash=hash_pw("TestPassword123!"),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


async def _create_isolated_client(db_session: AsyncSession, *, tenant_id, suffix: str) -> Client:
    client = Client.new(
        tenant_id=tenant_id,
        client_id=str(uuid4()),
        client_secret="client-secret-12345",
        redirects=[f"https://client-{suffix}.example.test/callback"],
    )
    client.grant_types = "authorization_code refresh_token"
    client.response_types = "code"
    db_session.add(client)
    await db_session.commit()
    await db_session.refresh(client)
    return client


@pytest.mark.asyncio
async def test_logoutstate_replace_updates_existing_record(
    tmp_path,
    db_session: AsyncSession,
    test_db_engine,
) -> None:
    async with _admin_client(tmp_path, db_session, test_db_engine) as (client, _deployment):
        record = LogoutState(
            status="pending",
            initiated_by="session-end",
            reason="initial",
            frontchannel_required=False,
            backchannel_required=True,
            logout_metadata={"phase": "before"},
        )
        db_session.add(record)
        await db_session.commit()
        await db_session.refresh(record)

        response = await client.put(
            f"/logoutstate/{record.id}",
            headers={"X-API-Key": "test-admin-key"},
            json={
                "status": "completed",
                "initiated_by": "operator",
                "reason": "verified",
                "frontchannel_required": True,
                "backchannel_required": False,
                "logout_metadata": {"phase": "after"},
            },
        )

        assert response.status_code == HTTPStatus.OK, response.text
        payload = response.json()
        assert payload["id"] == str(record.id)
        assert payload["status"] == "completed"
        assert payload["initiated_by"] == "operator"
        assert payload["logout_metadata"] == {"phase": "after"}


@pytest.mark.asyncio
async def test_pushedauthorizationrequest_replace_updates_existing_record(
    tmp_path,
    db_session: AsyncSession,
    test_db_engine,
) -> None:
    suffix = uuid4().hex[:8]
    tenant = await _create_isolated_tenant(db_session, suffix=suffix)
    client_row = await _create_isolated_client(db_session, tenant_id=tenant.id, suffix=suffix)

    async with _admin_client(tmp_path, db_session, test_db_engine) as (client, _deployment):
        record = PushedAuthorizationRequest(
            request_uri=f"urn:ietf:params:oauth:request_uri:{uuid4()}",
            client_id=client_row.id,
            tenant_id=tenant.id,
            params={"scope": "openid", "prompt": "login"},
            expires_in=90,
            expires_at=datetime.now(timezone.utc) + timedelta(seconds=90),
        )
        db_session.add(record)
        await db_session.commit()
        await db_session.refresh(record)

        replacement = {
            "request_uri": f"urn:ietf:params:oauth:request_uri:{uuid4()}",
            "client_id": str(client_row.id),
            "tenant_id": str(tenant.id),
            "params": {"scope": "openid profile", "prompt": "consent"},
            "expires_in": 120,
            "expires_at": (datetime.now(timezone.utc) + timedelta(seconds=120)).isoformat(),
        }
        response = await client.put(
            f"/pushedauthorizationrequest/{record.id}",
            headers={"X-API-Key": "test-admin-key"},
            json=replacement,
        )

        assert response.status_code == HTTPStatus.OK, response.text
        payload = response.json()
        assert payload["id"] == str(record.id)
        assert payload["request_uri"] == replacement["request_uri"]
        assert payload["params"] == replacement["params"]
        assert payload["expires_in"] == 120


@pytest.mark.asyncio
async def test_revokedtoken_replace_updates_existing_record(
    tmp_path,
    db_session: AsyncSession,
    test_db_engine,
) -> None:
    suffix = uuid4().hex[:8]
    tenant = await _create_isolated_tenant(db_session, suffix=suffix)
    client_row = await _create_isolated_client(db_session, tenant_id=tenant.id, suffix=suffix)

    async with _admin_client(tmp_path, db_session, test_db_engine) as (client, _deployment):
        record = RevokedToken(
            token_hash=f"token-hash-{suffix}",
            token_type_hint="access_token",
            subject=f"subject-{suffix}",
            tenant_id=tenant.id,
            client_id=client_row.id,
            revoked_reason="initial",
        )
        db_session.add(record)
        await db_session.commit()
        await db_session.refresh(record)

        response = await client.put(
            f"/revokedtoken/{record.id}",
            headers={"X-API-Key": "test-admin-key"},
            json={
                "token_hash": f"token-hash-{suffix}-updated",
                "token_type_hint": "refresh_token",
                "subject": f"subject-{suffix}-updated",
                "tenant_id": str(tenant.id),
                "client_id": str(client_row.id),
                "revoked_reason": "rotated",
            },
        )

        assert response.status_code == HTTPStatus.OK, response.text
        payload = response.json()
        assert payload["id"] == str(record.id)
        assert payload["token_hash"] == f"token-hash-{suffix}-updated"
        assert payload["revoked_reason"] == "rotated"


@pytest.mark.asyncio
async def test_tenant_replace_updates_existing_record(
    tmp_path,
    db_session: AsyncSession,
    test_db_engine,
) -> None:
    suffix = uuid4().hex[:8]

    async with _admin_client(tmp_path, db_session, test_db_engine) as (client, _deployment):
        tenant = await _create_isolated_tenant(db_session, suffix=suffix)

        response = await client.put(
            f"/tenant/{tenant.id}",
            headers={"X-API-Key": "test-admin-key"},
            json={
                "slug": f"tenant-{suffix}-updated",
                "name": f"Tenant {suffix} Updated",
                "email": f"tenant-{suffix}-updated@example.com",
            },
        )

        assert response.status_code == HTTPStatus.OK, response.text
        payload = response.json()
        assert payload["id"] == str(tenant.id)
        assert payload["slug"] == f"tenant-{suffix}-updated"
        assert payload["name"] == f"Tenant {suffix} Updated"
        assert payload["email"] == f"tenant-{suffix}-updated@example.com"


@pytest.mark.asyncio
async def test_tokenrecord_replace_updates_existing_record(
    tmp_path,
    db_session: AsyncSession,
    test_db_engine,
) -> None:
    suffix = uuid4().hex[:8]
    tenant = await _create_isolated_tenant(db_session, suffix=suffix)
    client_row = await _create_isolated_client(db_session, tenant_id=tenant.id, suffix=suffix)

    async with _admin_client(tmp_path, db_session, test_db_engine) as (client, _deployment):
        record = TokenRecord(
            token_hash=f"access-token-{suffix}",
            token_kind="access",
            token_type_hint="Bearer",
            subject=f"user-{suffix}",
            tenant_id=tenant.id,
            client_id=client_row.id,
            scope="openid",
            issuer="https://issuer.example.test",
            claims={"sub": f"user-{suffix}"},
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
        )
        db_session.add(record)
        await db_session.commit()
        await db_session.refresh(record)

        response = await client.put(
            f"/tokenrecord/{record.id}",
            headers={"X-API-Key": "test-admin-key"},
            json={
                "token_hash": f"access-token-{suffix}-updated",
                "token_kind": "refresh",
                "token_type_hint": "refresh_token",
                "active": False,
                "subject": f"user-{suffix}-updated",
                "tenant_id": str(tenant.id),
                "client_id": str(client_row.id),
                "scope": "openid profile",
                "issuer": "https://issuer.example.test/updated",
                "claims": {"sub": f"user-{suffix}-updated"},
                "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=20)).isoformat(),
                "revoked_reason": "superseded",
            },
        )

        assert response.status_code == HTTPStatus.OK, response.text
        payload = response.json()
        assert payload["id"] == str(record.id)
        assert payload["token_hash"] == f"access-token-{suffix}-updated"
        assert payload["token_kind"] == "refresh"
        assert payload["active"] is False
        assert payload["revoked_reason"] == "superseded"


@pytest.mark.asyncio
async def test_client_clear_returns_jsonrpc_result_and_deletes_matching_rows(
    tmp_path,
    db_session: AsyncSession,
    test_db_engine,
) -> None:
    suffix = uuid4().hex[:8]
    tenant = await _create_isolated_tenant(db_session, suffix=suffix)
    client_row = await _create_isolated_client(db_session, tenant_id=tenant.id, suffix=suffix)

    async with _admin_client(tmp_path, db_session, test_db_engine) as (client, _deployment):
        payload = await _invoke_rpc(
            client,
            {"Authorization": "Bearer test-admin-key"},
            "Client.clear",
            {
                "client_secret_hash": client_row.client_secret_hash.decode(),
                "redirect_uris": client_row.redirect_uris,
                "tenant_id": str(tenant.id),
            },
        )

        assert "error" not in payload, payload
        assert payload["result"]["deleted"] == 1

        remaining = await db_session.scalar(select(Client).where(Client.id == client_row.id))
        assert remaining is None


@pytest.mark.asyncio
async def test_tenant_clear_returns_jsonrpc_result_and_deletes_matching_rows(
    tmp_path,
    db_session: AsyncSession,
    test_db_engine,
) -> None:
    suffix = uuid4().hex[:8]
    tenant = await _create_isolated_tenant(db_session, suffix=suffix)

    async with _admin_client(tmp_path, db_session, test_db_engine) as (client, _deployment):
        payload = await _invoke_rpc(
            client,
            {"Authorization": "Bearer test-admin-key"},
            "Tenant.clear",
            {
                "name": tenant.name,
                "email": tenant.email,
                "slug": tenant.slug,
            },
        )

        assert "error" not in payload, payload
        assert payload["jsonrpc"] == "2.0"
        assert isinstance(payload["result"]["deleted"], int)


@pytest.mark.asyncio
async def test_user_clear_returns_jsonrpc_result_and_deletes_matching_rows(
    tmp_path,
    db_session: AsyncSession,
    test_db_engine,
) -> None:
    suffix = uuid4().hex[:8]
    tenant = await _create_isolated_tenant(db_session, suffix=suffix)
    user = await _create_isolated_user(db_session, tenant_id=tenant.id, suffix=suffix)

    async with _admin_client(tmp_path, db_session, test_db_engine) as (client, _deployment):
        payload = await _invoke_rpc(
            client,
            {"Authorization": "Bearer test-admin-key"},
            "User.clear",
            {
                "username": user.username,
                "email": user.email,
                "tenant_id": str(tenant.id),
            },
        )

        assert "error" not in payload, payload
        assert payload["result"]["deleted"] == 1

        remaining = await db_session.scalar(select(User).where(User.id == user.id))
        assert remaining is None


@pytest.mark.asyncio
async def test_pushedauthorizationrequest_create_returns_jsonrpc_envelope(
    tmp_path,
    db_session: AsyncSession,
    test_db_engine,
) -> None:
    suffix = uuid4().hex[:8]
    tenant = await _create_isolated_tenant(db_session, suffix=suffix)
    client_row = await _create_isolated_client(db_session, tenant_id=tenant.id, suffix=suffix)

    async with _admin_client(tmp_path, db_session, test_db_engine) as (client, _deployment):
        request_uri = f"urn:ietf:params:oauth:request_uri:{uuid4()}"
        payload = await _invoke_rpc(
            client,
            {"Authorization": "Bearer test-admin-key"},
            "PushedAuthorizationRequest.create",
            {
                "request_uri": request_uri,
                "client_id": str(client_row.id),
                "tenant_id": str(tenant.id),
                "params": {"scope": "openid profile", "prompt": "consent"},
                "expires_in": 180,
                "expires_at": (datetime.now(timezone.utc) + timedelta(seconds=180)).isoformat(),
            },
        )

        assert payload["jsonrpc"] == "2.0"
        assert "error" not in payload, payload
        assert payload["result"]["request_uri"] == request_uri
        assert payload["result"]["client_id"] == str(client_row.id)
        assert payload["result"]["tenant_id"] == str(tenant.id)
