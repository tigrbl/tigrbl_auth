from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from tigrbl_auth.crypto import hash_pw
from tigrbl_auth.framework import select
from tigrbl_auth.services.persistence import (
    append_audit_event_async,
    create_session_async,
    get_token_record_async,
    get_active_session_async,
    get_client_registration_async,
    get_latest_logout_for_session_async,
    get_session_async,
    introspect_token_async,
    is_token_revoked_async,
    mark_logout_channel_async,
    record_consent_async,
    revoke_consent_async,
    revoke_token_async,
    rotate_session_cookie_secret_async,
    terminate_session_async,
    touch_session_async,
    upsert_client_registration_async,
    upsert_token_record_async,
)
from tigrbl_auth.services.token_service import (
    JWTCoder,
    RefreshTokenReuseError,
    issue_persisted_token_pair,
    redeem_refresh_token,
)
from tigrbl_auth.tables import AuditEvent, Client, Consent, Tenant, User


pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def _identity_triplet(db_session):
    suffix = uuid4().hex[:8]
    tenant = Tenant(slug=f"tenant-{suffix}", name=f"Tenant {suffix}", email=f"tenant-{suffix}@example.com")
    db_session.add(tenant)
    await db_session.commit()

    user = User(
        tenant_id=tenant.id,
        username=f"user-{suffix}",
        email=f"user-{suffix}@example.com",
        password_hash=hash_pw("SecretPass123!"),
    )
    db_session.add(user)
    await db_session.commit()

    client = Client.new(
        tenant_id=tenant.id,
        client_id=str(uuid4()),
        client_secret="super-secret",
        redirects=["https://client.example/callback"],
    )
    db_session.add(client)
    await db_session.commit()
    return tenant, user, client


async def test_token_revocation_and_introspection_state_is_durable(db_session):
    tenant, user, client = await _identity_triplet(db_session)
    now = datetime.now(timezone.utc)
    token = "capability-durable-access-token"
    claims = {
        "sub": str(user.id),
        "tid": str(tenant.id),
        "client_id": str(client.id),
        "scope": "openid profile",
        "iss": "https://issuer.example",
        "aud": ["api://default"],
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=30)).timestamp()),
    }

    digest = await upsert_token_record_async(token, claims, token_kind="access", token_type_hint="access_token")
    assert digest

    active_payload = await introspect_token_async(token)
    assert active_payload["active"] is True
    assert active_payload["sub"] == str(user.id)

    await revoke_token_async(token, token_type_hint="access_token", reason="capability-durability")
    assert await is_token_revoked_async(token) is True

    inactive_payload = await introspect_token_async(token)
    assert inactive_payload == {"active": False}


async def test_session_logout_consent_and_audit_roundtrip_is_durable(db_session):
    tenant, user, client = await _identity_triplet(db_session)

    session = await create_session_async(
        user_id=user.id,
        tenant_id=tenant.id,
        username=user.username,
        client_id=client.id,
        cookie_secret_hash="cookie-hash-1",
        session_state_salt="salt-1",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    assert session.id is not None

    await touch_session_async(session.id)
    await rotate_session_cookie_secret_async(session.id, cookie_secret_hash="cookie-hash-2")
    persisted_session = await get_session_async(session.id)
    assert persisted_session is not None
    assert persisted_session.cookie_secret_hash == "cookie-hash-2"

    consent = await record_consent_async(
        user_id=user.id,
        tenant_id=tenant.id,
        client_id=client.id,
        scope="openid profile email",
        claims={"essential": ["email"]},
        expires_at=datetime.now(timezone.utc) + timedelta(days=1),
    )
    revoked = await revoke_consent_async(consent.id)
    assert revoked is not None
    assert revoked.state == "revoked"

    logout = await terminate_session_async(
        session.id,
        initiated_by="rp_logout",
        reason="capability-test",
        frontchannel_required=True,
        backchannel_required=True,
        metadata={"source": "capability"},
    )
    assert logout is not None
    assert logout.status == "pending"

    await mark_logout_channel_async(logout.id, channel="frontchannel")
    await mark_logout_channel_async(logout.id, channel="backchannel")
    latest_logout = await get_latest_logout_for_session_async(session.id)
    assert latest_logout is not None
    assert latest_logout.status == "complete"

    active_session = await get_active_session_async(session.id)
    assert active_session is None

    event = await append_audit_event_async(
        tenant_id=tenant.id,
        actor_user_id=user.id,
        actor_client_id=client.id,
        session_id=session.id,
        event_type="session.logout",
        target_type="session",
        target_id=str(session.id),
        details={"logout_id": str(logout.id)},
    )
    assert event.id is not None

    db_session.expire_all()
    saved_consent = await db_session.scalar(select(Consent).where(Consent.id == consent.id))
    saved_audit = await db_session.scalar(select(AuditEvent).where(AuditEvent.id == event.id))
    assert saved_consent is not None and saved_consent.state == "revoked"
    assert saved_audit is not None and saved_audit.event_type == "session.logout"


async def test_client_registration_metadata_roundtrip_is_durable(db_session):
    tenant, _, client = await _identity_triplet(db_session)

    registration = await upsert_client_registration_async(
        client_id=client.id,
        tenant_id=tenant.id,
        metadata={
            "redirect_uris": ["https://client.example/callback"],
            "token_endpoint_auth_method": "client_secret_basic",
            "frontchannel_logout_uri": "https://client.example/frontchannel-logout",
        },
        contacts=["ops@example.com"],
        software_id="capability-client",
        software_version="9.0",
        registration_access_token_hash="rat-hash",
        registration_client_uri="https://issuer.example/register/" + str(client.id),
    )
    assert registration.client_id == client.id

    persisted = await get_client_registration_async(client.id)
    assert persisted is not None
    assert persisted.software_id == "capability-client"
    assert persisted.registration_metadata["token_endpoint_auth_method"] == "client_secret_basic"


async def test_refresh_token_rotation_and_reuse_rejection_is_durable(db_session, test_db_engine):
    tenant, user, client = await _identity_triplet(db_session)
    jwt = JWTCoder.default()

    _, refresh_token = await issue_persisted_token_pair(
        jwt=jwt,
        sub=str(user.id),
        tid=str(tenant.id),
        client_id=str(client.id),
        issuer="https://issuer.example",
        audience="api://default",
        scope="openid profile",
    )

    rotated = await redeem_refresh_token(
        jwt=jwt,
        refresh_token=refresh_token,
        client_id=str(client.id),
    )
    assert rotated["refresh_token"] != refresh_token

    original = await get_token_record_async(refresh_token)
    successor = await get_token_record_async(rotated["refresh_token"])
    assert original is not None and original.used_at is not None
    assert successor is not None
    assert successor.refresh_parent_hash == original.token_hash
    assert successor.refresh_family_id == original.refresh_family_id

    with pytest.raises(RefreshTokenReuseError):
        await redeem_refresh_token(
            jwt=jwt,
            refresh_token=refresh_token,
            client_id=str(client.id),
        )

    replayed = await get_token_record_async(refresh_token)
    successor_after_replay = await get_token_record_async(rotated["refresh_token"])
    assert replayed is not None and replayed.reuse_detected_at is not None
    assert successor_after_replay is not None
    assert successor_after_replay.revoked_reason == "refresh_token_reuse_detected"

    raw_engine, _ = test_db_engine.provider.ensure()
    dispose_result = raw_engine.dispose()
    if hasattr(dispose_result, "__await__"):
        await dispose_result
