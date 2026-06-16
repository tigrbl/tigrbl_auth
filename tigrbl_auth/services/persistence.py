"""Compatibility facade for canonical identity storage persistence helpers."""

from contextlib import asynccontextmanager

from tigrbl_auth._identity_storage import ensure_identity_storage_importable
from tigrbl_auth.runtime.engine_resolver import resolve_api_provider
from tigrbl_auth.tables.engine import ENGINE

ensure_identity_storage_importable()

from tigrbl_identity_storage.persistence import *  # noqa: F403
from tigrbl_identity_storage.persistence import __all__ as _storage_all


def _resolve_provider():
    try:
        from tigrbl_auth.api.surfaces import surface_api

        provider = resolve_api_provider(surface_api)
        if provider is not None:
            return provider
    except Exception:
        pass
    return ENGINE.provider


@asynccontextmanager
async def _session():
    provider = _resolve_provider()
    _, maker = provider.ensure()
    async with maker() as session:
        yield session


__all__ = [*_storage_all, "_session"]
