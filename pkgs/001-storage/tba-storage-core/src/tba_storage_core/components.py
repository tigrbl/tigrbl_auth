"""Explicit full identity-storage composition used by the compatibility facade."""

from __future__ import annotations

from importlib.resources import files

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10
    import tomli as tomllib

from tigrbl_migrations import (
    StorageComposition,
    discover_components,
)
from tigrbl_migrations.version import require_supported_manifest_version


def _load_import_roots() -> tuple[str, ...]:
    profile = tomllib.loads(
        files(__package__).joinpath("storage.toml").read_text(encoding="utf-8")
    )
    require_supported_manifest_version(profile["manifest_version"])
    return tuple(profile["components"])


COMPONENT_IMPORT_ROOTS = _load_import_roots()


def load_full_composition():
    manifests, migrations = discover_components(COMPONENT_IMPORT_ROOTS)
    return StorageComposition.from_manifests(*manifests), migrations


__all__ = ["COMPONENT_IMPORT_ROOTS", "load_full_composition"]
