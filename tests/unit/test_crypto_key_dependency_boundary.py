from __future__ import annotations

from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[2]


def _load_package_pyproject(name: str) -> dict:
    matches = sorted((ROOT / "pkgs").glob(f"**/{name}/pyproject.toml"))
    assert matches, name
    return tomllib.loads(matches[0].read_text(encoding="utf-8"))


def test_crypto_key_execution_dependencies_flow_through_storage_runtime() -> None:
    jose_dependencies = set(_load_package_pyproject("tba-provider-identity-jose")["project"]["dependencies"])
    storage_dependencies = set(_load_package_pyproject("tba-storage-core")["project"]["dependencies"])
    storage_runtime_dependencies = set(
        _load_package_pyproject("tba-runtime-identity-storage")["project"]["dependencies"]
    )

    assert "tba-storage-core==0.4.0.dev2" not in jose_dependencies
    assert "tba-contracts-security-trust==0.1.0" in storage_dependencies
    assert "tba-contracts-security-trust==0.1.0" in storage_runtime_dependencies
