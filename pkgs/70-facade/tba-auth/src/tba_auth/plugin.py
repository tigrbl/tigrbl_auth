from __future__ import annotations

from typing import Any

from .compat import LazyCompatEntrypoint, resolve_entrypoint, warn_legacy_import

warn_legacy_import("tba_auth.plugin", stacklevel=2)

TbaPlugin = LazyCompatEntrypoint("TbaPlugin")


def install(*args: Any, **kwargs: Any) -> Any:
    return resolve_entrypoint("plugin_install")(*args, **kwargs)


__all__ = ["TbaPlugin", "install"]
