from __future__ import annotations

import ast
import importlib
from pathlib import Path

import pytest

from tigrbl_identity_storage import build_migration_contract
from tigrbl_identity_storage.tables import Client, Tenant, TokenRecord, User
from tigrbl_identity_storage.tables.engine import dsn


ROOT = Path(__file__).resolve().parents[2]
STORAGE_SRC = ROOT / "pkgs" / "20-storage" / "tigrbl-identity-storage" / "src" / "tigrbl_identity_storage"


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
        required_collections=("tenants", "users", "clients", "services", "service_keys"),
    )

    assert contract.latest_revision == "0014_optional_contract_state_tables"
    assert contract.is_ordered is True
    assert len(contract.revisions) >= 9
    assert dsn.startswith("sqlite")


@pytest.mark.unit
def test_storage_public_boundary_has_no_generic_repository_imports() -> None:
    files = [
        STORAGE_SRC / "__init__.py",
        STORAGE_SRC / "migration_contract.py",
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
