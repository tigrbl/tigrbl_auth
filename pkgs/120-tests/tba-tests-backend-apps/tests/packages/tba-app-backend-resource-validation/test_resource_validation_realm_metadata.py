from __future__ import annotations

from importlib import import_module
from types import SimpleNamespace

import pytest
from httpx import ASGITransport, AsyncClient

from tba_auth.config.deployment import DEFAULT_VALUES


build_app = import_module("tba_app_backend_resource_validation").build_app


def _settings() -> SimpleNamespace:
    values = dict(DEFAULT_VALUES)
    values.update(
        deployment_profile="production",
        issuer="http://localhost:8014",
        protected_resource_identifier="http://localhost:8014/resource",
        require_tls=False,
    )
    return SimpleNamespace(**values)


@pytest.mark.asyncio
async def test_resource_validation_exposes_realm_metadata() -> None:
    app = build_app(_settings())

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/realms/default/.well-known/openid-configuration")

    assert response.status_code == 200
    assert response.json()["issuer"] == "http://localhost:8014/realms/default"
