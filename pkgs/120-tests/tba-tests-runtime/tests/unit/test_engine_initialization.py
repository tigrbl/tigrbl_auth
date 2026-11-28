import pytest
from sqlalchemy import text
from tba_app_backend_core.surfaces import surface_api
from tba_runtime_identity.engine_resolver import resolve_api_provider


@pytest.mark.unit
async def test_engine_initialization(db_session):
    provider = resolve_api_provider(surface_api)
    assert provider is not None
    result = await db_session.execute(text("PRAGMA foreign_keys"))
    assert result.scalar() == 1
