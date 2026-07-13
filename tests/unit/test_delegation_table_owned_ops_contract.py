from __future__ import annotations

import ast
from pathlib import Path


DELEGATION_TABLE = (
    Path(__file__).resolve().parents[2]
    / "pkgs"
    / "01-storage"
    / "tigrbl-identity-storage"
    / "src"
    / "tigrbl_identity_storage"
    / "tables"
    / "delegation_grant"
    / "_table.py"
)


def _bound_ops(class_name: str) -> set[str]:
    module = ast.parse(DELEGATION_TABLE.read_text(encoding="utf-8"))
    aliases: set[str] = set()
    for node in module.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call):
                continue
            keywords = {item.arg: item.value for item in decorator.keywords}
            bind = keywords.get("bind")
            alias = keywords.get("alias")
            if (
                isinstance(bind, ast.Name)
                and bind.id == class_name
                and isinstance(alias, ast.Constant)
                and isinstance(alias.value, str)
            ):
                aliases.add(alias.value)
    return aliases


def test_delegation_storage_tables_own_grant_and_provenance_ops() -> None:
    assert {
        "activate_grant",
        "create_grant",
        "expire_grant",
        "inspect_grant",
        "list_grants",
        "replace_grant",
        "revoke_grant",
    } <= _bound_ops("DelegationGrant")
    assert {"persist_provenance"} <= _bound_ops("DelegationGrantProof")
    assert {"link_token", "list_for_grant"} <= _bound_ops("DelegationGrantTokenLink")
