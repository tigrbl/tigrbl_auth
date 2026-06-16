"""Compatibility loader for legacy CLI fragments."""

from __future__ import annotations

import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Iterable, MutableMapping


_SKIP_KEYS = {
    "__builtins__",
    "__cached__",
    "__doc__",
    "__loader__",
    "__name__",
    "__package__",
    "__spec__",
}


def load_fragments(
    namespace: MutableMapping[str, object],
    package_file: str,
    logical_filename: str,
    fragment_names: Iterable[str],
) -> None:
    package_path = Path(package_file).resolve()
    package_dir = package_path.parent
    logical_file = str(package_dir.parent / logical_filename)
    fragment_namespaces: list[MutableMapping[str, object]] = []
    namespace["__file__"] = logical_file

    for fragment_name in fragment_names:
        fragment_path = package_dir / f"{fragment_name}.py"
        fragment_module_name = f"{namespace.get('__name__', 'tigrbl_identity_cli.cli')}._loaded_{fragment_name}"
        spec = spec_from_file_location(fragment_module_name, fragment_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"cannot load CLI fragment {fragment_path}")
        module = module_from_spec(spec)
        for key, value in namespace.items():
            if key not in _SKIP_KEYS and key != "__file__":
                module.__dict__[key] = value
        sys.modules[fragment_module_name] = module
        spec.loader.exec_module(module)
        fragment_globals = module.__dict__
        fragment_globals["__file__"] = logical_file
        fragment_namespaces.append(fragment_globals)
        for key, value in fragment_globals.items():
            if key not in _SKIP_KEYS:
                namespace[key] = value
        namespace["__file__"] = logical_file
        for fragment_namespace in fragment_namespaces:
            fragment_namespace.update(namespace)
