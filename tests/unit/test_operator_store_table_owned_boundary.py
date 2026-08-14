from __future__ import annotations

import importlib
from pathlib import Path

from sqlalchemy import create_engine

from tigrbl_identity_storage_operator.tables import OperatorRecord


ROOT = Path(__file__).resolve().parents[2]
STORAGE_ROOT = ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage"
RUNTIME_ROOT = (
    ROOT
    / "pkgs/30-storage-runtime/tigrbl-identity-storage-runtime/src/tigrbl_identity_storage_runtime"
)


def test_operator_store_has_no_legacy_sqlite_store_module() -> None:
    assert not (RUNTIME_ROOT / "_operator_store/sqlite_store.py").exists()


def test_operator_store_orchestration_does_not_own_sqlite_ddl_or_raw_dml() -> None:
    violations: list[str] = []
    for path in (RUNTIME_ROOT / "_operator_store").glob("*.py"):
        source = path.read_text(encoding="utf-8")
        for forbidden in ("import sqlite3", "CREATE TABLE", "INSERT INTO", "SELECT ", "DELETE FROM"):
            if forbidden in source:
                violations.append(f"{path}: contains {forbidden}")
    assert violations == []


def test_operator_store_tables_own_operator_record_surfaces() -> None:
    expected = {
        "operator_metadata.py": "OperatorMetadata",
        "operator_record.py": "OperatorRecord",
        "operator_transaction.py": "OperatorTransaction",
        "operator_audit_event.py": "OperatorAuditEvent",
        "operator_activity.py": "OperatorActivity",
    }
    for filename, symbol in expected.items():
        path = STORAGE_ROOT / "tables" / filename
        if not path.exists():
            path = STORAGE_ROOT / "tables" / filename.removesuffix(".py") / "_table.py"
        source = path.read_text(encoding="utf-8")
        assert f"class {symbol}" in source


def test_operator_migration_compiles_each_index_to_distinct_driver_sql(
    monkeypatch,
) -> None:
    migration = importlib.import_module(
        "tigrbl_identity_storage_operator.migrations.versions."
        "469839b2_d339_544a_b747_fd68b6a5f235_initial_schema"
    )
    engine = create_engine("sqlite+pysqlite:///:memory:")

    class RecordingConnection:
        dialect = engine.dialect

        def __init__(self) -> None:
            self.index_statements: list[str] = []

        def execute(self, _statement) -> None:
            return None

        def exec_driver_sql(self, statement: str) -> None:
            self.index_statements.append(statement)

    connection = RecordingConnection()
    monkeypatch.setattr(migration, "TABLE_MODELS", (OperatorRecord,))
    migration.upgrade(connection)

    assert len(connection.index_statements) == 4
    assert len(set(connection.index_statements)) == 4
    for column in ("record_id", "resource", "status", "tenant"):
        assert any(
            f"ix_operator_records_{column}" in statement
            and f"({column})" in statement
            for statement in connection.index_statements
        )
