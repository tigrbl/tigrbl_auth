from __future__ import annotations

from typing import Any

from .compat import LazyCompatEntrypoint, resolve_entrypoint, warn_legacy_import

warn_legacy_import("tigrbl_auth.app", stacklevel=2)

app = LazyCompatEntrypoint("app")


def build_app(*args: Any, **kwargs: Any) -> Any:
    return resolve_entrypoint("build_app")(*args, **kwargs)


def build_application_runtime_plan(*args: Any, **kwargs: Any) -> Any:
    return resolve_entrypoint("build_application_runtime_plan")(*args, **kwargs)


__all__ = ["app", "build_app", "build_application_runtime_plan"]
