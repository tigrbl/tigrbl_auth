from __future__ import annotations

import importlib.util
from pathlib import Path

from tigrbl import create_table_record, field_value, list_table_records


ROOT = Path(__file__).resolve().parents[2]


def test_layer30_common_adapter_is_removed() -> None:
    assert (
        importlib.util.find_spec("tigrbl_identity_storage_runtime.ops.common") is None
    )
    assert callable(create_table_record)
    assert callable(list_table_records)
    assert callable(field_value)


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
