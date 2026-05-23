from __future__ import annotations

from typing import Any

from .compat import resolve_entrypoint, warn_legacy_import

warn_legacy_import("tigrbl_auth.cli", stacklevel=2)


def main(*args: Any, **kwargs: Any) -> Any:
    return resolve_entrypoint("cli_main")(*args, **kwargs)


__all__ = ["main"]
