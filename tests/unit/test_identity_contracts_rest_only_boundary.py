from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

from tigrbl_identity_contracts.models import ContractProjection


ROOT = Path(__file__).resolve().parents[2]
TARGET_PACKAGES = (
    "tigrbl-identity-contracts",
    "tigrbl-identity-admin",
    "tigrbl-identity-concrete",
    "tigrbl-identity-server",
    "tigrbl-identity-runtime",
)

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def package_root(name: str) -> Path:
    matches = sorted((ROOT / "pkgs").glob(f"**/{name}/pyproject.toml"))
    assert matches, f"missing package root for {name}"
    return matches[0].parent


def test_identity_contracts_do_not_export_rpc_package() -> None:
    for module_name in (
        "tigrbl_identity_contracts.rpc",
        "tigrbl_identity_admin.rpc",
        "tigrbl_identity_server.rpc",
    ):
        with pytest.raises(ModuleNotFoundError):
            importlib.import_module(module_name)


def test_identity_contract_projection_is_openapi_only() -> None:
    with pytest.raises(ValueError):
        ContractProjection(
            kind="openrpc",
            profile="baseline",
            version="0.4.0.dev2",
            document={},
        )

    projection = ContractProjection(
        kind="openapi",
        profile="baseline",
        version="0.4.0.dev2",
        document={},
    )
    assert projection.kind == "openapi"


def test_identity_contracts_have_no_pydantic_schema_ownership() -> None:
    current_package_root = package_root("tigrbl-identity-contracts")
    metadata = tomllib.loads((current_package_root / "pyproject.toml").read_text(encoding="utf-8"))
    dependencies = [dependency.lower() for dependency in metadata.get("project", {}).get("dependencies", [])]
    assert not any("pydantic" in dependency for dependency in dependencies)

    offenders = []
    for path in (current_package_root / "src" / "tigrbl_identity_contracts").rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        if "BaseModel" in source or "pydantic" in source:
            offenders.append(path.relative_to(ROOT).as_posix())

    assert offenders == []


def test_identity_contracts_rest_schema_bridge_is_removed() -> None:
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("tigrbl_identity_contracts.rest")
    models = importlib.import_module("tigrbl_identity_contracts.models")

    table_backed_dtos = {
        "AdminPrincipalResponse",
        "AdminIdentityOut",
        "AdminIdentityProvisionIn",
        "AdminIdentityUpdateIn",
        "AdminTenantOut",
        "AdminTenantProvisionIn",
        "AdminTenantUpdateIn",
        "AdminTenantRequest",
        "AdminTenantResponse",
        "AdminRealmOut",
        "AdminRealmProvisionIn",
        "AdminRealmUpdateIn",
        "MyAccountProfileOut",
        "MyAccountProfileUpdateIn",
        "MyAccountSessionOut",
        "MyAccountConsentOut",
        "MyAccountAuthorizedAppOut",
        "MyAccountPasswordChangeIn",
        "MyAccountMutationOut",
        "RegisterIn",
    }
    for dto_name in table_backed_dtos:
        assert not hasattr(models, dto_name), dto_name


def test_storage_tables_own_table_backed_rest_shapes() -> None:
    table_modules = {
        "tigrbl_identity_storage.tables.auth_session": {"MyAccountSessionOut"},
        "tigrbl_identity_storage.tables.consent": {
            "MyAccountAuthorizedAppOut",
            "MyAccountConsentOut",
        },
        "tigrbl_identity_storage.tables.realm": {
            "AdminRealmOut",
            "AdminRealmProvisionIn",
            "AdminRealmUpdateIn",
        },
        "tigrbl_identity_storage.tables.tenant": {
            "AdminTenantOut",
            "AdminTenantProvisionIn",
            "AdminTenantUpdateIn",
        },
        "tigrbl_identity_storage.tables.user": {
            "AdminIdentityOut",
            "AdminIdentityProvisionIn",
            "AdminIdentityUpdateIn",
            "MyAccountMutationOut",
            "MyAccountPasswordChangeIn",
            "MyAccountProfileOut",
            "MyAccountProfileUpdateIn",
        },
    }
    for module_name, dto_names in table_modules.items():
        module = importlib.import_module(module_name)
        for dto_name in dto_names:
            assert hasattr(module, dto_name), f"{module_name}.{dto_name}"


def test_table_backed_route_modules_do_not_import_contract_dtos() -> None:
    route_root = package_root("tigrbl-identity-server") / "src" / "tigrbl_identity_server" / "rest" / "routers"
    table_backed_route_files = (
        "admin_identities.py",
        "admin_realms.py",
        "admin_tenants.py",
        "my_account.py",
    )
    for filename in table_backed_route_files:
        route_file = route_root / filename
        if not route_file.exists():
            continue
        source = route_file.read_text(encoding="utf-8")
        assert "tigrbl_identity_contracts" not in source, filename


def test_identity_core_package_metadata_does_not_advertise_rpc_surfaces() -> None:
    forbidden = ("json-rpc", "openrpc", "admin-rpc", "/rpc", "surface_rpc_enabled")
    for package in TARGET_PACKAGES:
        current_package_root = package_root(package)
        metadata = tomllib.loads(
            (current_package_root / "pyproject.toml").read_text(encoding="utf-8")
        )
        project_text = " ".join(
            str(value).lower()
            for value in (
                metadata.get("project", {}).get("description", ""),
                *metadata.get("project", {}).get("keywords", []),
            )
        )
        assert not any(token in project_text for token in forbidden), package


def test_identity_core_package_source_does_not_advertise_rpc_surfaces() -> None:
    forbidden = ("json-rpc", "openrpc", "admin-rpc", "surface_rpc_enabled")
    server_root = package_root("tigrbl-identity-server")
    allowed_negative_route_guards = {
        (
            server_root
            / "src"
            / "tigrbl_identity_server"
            / "security"
            / "admin_gate.py"
        )
    }
    for package in TARGET_PACKAGES:
        current_package_root = package_root(package)
        for path in current_package_root.rglob("*"):
            if path.suffix not in {".py", ".md", ".toml", ".yaml"}:
                continue
            if "__pycache__" in path.parts:
                continue
            source = path.read_text(encoding="utf-8").lower()
            if path in allowed_negative_route_guards:
                assert "json-rpc" not in source
                assert "admin-rpc" not in source
                assert "surface_rpc_enabled" not in source
                continue
            assert not any(token in source for token in forbidden), (
                path.relative_to(ROOT).as_posix()
            )
            assert "/rpc" not in source, path.relative_to(ROOT).as_posix()
