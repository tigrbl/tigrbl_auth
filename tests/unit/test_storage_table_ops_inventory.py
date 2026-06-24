from __future__ import annotations

import ast
import importlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TABLES_DIR = (
    ROOT
    / "pkgs"
    / "01-storage"
    / "tigrbl-identity-storage"
    / "src"
    / "tigrbl_identity_storage"
    / "tables"
)
MATRIX_PATH = ROOT / "docs" / "refactor" / "01-storage-classmethod-refactor-matrix.md"

PRIVATE_HELPER_ROWS = {
    ("OperatorRecord", "row_to_record"),
    ("OperatorRecord", "normalize_record"),
    ("OperatorRecord", "payload_from_record"),
}


def _decorator_name(decorator: ast.expr) -> str:
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        return target.attr
    return ""


def _matrix_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in MATRIX_PATH.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| 01-storage |"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        rows.append(
            {
                "module": cells[2].strip("`"),
                "class": cells[3].strip("`"),
                "method": cells[4].strip("`"),
                "action": cells[6].split(":", 1)[0],
            }
        )
    return rows


def _table_path(module_name: str) -> Path:
    suffix = module_name.removeprefix("tigrbl_identity_storage.tables.").replace(".", "/")
    return TABLES_DIR / f"{suffix}.py"


def _package_module(module_name: str) -> str:
    return module_name.removesuffix("._table")


def _ops_paths() -> list[Path]:
    return [
        path
        for path in sorted(TABLES_DIR.rglob("*.py"))
        if path.name == "_ops.py" or "_ops" in path.parts
    ]


def _op_spec(attr: object) -> object | None:
    return getattr(getattr(attr, "__func__", attr), "__tigrbl_op_spec__", None)


def test_storage_table_modules_do_not_define_classmethod_ops() -> None:
    offenders: list[str] = []
    for path in sorted(TABLES_DIR.glob("**/_table.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if any(_decorator_name(decorator) == "classmethod" for decorator in node.decorator_list):
                offenders.append(f"{path.relative_to(ROOT).as_posix()}::{node.name}")

    assert offenders == []


def test_storage_ops_modules_do_not_use_op_ctx() -> None:
    offenders: list[str] = []
    for path in _ops_paths():
        text = path.read_text(encoding="utf-8")
        if "op_ctx" in text or "_table_op_ctx" in text:
            offenders.append(path.relative_to(ROOT).as_posix())

    assert offenders == []


def test_matrix_table_ops_are_collapsed_from_table_classes() -> None:
    unexpected_semantic_methods: list[str] = []
    invalid_ctx_ops: list[str] = []

    for row in _matrix_rows():
        module = importlib.import_module(_package_module(row["module"]))
        cls = getattr(module, row["class"])
        method_name = row["method"]

        if (row["class"], method_name) in PRIVATE_HELPER_ROWS:
            continue
        if hasattr(cls, method_name):
            attr = getattr(cls, method_name)
            spec = _op_spec(attr)
            if spec is None:
                unexpected_semantic_methods.append(f"{row['class']}.{method_name}")
            elif getattr(spec, "expose_routes", None) is not False:
                invalid_ctx_ops.append(f"{row['class']}.{method_name}")

    assert unexpected_semantic_methods == []
    assert invalid_ctx_ops == []


def test_refactor_matrix_covers_every_original_table_classmethod_row() -> None:
    rows = _matrix_rows()
    assert len(rows) == 221
    assert all(_table_path(row["module"]).exists() for row in rows)
