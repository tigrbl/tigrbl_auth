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


def _class_methods(class_name: str) -> set[str]:
    module = ast.parse(DELEGATION_TABLE.read_text(encoding="utf-8"))
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return {item.name for item in node.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))}
    raise AssertionError(f"{class_name} not found in {DELEGATION_TABLE}")


def test_delegation_storage_tables_own_grant_and_provenance_ops() -> None:
    assert {
        "activate_grant",
        "create_grant",
        "expire_grant",
        "inspect_grant",
        "list_grants",
        "replace_grant",
        "revoke_grant",
    } <= _class_methods("DelegationGrant")
    assert {"persist_provenance"} <= _class_methods("DelegationGrantProof")
    assert {"link_token", "list_for_grant"} <= _class_methods("DelegationGrantTokenLink")
