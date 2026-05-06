from __future__ import annotations

import pytest

from tigrbl_auth.api.rpc.methods.directory import handle_tenant_list
from tigrbl_auth.api.rpc.schemas.directory import TenantListParams


pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_tenant_list_returns_bootstrapped_public_tenant_on_sqlite(runtime_engine_factory, tmp_path):
    database_url = f"sqlite+aiosqlite:///{tmp_path / 'tenant.db'}"

    async with runtime_engine_factory(database_url):
        result = await handle_tenant_list(TenantListParams(), None)

    assert result.count >= 1
    assert any(item.slug == "public" for item in result.items)
