from __future__ import annotations

import ast
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "pkgs").glob("*/src")):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)


def test_principals_t0_exports_all_first_class_models() -> None:
    import tigrbl_identity_principals as principals

    assert principals.PrincipalKind.USER.value == "user"
    assert principals.PrincipalStatus.ACTIVE.value == "active"
    assert principals.AuthorityRole.SUPERUSER.value == "superuser"
    assert principals.NONHUMAN_PRINCIPAL_KINDS
    assert str(principals.new_principal_id())


def test_principal_contracts_are_grouped_under_principals_package() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "01-contracts"
        / "tigrbl-identity-contracts"
        / "src"
        / "tigrbl_identity_contracts"
    )

    assert not (contracts_root / "principals.py").exists()
    assert (contracts_root / "principals" / "__init__.py").is_file()
    assert (contracts_root / "principals" / "enums.py").is_file()
    assert (contracts_root / "principals" / "models.py").is_file()


def test_authority_roles_are_authz_owned_with_principal_compatibility() -> None:
    import tigrbl_authz_policy as authz
    import tigrbl_identity_principals as principals

    assert authz.AuthorityRole.SUPERUSER.value == principals.AuthorityRole.SUPERUSER.value
    assert authz.has_admin_authority([authz.AuthorityRole.ADMIN]) is True
    assert authz.has_owner_authority(["owner"]) is True
    assert authz.has_superuser_authority(["superuser"]) is True


def test_principals_t0_constructs_human_and_nonhuman_principals() -> None:
    import tigrbl_identity_principals as principals

    user = principals.create_user_principal("user@example.test", tenant_id="tenant-a")
    service = principals.create_service_principal("svc:billing", tenant_id="tenant-a")
    app = principals.create_app_principal("app:portal", tenant_id="tenant-a")
    machine = principals.create_machine_principal("machine:runner-1", tenant_id="tenant-a")
    workload = principals.create_workload_principal("workload:jobs/monthly", tenant_id="tenant-a")
    device = principals.create_device_principal("device:tablet-1", tenant_id="tenant-a")

    assert user.is_human is True
    assert {service.kind, app.kind, machine.kind, workload.kind, device.kind} == {
        principals.PrincipalKind.SERVICE,
        principals.PrincipalKind.APP,
        principals.PrincipalKind.MACHINE,
        principals.PrincipalKind.WORKLOAD,
        principals.PrincipalKind.DEVICE,
    }
    assert all(item.is_nonhuman for item in (service, app, machine, workload, device))


def test_principals_t1_admin_owner_superuser_roles_are_explicit() -> None:
    import tigrbl_identity_principals as principals

    admin = principals.create_admin_principal("admin@example.test", owner=True, superuser=True)

    assert admin.kind is principals.PrincipalKind.ADMIN
    assert admin.is_admin is True
    assert admin.is_owner is True
    assert admin.is_superuser is True
    assert admin.to_dict()["roles"] == ["admin", "owner", "superuser"]


def test_principals_t1_membership_and_alias_resolution() -> None:
    import tigrbl_identity_principals as principals

    directory = principals.PrincipalDirectory()
    user = directory.add_principal(principals.create_user_principal("user@example.test", id="p-user"))
    membership = principals.membership_for(user, "tenant-a", roles=["viewer"])
    alias = principals.alias_for(user, issuer="https://issuer.example", subject="external-user", verified=True)

    directory.add_membership(membership)
    directory.add_alias(alias)

    assert directory.list_by_tenant("tenant-a") == (user,)
    assert directory.resolve_alias(issuer="https://issuer.example", subject="external-user") == user
    assert directory.memberships_for_principal(user.id) == (membership,)


def test_principals_t2_rejects_invalid_nonhuman_kind_and_alias_collision() -> None:
    import pytest
    import tigrbl_identity_principals as principals

    directory = principals.PrincipalDirectory()
    first = directory.add_principal(principals.create_user_principal("first@example.test", id="p-first"))
    second = directory.add_principal(principals.create_user_principal("second@example.test", id="p-second"))
    directory.add_alias(principals.alias_for(first, issuer="https://issuer.example", subject="external"))

    with pytest.raises(ValueError, match="not a nonhuman principal kind"):
        principals.create_nonhuman_principal(principals.PrincipalKind.USER, "user@example.test")
    with pytest.raises(ValueError, match="already bound"):
        directory.add_alias(principals.alias_for(second, issuer="https://issuer.example", subject="external"))


def test_principals_t2_import_dag_stays_clean() -> None:
    package_root = ROOT / "pkgs" / "tigrbl-identity-principals" / "src" / "tigrbl_identity_principals"
    forbidden = {"tigrbl_auth", "tigrbl_identity_admin", "tigrbl_identity_server", "tigrbl_identity_storage"}

    for path in package_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        assert not (imports & forbidden), path
