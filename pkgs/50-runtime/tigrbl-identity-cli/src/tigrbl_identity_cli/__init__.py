"""Dedicated CLI package for Tigrbl identity workflows."""

from __future__ import annotations

import sys


def install_tomllib_alias() -> None:
    if sys.version_info >= (3, 11):
        return
    try:  # pragma: no cover - exercised on Python 3.10 CI lanes
        import tomllib as _tomllib  # noqa: F401
    except ModuleNotFoundError:
        try:
            import tomli as _tomllib  # type: ignore[no-redef]
        except ModuleNotFoundError:
            return
        sys.modules.setdefault("tomllib", _tomllib)


install_tomllib_alias()

__all__ = ["install_tomllib_alias"]
