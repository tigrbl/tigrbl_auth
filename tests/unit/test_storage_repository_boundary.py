from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]
for src in (ROOT / "pkgs").glob("*/src"):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)

from tigrbl_identity_storage import (  # noqa: E402
    InMemoryRepository,
    STORAGE_MATRIX,
    SqlAlchemyRepositoryAdapter,
    StorageConflictError,
    StorageDialect,
    StorageNotFoundError,
    StorageRecord,
    StorageStatus,
    assert_repository_port,
    build_migration_contract,
    dialect_for_dsn,
    matrix_entry_for_dialect,
)


@pytest.mark.unit
def test_storage_t0_public_surfaces_are_importable() -> None:
    repository = assert_repository_port(InMemoryRepository())
    record = StorageRecord(collection="principals", id="principal-1", tenant_id="tenant-a", payload={"subject": "user:1"})

    created = repository.create(record)

    assert created.id == "principal-1"
    assert dialect_for_dsn("sqlite+aiosqlite:///identity.db") == StorageDialect.SQLITE
    assert matrix_entry_for_dialect(StorageDialect.POSTGRESQL).supports_schema_namespace is True


@pytest.mark.unit
def test_storage_t1_repository_port_crud_and_tenant_isolation() -> None:
    repository = InMemoryRepository()
    repository.create(StorageRecord(collection="principals", id="principal-1", tenant_id="tenant-a", payload={"name": "A"}))

    updated = repository.update(
        "principals",
        "principal-1",
        tenant_id="tenant-a",
        payload={"name": "B"},
        expected_version=1,
    )
    listed = repository.list("principals", tenant_id="tenant-a")

    assert updated.version == 2
    assert updated.payload == {"name": "B"}
    assert listed == (updated,)
    with pytest.raises(StorageNotFoundError):
        repository.get("principals", "principal-1", tenant_id="tenant-b")
    with pytest.raises(StorageConflictError):
        repository.update("principals", "principal-1", tenant_id="tenant-a", payload={}, expected_version=1)


@dataclass
class FakeRow:
    collection: str
    id: str
    tenant_id: str
    payload: dict[str, Any]
    version: int
    status: StorageStatus
    created_at: str
    updated_at: str


class FakeModelFactory:
    @staticmethod
    def from_storage_record(record: StorageRecord) -> FakeRow:
        return FakeRow(
            collection=record.collection,
            id=record.id,
            tenant_id=record.tenant_id,
            payload=dict(record.payload),
            version=record.version,
            status=record.status,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )

    @staticmethod
    def to_storage_record(row: FakeRow) -> StorageRecord:
        return StorageRecord(
            collection=row.collection,
            id=row.id,
            tenant_id=row.tenant_id,
            payload=row.payload,
            version=row.version,
            status=row.status,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )


class FakeSession:
    def __init__(self) -> None:
        self.rows: dict[tuple[str, str], FakeRow] = {}
        self.commits = 0

    def add(self, row: FakeRow) -> None:
        self.rows[(row.collection, row.id)] = row

    def merge(self, row: FakeRow) -> None:
        self.rows[(row.collection, row.id)] = row

    def get(self, _model_factory: object, key: tuple[str, str]) -> FakeRow | None:
        return self.rows.get(key)

    def list(self, _model_factory: object, *, collection: str, tenant_id: str) -> list[FakeRow]:
        return [row for row in self.rows.values() if row.collection == collection and row.tenant_id == tenant_id]

    def commit(self) -> None:
        self.commits += 1


@pytest.mark.unit
def test_storage_t1_sqlalchemy_adapter_contract_uses_session_boundary() -> None:
    session = FakeSession()
    adapter = SqlAlchemyRepositoryAdapter(session, FakeModelFactory)
    record = StorageRecord(collection="clients", id="client-1", tenant_id="tenant-a", payload={"client_id": "web"})

    created = adapter.create(record)
    updated = adapter.update("clients", "client-1", tenant_id="tenant-a", payload={"client_id": "web-v2"}, expected_version=1)
    deleted = adapter.delete("clients", "client-1", tenant_id="tenant-a")

    assert created.payload["client_id"] == "web"
    assert updated.version == 2
    assert deleted.status == StorageStatus.DELETED
    assert session.commits == 3


@pytest.mark.unit
def test_storage_t1_migration_contract_and_sqlite_postgres_matrix() -> None:
    versions_dir = Path("pkgs/20-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/migrations/versions")
    contract = build_migration_contract(
        versions_dir=versions_dir,
        required_collections=("tenants", "users", "clients", "services", "service_keys"),
    )

    assert contract.latest_revision == "0011_delegation_grant_lifecycle_tables"
    assert contract.is_ordered is True
    assert len(contract.revisions) >= 9
    assert {entry.dialect for entry in STORAGE_MATRIX} == {StorageDialect.SQLITE, StorageDialect.POSTGRESQL}
    assert dialect_for_dsn("postgresql+asyncpg://example/identity") == StorageDialect.POSTGRESQL


@pytest.mark.unit
def test_storage_t2_delete_visibility_and_no_protocol_semantics() -> None:
    repository = InMemoryRepository()
    repository.create(StorageRecord(collection="tokens", id="token-1", tenant_id="tenant-a", payload={"value": "opaque"}))

    deleted = repository.delete("tokens", "token-1", tenant_id="tenant-a")

    assert deleted.status == StorageStatus.DELETED
    assert repository.list("tokens", tenant_id="tenant-a") == ()
    with pytest.raises(StorageNotFoundError):
        repository.get("tokens", "token-1", tenant_id="tenant-a")


@pytest.mark.unit
def test_storage_t2_public_boundary_has_no_protocol_imports() -> None:
    files = [
        Path("pkgs/20-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/__init__.py"),
        Path("pkgs/20-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/repository.py"),
        Path("pkgs/20-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/migration_contract.py"),
    ]
    forbidden = {
        "tigrbl_auth",
        "tigrbl_auth_protocol_oauth",
        "tigrbl_auth_protocol_oidc",
        "tigrbl_identity_server",
        "tigrbl_identity_runtime",
    }

    imports: set[str] = set()
    for file in files:
        tree = ast.parse(file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                imports.add(node.module.split(".")[0])

    assert imports.isdisjoint(forbidden)
