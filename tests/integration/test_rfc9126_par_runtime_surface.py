from __future__ import annotations

from http import HTTPStatus

import pytest

from tests.integration.test_profile_all_documented_endpoints import _profile_client


pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_hardening_mounts_and_executes_rfc9126_par_carrier(
    tmp_path,
    db_session,
    monkeypatch,
) -> None:
    async with _profile_client(
        "hardening",
        tmp_path,
        db_session,
        monkeypatch,
    ) as (client, deployment):
        openapi = (await client.get("/openapi.json")).json()
        response = await client.post("/par", data={})

    assert deployment.flag_enabled("enable_rfc9126")
    assert "/par" in openapi["paths"]
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "client_id parameter required" in response.text
