"""Shared HTTP and JSON-RPC setup for administration tests."""

from __future__ import annotations

from contextlib import asynccontextmanager
from http import HTTPStatus
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from tba_app_backend_core import build_app
from tba_app_backend_core.surfaces import AdminRouter
from tba_app_backend_core.surfaces import surface_api as composed_surface_api
from tba_auth.config.deployment import DEFAULT_VALUES, resolve_deployment
from tba_auth.db import get_db as legacy_get_db
from tba_auth.runtime.engine_resolver import (
    register_api_provider,
    resolve_api_provider,
    resolve_default_provider,
    set_default_provider,
)
from tba_auth.tables import RestOltpTable
from tba_auth.tables.engine import get_db as engine_get_db
from tba_runtime_identity_storage.engine import get_db as tables_get_db


def _settings(tmp_path: Path) -> SimpleNamespace:
    values = dict(DEFAULT_VALUES)
    values.update(
        deployment_profile="baseline",
        issuer="https://admin.example.test",
        protected_resource_identifier="https://admin.example.test/resource",
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


async def _ensure_runtime_tables(provider: Any) -> None:
    setattr(AdminRouter, "_ddl_executed", False)
    initialize = getattr(AdminRouter, "initialize", None)
    if callable(initialize):
        await initialize()
    raw_engine, _ = provider.ensure()

    def _create_runtime_tables(sync_conn):
        RestOltpTable.metadata.create_all(bind=sync_conn, checkfirst=True)

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
    original_admin_router = resolve_api_provider(AdminRouter)
    original_composed_surface = resolve_api_provider(composed_surface_api)
    original_app = resolve_api_provider(app)
    original_default_provider = resolve_default_provider()
    register_api_provider(AdminRouter, provider)
    register_api_provider(composed_surface_api, provider)
    register_api_provider(app, provider)
    set_default_provider(provider)
    await _ensure_runtime_tables(provider)
    _override_db(app, db_session)
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url=deployment.issuer
        ) as client:
            yield client, deployment
    finally:
        register_api_provider(AdminRouter, original_admin_router or provider)
        register_api_provider(
            composed_surface_api, original_composed_surface or provider
        )
        register_api_provider(app, original_app or provider)
        if original_default_provider is not None:
            set_default_provider(original_default_provider)
        setattr(AdminRouter, "_ddl_executed", False)


async def _invoke_rpc(
    client: AsyncClient,
    headers: dict[str, str],
    method_name: str,
    params: dict[str, Any],
) -> dict[str, Any]:
    response = await client.post(
        "/rpc",
        headers=headers,
        json={
            "jsonrpc": "2.0",
            "method": method_name,
            "params": params,
            "id": method_name,
        },
    )
    if response.status_code == HTTPStatus.NO_CONTENT and not response.text:
        return {"jsonrpc": "2.0", "result": None, "id": method_name}
    assert response.status_code == HTTPStatus.OK, response.text
    payload = response.json()
    assert payload["jsonrpc"] == "2.0"
    return payload
