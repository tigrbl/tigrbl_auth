from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4

import pytest

from tigrbl_identity_contracts.admin_tenants import TenantAdministrator
from tigrbl_identity_server.platform_tenant_administration import (
    build_tenant_administration_capability,
)


pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_tenant_list_returns_bootstrapped_public_tenant_on_sqlite(
    runtime_engine_factory,
):
    db_root = (Path.cwd() / ".tmp-test-env" / f"tenant-{uuid4().hex[:8]}").resolve()
    db_root.mkdir(parents=True, exist_ok=True)
    database_url = f"sqlite+aiosqlite:///{db_root / 'tenant.db'}"

    try:
        async with runtime_engine_factory(database_url) as engine:
            _, maker = engine.provider.ensure()
            async with maker() as db:
                capability = build_tenant_administration_capability(db)
                actor = TenantAdministrator(
                    actor_id="integration-test",
                    tenant_id="integration-test",
                    is_admin=True,
                    is_superuser=True,
                )
                result = (await capability.call("list_tenants", actor)).value
    finally:
        shutil.rmtree(db_root, ignore_errors=True)

    assert len(result) >= 1
    assert any(item.slug == "public" for item in result)
