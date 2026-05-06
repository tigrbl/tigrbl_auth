from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4

import pytest

from tigrbl_auth.api.rpc.methods.directory import handle_tenant_list
from tigrbl_auth.api.rpc.schemas.directory import TenantListParams


pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_tenant_list_returns_bootstrapped_public_tenant_on_sqlite(runtime_engine_factory):
    db_root = (Path.cwd() / ".tmp-test-env" / f"tenant-{uuid4().hex[:8]}").resolve()
    db_root.mkdir(parents=True, exist_ok=True)
    database_url = f"sqlite+aiosqlite:///{db_root / 'tenant.db'}"

    try:
        async with runtime_engine_factory(database_url):
            result = await handle_tenant_list(TenantListParams(), None)
    finally:
        shutil.rmtree(db_root, ignore_errors=True)

    assert result.count >= 1
    assert any(item.slug == "public" for item in result.items)
