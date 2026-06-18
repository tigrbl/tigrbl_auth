from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"
STORAGE_ROOT = PKGS / "tigrbl-identity-storage" / "src"
NON_STORAGE_SOURCE_ROOTS = [
    PKGS / "tigrbl-auth-api-my-account" / "src",
    PKGS / "tigrbl-auth-api-public" / "src",
    PKGS / "tigrbl-auth-protocol-oauth" / "src",
    PKGS / "tigrbl-authn-credentials" / "src",
    PKGS / "tigrbl-identity-operator" / "src",
    PKGS / "tigrbl-identity-server" / "src",
]

RAW_HANDLER_TOKENS = (
    ".handlers.create.core",
    ".handlers.update.core",
    ".handlers.delete.core",
    ".handlers.clear.core",
)

RAW_HANDLER_ALLOWLIST = {
    "pkgs/tigrbl-identity-server/src/tigrbl_identity_server/security/handler_records.py",
}


def _python_files(root: Path) -> list[Path]:
    return [path for path in root.rglob("*.py") if "__pycache__" not in path.parts]


def test_non_storage_packages_do_not_own_raw_durable_table_mutations() -> None:
    offenders: list[str] = []
    for root in NON_STORAGE_SOURCE_ROOTS:
        if not root.exists():
            continue
        for path in _python_files(root):
            rel = path.relative_to(ROOT).as_posix()
            if rel in RAW_HANDLER_ALLOWLIST:
                continue
            source = path.read_text(encoding="utf-8")
            for token in RAW_HANDLER_TOKENS:
                if token in source:
                    offenders.append(f"{rel} uses {token}")

    assert offenders == []


def test_no_rpc_support_is_reintroduced_in_product_api_packages() -> None:
    offenders: list[str] = []
    for root in [PKGS / "tigrbl-auth-api-my-account" / "src", PKGS / "tigrbl-auth-api-public" / "src"]:
        if not root.exists():
            continue
        for path in _python_files(root):
            source = path.read_text(encoding="utf-8")
            if "openrpc" in source.lower() or '"/rpc"' in source or "'/rpc'" in source:
                offenders.append(path.relative_to(ROOT).as_posix())

    assert offenders == []


def test_storage_table_ops_are_not_hidden_in_module_level_free_functions() -> None:
    offenders: list[str] = []
    for path in (STORAGE_ROOT / "tigrbl_identity_storage" / "tables").glob("*.py"):
        if path.name in {"__init__.py", "_ops.py", "engine.py"}:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
                offenders.append(f"{path.relative_to(ROOT).as_posix()}::{node.name}")

    assert offenders == []
