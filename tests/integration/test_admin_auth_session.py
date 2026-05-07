from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tigrbl_auth.api.app import build_app
from tigrbl_auth.config.deployment import DEFAULT_VALUES, resolve_deployment
from tigrbl_auth.crypto import hash_pw
from tigrbl_auth.db import get_db as legacy_get_db
from tigrbl_auth.framework import select
from tigrbl_auth.routers.surface import surface_api as legacy_surface_api
from tigrbl_auth.runtime.engine_resolver import (
    register_api_provider,
    resolve_api_provider,
    resolve_default_provider,
    set_default_provider,
)
from tigrbl_auth.services.admin_identity_bootstrap import ensure_default_superuser_async
from tigrbl_auth.tables import Tenant, User, get_db as tables_get_db
from tigrbl_auth.tables.engine import get_db as engine_get_db


pytestmark = pytest.mark.integration


def _settings(tmp_path: Path) -> SimpleNamespace:
    values = dict(DEFAULT_VALUES)
    values.update(
        deployment_profile="baseline",
        issuer="https://admin.example.test",
        protected_resource_identifier="https://admin.example.test/resource",
        require_tls=False,
        admin_api_key="test-admin-key",
        admin_api_key_dir=str(tmp_path),
        session_cookie_force_secure=False,
        bootstrap_admin_username="admin",
        bootstrap_admin_email="admin@example.test",
        bootstrap_admin_password="AdminPass123!",
        bootstrap_admin_force_password_change=True,
        admin_password_reset_debug_disclosure=True,
    )
    return SimpleNamespace(**values)


def _override_db(app: object, session: AsyncSession) -> None:
    def _dependency_override():
        return session

    for dependency in (legacy_get_db, tables_get_db, engine_get_db):
        app.router.dependency_overrides[dependency] = _dependency_override
        app.dependency_overrides[dependency] = _dependency_override


async def _ensure_runtime_tables(provider: object) -> None:
    setattr(legacy_surface_api, "_ddl_executed", False)
    initialize = getattr(legacy_surface_api, "initialize", None)
    if callable(initialize):
        await initialize()
    raw_engine, _ = provider.ensure()

    def _create_runtime_tables(sync_conn):
        from tigrbl_auth.tables import Base

        Base.metadata.create_all(bind=sync_conn, checkfirst=True)

    begin_ctx = raw_engine.begin()
    if hasattr(begin_ctx, "__aenter__"):
        async with begin_ctx as conn:
            await conn.run_sync(_create_runtime_tables)
    else:
        with begin_ctx as conn:
            _create_runtime_tables(conn)


@asynccontextmanager
async def _admin_client(tmp_path: Path, db_session: AsyncSession, test_db_engine):
    settings_obj = _settings(tmp_path)
    deployment = resolve_deployment(settings_obj, plugin_mode="mixed")
    app = build_app(settings_obj, deployment=deployment)
    provider = test_db_engine.provider
    original_legacy_surface = resolve_api_provider(legacy_surface_api)
    original_app = resolve_api_provider(app)
    original_default_provider = resolve_default_provider()
    register_api_provider(legacy_surface_api, provider)
    register_api_provider(app, provider)
    set_default_provider(provider)
    await _ensure_runtime_tables(provider)
    _override_db(app, db_session)
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url=deployment.issuer) as client:
            yield client, settings_obj
    finally:
        register_api_provider(legacy_surface_api, original_legacy_surface or provider)
        register_api_provider(app, original_app or provider)
        if original_default_provider is not None:
            set_default_provider(original_default_provider)
        setattr(legacy_surface_api, "_ddl_executed", False)


async def _seed_admin_user(db_session: AsyncSession, *, password: str = "AdminPass123!") -> User:
    tenant = Tenant(slug=f"admin-{uuid4().hex[:8]}", name="Admin Tenant", email="tenant@example.test")
    db_session.add(tenant)
    await db_session.commit()

    user = User(
        tenant_id=tenant.id,
        username="admin-user",
        email="admin-user@example.test",
        password_hash=hash_pw(password),
        is_admin=True,
        is_superuser=True,
        must_change_password=False,
    )
    db_session.add(user)
    await db_session.commit()
    return user


@pytest.mark.asyncio
async def test_admin_auth_login_sets_session_cookie_and_resolves_session(tmp_path, db_session: AsyncSession, test_db_engine) -> None:
    await _seed_admin_user(db_session)
    async with _admin_client(tmp_path, db_session, test_db_engine) as (client, _settings_obj):
        login = await client.post("/admin/auth/login", json={"identifier": "admin-user", "password": "AdminPass123!"})
        assert login.status_code == 200, login.text
        assert login.json()["authenticated"] is True
        assert login.json()["is_admin"] is True
        assert "set-cookie" in login.headers

        session = await client.get("/admin/auth/session")
        assert session.status_code == 200, session.text
        payload = session.json()
        assert payload["authenticated"] is True
        assert payload["username"] == "admin-user"
        assert payload["is_superuser"] is True


@pytest.mark.asyncio
async def test_admin_auth_forgot_reset_and_change_password_flow(tmp_path, db_session: AsyncSession, test_db_engine) -> None:
    await _seed_admin_user(db_session)
    async with _admin_client(tmp_path, db_session, test_db_engine) as (client, _settings_obj):
        forgot = await client.post("/admin/auth/forgot-password", json={"identifier": "admin-user"})
        assert forgot.status_code == 200, forgot.text
        token = forgot.json()["debug_reset_token"]
        assert token

        reset = await client.post("/admin/auth/reset-password", json={"token": token, "password": "NewAdminPass123!"})
        assert reset.status_code == 200, reset.text

        login = await client.post("/admin/auth/login", json={"identifier": "admin-user", "password": "NewAdminPass123!"})
        assert login.status_code == 200, login.text

        change = await client.post(
            "/admin/auth/change-password",
            json={"current_password": "NewAdminPass123!", "new_password": "RotatedAdminPass123!"},
        )
        assert change.status_code == 200, change.text
        assert change.json()["must_change_password"] is False

        logout = await client.post("/admin/auth/logout", json={})
        assert logout.status_code == 200, logout.text

        relogin = await client.post("/admin/auth/login", json={"identifier": "admin-user", "password": "RotatedAdminPass123!"})
        assert relogin.status_code == 200, relogin.text


@pytest.mark.asyncio
async def test_default_superuser_bootstrap_materializes_admin_identity(tmp_path, db_session: AsyncSession, test_db_engine) -> None:
    async with _admin_client(tmp_path, db_session, test_db_engine) as (_client, settings_obj):
        details = await ensure_default_superuser_async(settings_obj)
        assert details is not None
        assert details["username"] == "admin"

        tenant = await db_session.scalar(select(Tenant).where(Tenant.slug == "public"))
        assert tenant is not None
        user = await db_session.scalar(select(User).where(User.username == "admin"))
        assert user is not None
        assert user.is_admin is True
        assert user.is_superuser is True
        assert user.must_change_password is True


@pytest.mark.asyncio
async def test_superuser_can_onboard_admin_identities(tmp_path, db_session: AsyncSession, test_db_engine) -> None:
    async with _admin_client(tmp_path, db_session, test_db_engine) as (client, settings_obj):
        await ensure_default_superuser_async(settings_obj)

        login = await client.post("/admin/auth/login", json={"identifier": "admin", "password": "AdminPass123!"})
        assert login.status_code == 200, login.text

        create = await client.post(
            "/admin/identities",
            json={
                "tenant_id": str((await db_session.scalar(select(Tenant).where(Tenant.slug == "public"))).id),
                "username": "ops-admin",
                "email": "ops-admin@example.test",
                "password": "TempAdminPass123!",
                "is_admin": True,
                "must_change_password": True,
            },
        )
        assert create.status_code == 200, create.text
        created = create.json()
        assert created["username"] == "ops-admin"
        assert created["is_admin"] is True
        assert created["must_change_password"] is True

        listing = await client.get(f"/admin/identities?tenant_id={created['tenant_id']}")
        assert listing.status_code == 200, listing.text
        payload = listing.json()
        assert any(item["email"] == "ops-admin@example.test" for item in payload)

        update = await client.patch(
            f"/admin/identities/{created['id']}",
            json={"is_active": False, "must_change_password": False},
        )
        assert update.status_code == 200, update.text
        assert update.json()["is_active"] is False
        assert update.json()["must_change_password"] is False
