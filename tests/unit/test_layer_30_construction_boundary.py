from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNTIME_SRC = (
    ROOT
    / "pkgs"
    / "30-storage-runtime"
    / "tigrbl-identity-storage-runtime"
    / "src"
    / "tigrbl_identity_storage_runtime"
)


def test_new_table_runtime_construction_surface_has_no_higher_layer_imports() -> None:
    files = (
        RUNTIME_SRC / "make.py",
        RUNTIME_SRC / "define.py",
        RUNTIME_SRC / "derive.py",
        RUNTIME_SRC / "factories.py",
        RUNTIME_SRC / "inventory.py",
    )
    forbidden_prefixes = (
        "tigrbl_auth_protocol_",
        "tigrbl_identity_runtime",
        "tigrbl_identity_server",
        "tigrbl_auth_api_",
    )

    for file in files:
        tree = ast.parse(file.read_text(encoding="utf-8"))
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)
        assert not any(
            module.startswith(forbidden_prefixes) for module in imports
        ), file
