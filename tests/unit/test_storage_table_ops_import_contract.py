from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FACADE_DIR = ROOT / "pkgs" / "tigrbl-auth" / "src" / "tigrbl_auth"
STORAGE_DIR = ROOT / "pkgs" / "tigrbl-identity-storage" / "src" / "tigrbl_identity_storage"


def test_orm_export_paths_are_not_supported_for_storage_ops() -> None:
    assert not (FACADE_DIR / "orm").exists()
    assert not (STORAGE_DIR / "orm").exists()


def test_storage_package_exports_tables_not_orm_facades() -> None:
    tables_init = STORAGE_DIR / "tables" / "__init__.py"
    source = tables_init.read_text(encoding="utf-8")

    assert "AuthSession" in source
    assert "Consent" in source
    assert "TokenRecord" in source
    assert ".orm" not in source
