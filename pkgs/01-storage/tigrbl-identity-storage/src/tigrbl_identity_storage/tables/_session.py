"""Storage-local database session resolution for table-owned helpers."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

from tigrbl_identity_runtime.engine_resolver import resolve_api_provider, resolve_default_provider
from tigrbl_identity_storage.tables.engine import ENGINE


def resolve_storage_provider() -> Any:
    for module_name, attr_name in (
        ("tigrbl_auth.api.surfaces", "surface_api"),
        ("tigrbl_auth.app", "app"),
    ):
        try:
            module = __import__(module_name, fromlist=[attr_name])
            api = getattr(module, attr_name)
            provider = resolve_api_provider(api)
            if provider is not None:
                return provider
        except Exception:
            pass
    try:
        provider = resolve_default_provider()
        if provider is not None:
            return provider
    except Exception:
        pass
    return ENGINE.provider


@asynccontextmanager
async def storage_session() -> AsyncIterator[Any]:
    provider = resolve_storage_provider()
    _, maker = provider.ensure()
    async with maker() as session:
        try:
            yield session
            commit = getattr(session, "commit", None)
            if callable(commit):
                result = commit()
                if hasattr(result, "__await__"):
                    await result
        except Exception:
            rollback = getattr(session, "rollback", None)
            if callable(rollback):
                result = rollback()
                if hasattr(result, "__await__"):
                    await result
            raise


__all__ = ["resolve_storage_provider", "storage_session"]
