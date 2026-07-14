from __future__ import annotations

import ast
import importlib
from pathlib import Path

import pytest

from tigrbl_identity_storage import build_migration_contract
from tigrbl_identity_storage.tables import Client, Tenant, TokenRecord, User
from tigrbl_identity_storage_runtime.engine import dsn


ROOT = Path(__file__).resolve().parents[2]
STORAGE_SRC = ROOT / "pkgs" / "01-storage" / "tigrbl-identity-storage" / "src" / "tigrbl_identity_storage"


@pytest.mark.unit
def test_storage_generic_repository_surface_is_removed() -> None:
    assert not (STORAGE_SRC / "repository.py").exists()

    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("tigrbl_identity_storage.repository")


@pytest.mark.unit
def test_storage_public_root_exports_migrations_not_repository_abstractions() -> None:
    package = importlib.import_module("tigrbl_identity_storage")
    removed_names = {
        "InMemoryRepository",
        "RepositoryPort",
        "SqlAlchemyRepositoryAdapter",
        "StorageRecord",
        "StorageDialect",
        "STORAGE_MATRIX",
    }

    assert removed_names.isdisjoint(set(package.__all__))
    assert hasattr(package, "build_migration_contract")


@pytest.mark.unit
def test_storage_tables_are_the_canonical_storage_surface() -> None:
    for model in (Tenant, User, Client, TokenRecord):
        assert getattr(model, "__table__", None) is not None
        assert getattr(model, "handlers", None) is not None
        assert getattr(model, "schemas", None) is not None


@pytest.mark.unit
def test_storage_migration_contract_uses_tigrbl_owned_tables() -> None:
    versions_dir = STORAGE_SRC / "migrations" / "versions"
    contract = build_migration_contract(
        versions_dir=versions_dir,
        required_collections=(
            "tenants",
            "users",
            "clients",
            "service_identities",
            "credential_service_keys",
        ),
    )

    expected_latest = sorted(path.stem for path in versions_dir.glob("[0-9][0-9][0-9][0-9]_*.py"))[-1]
    assert contract.latest_revision == expected_latest
    assert contract.is_ordered is True
    assert len(contract.revisions) >= 9
    assert dsn.startswith("sqlite")


@pytest.mark.unit
def test_storage_public_boundary_has_no_generic_repository_imports() -> None:
    assert not (STORAGE_SRC / "migration_contract.py").exists()
    assert (STORAGE_SRC / "migrations" / "contract.py").exists()

    files = [
        STORAGE_SRC / "__init__.py",
        STORAGE_SRC / "migrations" / "contract.py",
        STORAGE_SRC / "migrations" / "__init__.py",
        STORAGE_SRC / "tables" / "__init__.py",
    ]
    forbidden_modules = {"tigrbl_identity_storage.repository"}
    forbidden_names = {
        "InMemoryRepository",
        "RepositoryPort",
        "SqlAlchemyRepositoryAdapter",
        "StorageRecord",
    }

    imports: set[str] = set()
    names: set[str] = set()
    for file in files:
        tree = ast.parse(file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                imports.add(node.module)
                names.update(alias.name for alias in node.names)

    assert imports.isdisjoint(forbidden_modules)
    assert names.isdisjoint(forbidden_names)


@pytest.mark.unit
def test_engine_and_session_execution_are_runtime_owned() -> None:
    storage_engine = STORAGE_SRC / "tables" / "engine.py"
    runtime_root = (
        ROOT
        / "pkgs"
        / "30-storage-runtime"
        / "tigrbl-identity-storage-runtime"
        / "src"
        / "tigrbl_identity_storage_runtime"
    )

    runtime_engine_source = (runtime_root / "engine.py").read_text(encoding="utf-8")
    runtime_session_source = (runtime_root / "session.py").read_text(encoding="utf-8")

    assert not storage_engine.exists()
    assert not (STORAGE_SRC / "db.py").exists()
    assert "build_engine(" in runtime_engine_source
    assert "asynccontextmanager" in runtime_session_source


@pytest.mark.unit
def test_storage_framework_is_schema_only_and_generic_ops_are_removed() -> None:
    framework_source = (STORAGE_SRC / "framework.py").read_text(encoding="utf-8")
    forbidden = {
        "TigrblApp",
        "TigrblRouter",
        "hook_ctx",
        "op_ctx",
        "build_engine",
        "storage_session",
        "HTTPException",
    }

    assert not (STORAGE_SRC / "tables" / "_ops.py").exists()
    assert not (STORAGE_SRC / "tables" / "_sync.py").exists()
    assert not (STORAGE_SRC / "tables" / "_security_ctx.py").exists()
    assert all(name not in framework_source for name in forbidden)
