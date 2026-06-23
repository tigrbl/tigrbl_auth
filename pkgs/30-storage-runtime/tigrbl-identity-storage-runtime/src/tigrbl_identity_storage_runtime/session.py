"""Runtime provider/session resolution for identity storage composition."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

from tigrbl_identity_storage.tables.engine import ENGINE


def _resolve_api_provider(api: Any) -> Any:
    from tigrbl.engine import resolver as engine_resolver

    try:
        return engine_resolver.resolve_provider(api=api)
    except TypeError:
        return engine_resolver.resolve_provider(router=api)


def _resolve_default_provider() -> Any:
    from tigrbl.engine import resolver as engine_resolver

    return engine_resolver.resolve_provider()


def resolve_storage_provider() -> Any:
    for module_name, attr_name in (
        ("tigrbl_auth.api.surfaces", "surface_api"),
        ("tigrbl_auth.app", "app"),
    ):
        try:
            module = __import__(module_name, fromlist=[attr_name])
            api = getattr(module, attr_name)
            provider = _resolve_api_provider(api)
            if provider is not None:
                return provider
        except Exception:
            pass
    try:
        provider = _resolve_default_provider()
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
