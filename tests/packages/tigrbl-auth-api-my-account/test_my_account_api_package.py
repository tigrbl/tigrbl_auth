from __future__ import annotations

import sys
from importlib import import_module
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tigrbl_auth.config.deployment import DEFAULT_VALUES, resolve_deployment
from tigrbl_auth.crypto import hash_pw
from tigrbl_auth.orm import AuthSession, Client, Consent, Tenant, User

ROOT = Path(__file__).resolve().parents[3]
PKG_SRC = ROOT / "pkgs" / "tigrbl-auth-api-my-account" / "src"
if str(PKG_SRC) not in sys.path:
    sys.path.insert(0, str(PKG_SRC))

my_account_package = import_module("tigrbl_auth_api_my_account")
PRODUCT_SURFACE = my_account_package.PRODUCT_SURFACE
MY_ACCOUNT_API_CONTRACT = my_account_package.MY_ACCOUNT_API_CONTRACT
build_app = my_account_package.build_app

router_module = import_module("tigrbl_auth.api.rest.routers.my_account")


def _settings() -> SimpleNamespace:
    values = dict(DEFAULT_VALUES)
    values.update(
        deployment_profile="production",
        issuer="http://localhost:8019",
        protected_resource_identifier="http://localhost:8019/resource",
        require_tls=False,
        session_cookie_force_secure=False,
    )
    return SimpleNamespace(**values)


async def _tenant(db: AsyncSession, label: str) -> Tenant:
    suffix = uuid4().hex[:8]
    row = Tenant(
        slug=f"{label}-{suffix}",
        name=f"{label.title()} Tenant",
        email=f"{label}-{suffix}@example.test",
    )
    db.add(row)
    await db.commit()
    return row


async def _user(db: AsyncSession, tenant: Tenant, username: str) -> User:
    row = User(
        tenant_id=tenant.id,
        username=username,
        email=f"{username}@example.test",
        password_hash=hash_pw("CurrentPass123!"),
        is_active=True,
    )
    db.add(row)
    await db.commit()
    return row


async def _client(db: AsyncSession, tenant: Tenant) -> Client:
    row = Client.new(
        tenant_id=tenant.id,
        client_id=str(uuid4()),
        client_secret="client-secret",
        redirects=["https://client.example/callback"],
    )
    db.add(row)
    await db.commit()
    return row


def test_my_account_contract_matches_product_surface_registry() -> None:
    deployment = resolve_deployment(
        profile="production", product_surface=PRODUCT_SURFACE
    )

    assert PRODUCT_SURFACE == "my-account-api"
    assert MY_ACCOUNT_API_CONTRACT.product_surface == PRODUCT_SURFACE
    assert MY_ACCOUNT_API_CONTRACT.intended_uix == "@tigrbl-auth/my-account-uix"
    assert deployment.plugin_mode == "public-only"
    assert deployment.surface_enabled("public-rest")
    assert not deployment.surface_enabled("admin-rpc")
    assert deployment.active_openrpc_methods == ()
    for capability in MY_ACCOUNT_API_CONTRACT.baseline_capabilities:
        assert deployment.capability_enabled(capability), capability


def test_my_account_build_app_uses_environment_backed_default_settings() -> None:
    with patch.dict(
        "os.environ",
        {
            "AUTHN_ISSUER": "http://localhost:8019",
            "TIGRBL_AUTH_PROFILE": "production",
            "TIGRBL_AUTH_REQUIRE_TLS": "false",
        },
    ):
        built = build_app()

    assert built.deployment.issuer == "http://localhost:8019"
    assert built.deployment.product_surface == PRODUCT_SURFACE
    assert built.settings_obj.require_tls is False


@pytest.mark.asyncio
async def test_my_account_openapi_is_current_subject_only() -> None:
    my_account_app = build_app(_settings())

    async with AsyncClient(
        transport=ASGITransport(app=my_account_app), base_url="http://test"
    ) as client:
        openapi_response = await client.get("/openapi.json")
        anonymous = await client.get("/account/profile")
        rpc = await client.post("/rpc", json={})

    assert openapi_response.status_code == 200
    assert anonymous.status_code == 401
    assert rpc.status_code == 404
    paths = openapi_response.json()["paths"]
    assert "/account/profile" in paths
    assert "/account/sessions" in paths
    assert "/account/sessions/{session_id}" in paths
    assert "/account/authorized-apps" in paths
    assert "/account/authorized-apps/{client_id}" in paths
    assert "/account/consents" in paths
    assert "/account/consents/{consent_id}" in paths
    assert "/account/password/change" in paths
    for forbidden in (
        "/admin/tenant",
        "/admin/identity",
        "/tenant",
        "/user",
        "/client",
        "/service",
        "/authsession",
        "/login",
        "/authorize",
        "/token",
        "/register",
        "/introspect",
    ):
        assert forbidden not in paths
    for operation in paths["/account/profile"].values():
        assert operation["tags"] == ["My Account"]


@pytest.mark.asyncio
async def test_my_account_cors_allows_uix_origin_on_error_responses() -> None:
    my_account_app = build_app(_settings())

    async with AsyncClient(
        transport=ASGITransport(app=my_account_app), base_url="http://test"
    ) as client:
        preflight = await client.options(
            "/account/profile",
            headers={
                "origin": "http://localhost:3019",
                "access-control-request-method": "GET",
            },
        )
        anonymous = await client.get(
            "/account/profile",
            headers={"origin": "http://localhost:3019"},
        )

    assert preflight.status_code == 204
    assert preflight.headers["access-control-allow-origin"] == "http://localhost:3019"
    assert preflight.headers["access-control-allow-credentials"] == "true"
    assert anonymous.status_code == 401
    assert anonymous.headers["access-control-allow-origin"] == "http://localhost:3019"
    assert anonymous.headers["access-control-allow-credentials"] == "true"


@pytest.mark.asyncio
async def test_my_account_handlers_are_current_subject_scoped(
    db_session: AsyncSession,
) -> None:
    tenant = await _tenant(db_session, "my-account")
    alice = await _user(db_session, tenant, "alice-account")
    bob = await _user(db_session, tenant, "bob-account")
    client = await _client(db_session, tenant)
    alice_session = AuthSession(
        tenant_id=tenant.id,
        user_id=alice.id,
        username=alice.username,
        session_state="active",
    )
    bob_session = AuthSession(
        tenant_id=tenant.id,
        user_id=bob.id,
        username=bob.username,
        session_state="active",
    )
    alice_consent = Consent(
        tenant_id=tenant.id,
        user_id=alice.id,
        client_id=client.id,
        scope="openid profile",
        state="active",
    )
    bob_consent = Consent(
        tenant_id=tenant.id,
        user_id=bob.id,
        client_id=client.id,
        scope="openid email",
        state="active",
    )
    db_session.add_all([alice_session, bob_session, alice_consent, bob_consent])
    await db_session.commit()

    profile = await router_module.get_account_profile(
        current_user=alice,
        db=db_session,
    )
    sessions = await router_module.list_account_sessions(
        current_user=alice,
        db=db_session,
    )
    consents = await router_module.list_account_consents(
        current_user=alice,
        db=db_session,
    )
    apps = await router_module.list_account_authorized_apps(
        current_user=alice,
        db=db_session,
    )

    assert profile.id == str(alice.id)
    assert {item.id for item in sessions} == {str(alice_session.id)}
    assert {item.id for item in consents} == {str(alice_consent.id)}
    assert {item.client_id for item in apps} == {str(client.id)}

    with pytest.raises(Exception) as missing_session:
        await router_module.revoke_account_session(
            str(bob_session.id),
            current_user=alice,
            db=db_session,
        )
    assert getattr(missing_session.value, "status_code", None) == 404

    with pytest.raises(Exception) as missing_consent:
        await router_module.revoke_account_consent(
            str(bob_consent.id),
            current_user=alice,
            db=db_session,
        )
    assert getattr(missing_consent.value, "status_code", None) == 404

    revoked = await router_module.revoke_account_session(
        str(alice_session.id),
        current_user=alice,
        db=db_session,
    )
    revoked_consent = await router_module.revoke_account_consent(
        str(alice_consent.id),
        current_user=alice,
        db=db_session,
    )

    assert revoked.status == "revoked"
    assert revoked_consent.status == "revoked"
