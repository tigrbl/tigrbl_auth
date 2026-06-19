from __future__ import annotations

import ast
import importlib
import sys
import warnings
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "pkgs").glob("*/*/src")):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)


def _imports_for(package: str) -> set[str]:
    package_root = next((ROOT / "pkgs").glob(f"00-core/*/src/{package}"))
    imports: set[str] = set()
    for path in package_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
    return imports


def test_management_plane_contracts_import_surface() -> None:
    import tigrbl_management_plane_contracts as contracts

    assert contracts.AdminResourceKind.PRINCIPAL.value == "principal"
    assert contracts.AdminUiState.LOADING.value == "loading"
    assert contracts.SDKPackage(
        sdk_id="sdk:py",
        package_name="pkg",
        language="python",
        version="1.0.0",
        compatible_runtime_range=("1.0.0", "2.0.0"),
        generated_contracts={},
        auth_helpers=(),
        supported_errors=(),
    ).sdk_id == "sdk:py"
    assert contracts.ResidencyZone(
        zone_id="eu",
        jurisdictions=("eu",),
    ).zone_id == "eu"
    assert contracts.KeyRotationAuditEvidence.__name__ == "KeyRotationAuditEvidence"


def test_management_plane_contracts_do_not_import_runtime_or_stateful_packages() -> None:
    forbidden = {
        "tigrbl_auth",
        "tigrbl_authn_credentials",
        "tigrbl_authz_policy",
        "tigrbl_authz_resource_server",
        "tigrbl_identity_runtime",
        "tigrbl_identity_storage",
        "tigrbl_identity_server",
    }

    assert not (_imports_for("tigrbl_management_plane_contracts") & forbidden)


def test_legacy_plane_contract_modules_reexport_with_deprecation_warnings() -> None:
    sys.modules.pop("tigrbl_control_plane_contracts.admin_resources", None)
    sys.modules.pop("tigrbl_control_plane_contracts.governance", None)
    sys.modules.pop("tigrbl_user_plane_contracts.authz.residency", None)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        residency = importlib.import_module("tigrbl_user_plane_contracts.authz.residency")

    import tigrbl_management_plane_contracts as contracts

    assert residency.ResidencyZone is contracts.ResidencyZone
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("tigrbl_control_plane_contracts.admin_resources")
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("tigrbl_control_plane_contracts.governance")
    assert contracts.AdminResourceKind.__name__ == "AdminResourceKind"
    assert contracts.SDKPackage.__name__ == "SDKPackage"
    messages = "\n".join(str(item.message) for item in caught)
    assert "tigrbl_management_plane_contracts.residency" in messages
