from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"


def package_src(name: str) -> Path:
    matches = sorted(PKGS.glob(f"**/{name}/src"))
    assert matches, f"missing package src for {name}"
    return matches[0]


FACADE_DIR = package_src("tigrbl-auth") / "tigrbl_auth"
STORAGE_DIR = package_src("tigrbl-identity-storage") / "tigrbl_identity_storage"


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
