from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STORE_ROOT = ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage"


def test_operator_store_has_no_legacy_sqlite_store_module() -> None:
    assert not (STORE_ROOT / "_operator_store/sqlite_store.py").exists()


def test_operator_store_orchestration_does_not_own_sqlite_ddl_or_raw_dml() -> None:
    violations: list[str] = []
    for path in (STORE_ROOT / "_operator_store").glob("*.py"):
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
        source = (STORE_ROOT / "tables" / filename).read_text(encoding="utf-8")
        assert f"class {symbol}" in source
