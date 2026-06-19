from __future__ import annotations

from typing import Any

from .compat import LazyCompatEntrypoint, resolve_entrypoint, warn_legacy_import

warn_legacy_import("tigrbl_auth.plugin", stacklevel=2)

TigrblAuthPlugin = LazyCompatEntrypoint("TigrblAuthPlugin")


def install(*args: Any, **kwargs: Any) -> Any:
    return resolve_entrypoint("plugin_install")(*args, **kwargs)


__all__ = ["TigrblAuthPlugin", "install"]
