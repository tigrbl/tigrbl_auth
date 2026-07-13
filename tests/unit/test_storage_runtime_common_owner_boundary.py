from __future__ import annotations

from pathlib import Path

from tigrbl_identity_storage_runtime.ops import common


ROOT = Path(__file__).resolve().parents[2]


def test_layer30_common_adapter_preserves_helper_call_shapes() -> None:
    assert common.create_record is common.create_table_record
    assert common.read_record is common.read_table_record
    assert common.update_record is common.update_table_record
    assert common.delete_record is common.delete_table_record
    assert common.list_records is common.list_table_records
    assert common.first_record is common.first_table_record
    assert common.field is common.field_value
    assert common.record_id is common.record_identifier


def test_runtime_and_server_do_not_import_layer01_private_ops() -> None:
    roots = (
        ROOT / "pkgs" / "30-storage-runtime" / "tigrbl-identity-storage-runtime",
        ROOT / "pkgs" / "60-runtime" / "tigrbl-identity-server",
    )
    offenders = []
    forbidden = "tigrbl_identity_storage.tables._ops"
    for root in roots:
        for path in root.rglob("*.py"):
            if forbidden in path.read_text(encoding="utf-8"):
                offenders.append(path.relative_to(ROOT).as_posix())
    assert offenders == []
