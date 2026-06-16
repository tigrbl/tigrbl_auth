from __future__ import annotations

from types import SimpleNamespace

import pytest
from httpx import ASGITransport, AsyncClient

from tigrbl_auth.api.app import build_app
from tigrbl_auth.config.deployment import resolve_deployment


def _settings(tmp_path) -> SimpleNamespace:
    return SimpleNamespace(admin_api_key="test-admin-key", admin_api_key_dir=str(tmp_path))


async def _json_payload(app, path: str) -> dict:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(path)
    assert response.status_code == 200
    return response.json()


async def _response_payload(app, path: str) -> tuple[int, dict]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(path)
    payload = response.json() if response.content else {}
    return response.status_code, payload


@pytest.mark.asyncio
async def test_admin_gate_defers_openapi_payload_to_upstream_for_public_runtime(tmp_path) -> None:
    deployment = resolve_deployment()
    wrapped = build_app(_settings(tmp_path), deployment=deployment)
    inner = wrapped.app

    assert await _json_payload(wrapped, "/openapi.json") == await _json_payload(inner, "/openapi.json")


@pytest.mark.asyncio
async def test_admin_gate_defers_openapi_payload_to_upstream_for_mixed_runtime(tmp_path) -> None:
    deployment = resolve_deployment(plugin_mode="mixed")
    wrapped = build_app(_settings(tmp_path), deployment=deployment)
    inner = wrapped.app

    assert await _json_payload(wrapped, "/openapi.json") == await _json_payload(inner, "/openapi.json")


@pytest.mark.asyncio
async def test_admin_gate_defers_openrpc_payload_to_upstream_for_public_runtime(tmp_path) -> None:
    deployment = resolve_deployment()
    wrapped = build_app(_settings(tmp_path), deployment=deployment)

    assert deployment.active_openrpc_methods == ()
    assert await _response_payload(wrapped, "/openrpc.json") == (404, {"detail": "Not Found"})


@pytest.mark.asyncio
async def test_admin_gate_defers_openrpc_payload_to_upstream_for_mixed_runtime(tmp_path) -> None:
    deployment = resolve_deployment(plugin_mode="mixed")
    wrapped = build_app(_settings(tmp_path), deployment=deployment)
    inner = wrapped.app

    assert await _json_payload(wrapped, "/openrpc.json") == await _json_payload(inner, "/openrpc.json")
