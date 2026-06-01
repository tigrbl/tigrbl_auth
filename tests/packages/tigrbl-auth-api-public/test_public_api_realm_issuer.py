from __future__ import annotations

import sys
from importlib import import_module
from pathlib import Path
from types import SimpleNamespace

import pytest
from httpx import ASGITransport, AsyncClient

from tigrbl_auth.config.deployment import DEFAULT_VALUES


ROOT = Path(__file__).resolve().parents[3]
PKG_SRC = ROOT / "pkgs" / "tigrbl-auth-api-public" / "src"
if str(PKG_SRC) not in sys.path:
    sys.path.insert(0, str(PKG_SRC))

build_app = import_module("tigrbl_auth_api_public").build_app


def _settings() -> SimpleNamespace:
    values = dict(DEFAULT_VALUES)
    values.update(
        deployment_profile="production",
        issuer="http://localhost:8013",
        protected_resource_identifier="http://localhost:8013/resource",
        require_tls=False,
    )
    return SimpleNamespace(**values)


@pytest.mark.asyncio
async def test_public_api_exposes_default_realm_discovery() -> None:
    public_app = build_app(_settings())

    async with AsyncClient(
        transport=ASGITransport(app=public_app), base_url="http://test"
    ) as client:
        response = await client.get("/realms/default/.well-known/openid-configuration")

    assert response.status_code == 200
    payload = response.json()
    assert payload["issuer"] == "http://localhost:8013/realms/default"
    assert payload["jwks_uri"] == "http://localhost:8013/realms/default/.well-known/jwks.json"
    assert payload["tigrbl_auth_signing_scope"] == "realm:default"
