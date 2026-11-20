"""Compatibility helpers for the published Tigrbl engine-resolver surface.

These helpers keep the repository on Tigrbl's public API while insulating the
codebase from keyword/name drift between historical local assumptions
(`router=` / `register_router`) and the published resolver surface
(`api=` / `register_api`).
"""

from __future__ import annotations

from typing import Any


def _resolver():
    from tigrbl.engine import resolver as engine_resolver

    return engine_resolver


def resolve_api_provider(api: Any):
    """Resolve the provider bound to an API/router object.

    Prefer the published ``api=`` keyword while tolerating older local resolver
    surfaces that still exposed ``router=``.
    """

    engine_resolver = _resolver()
    try:
        return engine_resolver.resolve_provider(api=api)
    except TypeError:
        return engine_resolver.resolve_provider(router=api)


def resolve_default_provider():
    """Resolve the current default provider."""

    return _resolver().resolve_provider()


def register_api_provider(api: Any, ctx: Any) -> None:
    """Bind ``ctx`` to an API/router on the published resolver surface."""

    engine_resolver = _resolver()
    if hasattr(engine_resolver, "register_api"):
        engine_resolver.register_api(api, ctx)
        return
    engine_resolver.register_router(api, ctx)


def set_default_provider(ctx: Any) -> None:
    """Set the resolver default provider when the published surface supports it."""

    engine_resolver = _resolver()
    if hasattr(engine_resolver, "set_default"):
        engine_resolver.set_default(ctx)


__all__ = [
    "register_api_provider",
    "resolve_api_provider",
    "resolve_default_provider",
    "set_default_provider",
]
