from __future__ import annotations

import ast
import importlib
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"
SERVER_ROOT = PKGS / "tigrbl-identity-server" / "src"
AUTH_FACADE_ROOT = PKGS / "tigrbl-auth" / "src"


def _source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _imports_from(path: Path) -> set[str]:
    tree = ast.parse(_source(path))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    return imports


def test_server_has_no_rest_schema_bucket_module() -> None:
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("tigrbl_identity_server.routers.schemas")


def test_rest_schema_facade_points_to_protocol_contracts() -> None:
    schemas = importlib.import_module("tigrbl_auth.api.rest.schemas")
    contracts = importlib.import_module("tigrbl_identity_contracts.rest")

    assert schemas.CredsIn is contracts.CredsIn
    assert schemas.TokenPair is contracts.TokenPair


def test_no_package_imports_removed_server_schema_bucket() -> None:
    offenders: list[str] = []
    for root in (SERVER_ROOT, AUTH_FACADE_ROOT):
        for path in root.rglob("*.py"):
            source = _source(path)
            if (
                "tigrbl_identity_server.routers.schemas" in source
                or "routers.schemas" in source
            ):
                offenders.append(path.relative_to(ROOT).as_posix())

    assert offenders == []


@pytest.mark.parametrize(
    ("module_name", "names"),
    [
        (
            "tigrbl_identity_storage.tables.user",
            {
                "AdminIdentityOut",
                "AdminIdentityProvisionIn",
                "AdminIdentityUpdateIn",
                "MyAccountMutationOut",
                "MyAccountPasswordChangeIn",
                "MyAccountProfileOut",
                "MyAccountProfileUpdateIn",
            },
        ),
        (
            "tigrbl_identity_storage.tables.tenant",
            {"AdminTenantOut", "AdminTenantProvisionIn", "AdminTenantUpdateIn"},
        ),
        (
            "tigrbl_identity_storage.tables.realm",
            {"AdminRealmOut", "AdminRealmProvisionIn", "AdminRealmUpdateIn"},
        ),
        ("tigrbl_identity_storage.tables.auth_session", {"MyAccountSessionOut"}),
        (
            "tigrbl_identity_storage.tables.consent",
            {"MyAccountAuthorizedAppOut", "MyAccountConsentOut"},
        ),
    ],
)
def test_table_backed_rest_schemas_live_on_table_modules(
    module_name: str, names: set[str]
) -> None:
    module = importlib.import_module(module_name)

    missing = sorted(name for name in names if not hasattr(module, name))
    assert missing == []


@pytest.mark.parametrize(
    ("route_file", "required_imports"),
    [
        ("admin_identities.py", {"tigrbl_identity_storage.tables.user"}),
        ("admin_tenants.py", {"tigrbl_identity_storage.tables.tenant"}),
        (
            "admin_realms.py",
            {
                "tigrbl_identity_storage.tables.realm",
                "tigrbl_identity_storage.tables.tenant",
            },
        ),
        (
            "my_account.py",
            {
                "tigrbl_identity_storage.tables.auth_session",
                "tigrbl_identity_storage.tables.consent",
                "tigrbl_identity_storage.tables.user",
            },
        ),
    ],
)
def test_table_backed_rest_routers_import_schemas_from_table_modules(
    route_file: str, required_imports: set[str]
) -> None:
    path = SERVER_ROOT / "tigrbl_identity_server" / "rest" / "routers" / route_file
    imports = _imports_from(path)

    assert required_imports <= imports
    assert "tigrbl_identity_contracts.rest" not in imports


@pytest.mark.parametrize(
    "route_file",
    [
        "admin_auth.py",
        "auth_flows.py",
        "device_authorization.py",
        "login.py",
        "par.py",
        "register.py",
        "revoke.py",
        "token.py",
    ],
)
def test_protocol_rest_routers_import_protocol_schemas_from_contracts(
    route_file: str,
) -> None:
    path = SERVER_ROOT / "tigrbl_identity_server" / "rest" / "routers" / route_file

    assert "tigrbl_identity_contracts.rest" in _imports_from(path)


@pytest.mark.parametrize(
    "path",
    [
        SERVER_ROOT / "tigrbl_identity_server" / "routers" / "auth_flows.py",
        SERVER_ROOT / "tigrbl_identity_server" / "routers" / "authz" / "oidc.py",
    ],
)
def test_legacy_router_modules_are_bridge_only(path: Path) -> None:
    source = _source(path)

    assert "tigrbl_identity_server.rest.routers" in source
    assert ".handlers.create.core" not in source
    assert ".handlers.update.core" not in source
    assert ".handlers.delete.core" not in source
    assert ".handlers.clear.core" not in source
