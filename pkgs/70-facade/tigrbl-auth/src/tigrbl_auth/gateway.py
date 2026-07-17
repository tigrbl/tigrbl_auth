from __future__ import annotations

from typing import Any

from .compat import resolve_entrypoint, warn_legacy_import

warn_legacy_import("tigrbl_auth.gateway", stacklevel=2)


def build_gateway_runtime_plan(*args: Any, **kwargs: Any) -> Any:
    return resolve_entrypoint("build_gateway_runtime_plan")(*args, **kwargs)


def resolve_gateway_deployment(*args: Any, **kwargs: Any) -> Any:
    return resolve_entrypoint("resolve_gateway_deployment")(*args, **kwargs)


__all__ = ["build_gateway_runtime_plan", "resolve_gateway_deployment"]
