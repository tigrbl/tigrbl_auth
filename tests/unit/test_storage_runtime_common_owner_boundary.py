from __future__ import annotations

import importlib.util
from pathlib import Path

from tigrbl import create_table_record, field_value, list_table_records


ROOT = Path(__file__).resolve().parents[2]


def test_layer30_common_adapter_is_removed() -> None:
    assert (
        importlib.util.find_spec("tba_runtime_identity_storage.ops.common") is None
    )
    assert callable(create_table_record)
    assert callable(list_table_records)
    assert callable(field_value)


def test_runtime_and_server_do_not_import_layer01_private_ops() -> None:
    roots = (
        ROOT / "pkgs" / "30-storage-runtime" / "tba-runtime-identity-storage",
        ROOT / "pkgs" / "60-runtime" / "tba-server-identity",
    )
    offenders = []
    forbidden = "tba_storage_core.tables._ops"
    for root in roots:
        for path in root.rglob("*.py"):
            if forbidden in path.read_text(encoding="utf-8"):
                offenders.append(path.relative_to(ROOT).as_posix())
    assert offenders == []
