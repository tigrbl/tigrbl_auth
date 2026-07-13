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


def test_layer_30_has_no_repository_or_store_abstraction_modules() -> None:
    forbidden_suffixes = ("Repository", "Store", "UnitOfWork")
    for file in RUNTIME_SRC.rglob("*.py"):
        tree = ast.parse(file.read_text(encoding="utf-8"))
        class_names = {
            node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
        }
        assert not any(
            name.endswith(forbidden_suffixes) for name in class_names
        ), file

    for removed in (
        "repositories.py",
        "credential_repositories.py",
        "presentation_repositories.py",
        "attestation_repositories.py",
        "security_event_repositories.py",
        "workload_repositories.py",
        "replay_repository.py",
    ):
        assert not (RUNTIME_SRC / removed).exists()


def test_authorization_mutations_are_not_defined_by_layer_01_tables() -> None:
    storage_tables = (
        ROOT
        / "pkgs"
        / "01-storage"
        / "tigrbl-identity-storage"
        / "src"
        / "tigrbl_identity_storage"
        / "tables"
    )
    for relative in (
        Path("tenant_membership/_table.py"),
        Path("delegated_admin_scope/_table.py"),
        Path("attribute_policy/_table.py"),
    ):
        source = (storage_tables / relative).read_text(encoding="utf-8")
        tree = ast.parse(source)
        assert "op_ctx" not in source
        assert not any(
            isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef))
            for node in ast.walk(tree)
        )


def test_oidc_replay_mutation_is_not_defined_by_layer_01_table() -> None:
    table = (
        ROOT
        / "pkgs"
        / "01-storage"
        / "tigrbl-identity-storage"
        / "src"
        / "tigrbl_identity_storage"
        / "tables"
        / "backchannel_logout_replay"
        / "_table.py"
    )
    source = table.read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert "op_ctx" not in source
    assert not any(
        isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef))
        for node in ast.walk(tree)
    )


def test_oauth_state_mutations_are_not_defined_by_layer_01_tables() -> None:
    tables = (
        ROOT
        / "pkgs"
        / "01-storage"
        / "tigrbl-identity-storage"
        / "src"
        / "tigrbl_identity_storage"
        / "tables"
    )
    for relative in (
        Path("auth_code/_table.py"),
        Path("client_registration/_table.py"),
        Path("revoked_token/_table.py"),
    ):
        source = (tables / relative).read_text(encoding="utf-8")
        tree = ast.parse(source)
        assert "op_ctx" not in source
        assert not any(
            isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef))
            for node in ast.walk(tree)
        )
