from __future__ import annotations

from typing import Any

from .compat import resolve_entrypoint, warn_legacy_import

warn_legacy_import("tigrbl_auth.app", stacklevel=2)


def build_application_runtime_plan(*args: Any, **kwargs: Any) -> Any:
    return resolve_entrypoint("build_application_runtime_plan")(*args, **kwargs)


__all__ = ["build_application_runtime_plan"]
