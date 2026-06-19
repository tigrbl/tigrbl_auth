from __future__ import annotations

from typing import Any

from .compat import LazyCompatEntrypoint, resolve_entrypoint, warn_legacy_import

warn_legacy_import("tigrbl_auth.gateway", stacklevel=2)

app = LazyCompatEntrypoint("gateway_app")


def build_app(*args: Any, **kwargs: Any) -> Any:
    return resolve_entrypoint("build_app")(*args, **kwargs)


def build_gateway(*args: Any, **kwargs: Any) -> Any:
    return resolve_entrypoint("build_gateway")(*args, **kwargs)


def build_gateway_runtime_plan(*args: Any, **kwargs: Any) -> Any:
    return resolve_entrypoint("build_gateway_runtime_plan")(*args, **kwargs)


def resolve_gateway_deployment(*args: Any, **kwargs: Any) -> Any:
    return resolve_entrypoint("resolve_gateway_deployment")(*args, **kwargs)

__all__ = [
    "app",
    "build_app",
    "build_gateway",
    "build_gateway_runtime_plan",
    "resolve_gateway_deployment",
]
