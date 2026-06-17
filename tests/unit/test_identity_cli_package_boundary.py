from __future__ import annotations

import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[2]
CLI_SRC = ROOT / "pkgs" / "tigrbl-identity-cli" / "src"
OPERATOR_SRC = ROOT / "pkgs" / "tigrbl-identity-operator" / "src"

for value in (str(ROOT), str(CLI_SRC), str(OPERATOR_SRC)):
    if value in sys.path:
        sys.path.remove(value)
for value in (str(OPERATOR_SRC), str(CLI_SRC), str(ROOT)):
    if value not in sys.path:
        sys.path.insert(0, value)


def _clear_cli_modules() -> None:
    for value in (str(ROOT), str(CLI_SRC), str(OPERATOR_SRC)):
        while value in sys.path:
            sys.path.remove(value)
    for value in (str(OPERATOR_SRC), str(CLI_SRC), str(ROOT)):
        sys.path.insert(0, value)
    for name in list(sys.modules):
        if (
            name == "tigrbl_auth"
            or name.startswith("tigrbl_auth.cli")
            or name.startswith("tigrbl_identity_cli")
            or name.startswith("tigrbl_identity_operator.cli")
        ):
            sys.modules.pop(name, None)


def test_identity_cli_package_owns_canonical_entrypoint() -> None:
    _clear_cli_modules()

    from tigrbl_identity_cli.cli.main import main
    from tigrbl_identity_cli.cli.metadata import build_parser

    assert callable(main)
    assert build_parser().prog == "tigrbl-auth"


def test_legacy_cli_import_paths_are_shims_to_identity_cli() -> None:
    _clear_cli_modules()

    from tigrbl_auth.cli.handlers import HANDLER_MAP as auth_handlers
    from tigrbl_auth.cli.metadata import COMMAND_SPECS as auth_specs
    from tigrbl_identity_cli.cli.handlers import HANDLER_MAP as cli_handlers
    from tigrbl_identity_cli.cli.metadata import COMMAND_SPECS as cli_specs
    from tigrbl_identity_operator.cli.handlers import HANDLER_MAP as operator_handlers
    from tigrbl_identity_operator.cli.metadata import COMMAND_SPECS as operator_specs

    assert auth_handlers is cli_handlers
    assert operator_handlers is cli_handlers
    assert auth_specs is cli_specs
    assert operator_specs is cli_specs


def test_legacy_cli_packages_do_not_keep_per_module_shim_files() -> None:
    legacy_cli_roots = [
        ROOT / "tigrbl_auth" / "cli",
        ROOT / "pkgs" / "tigrbl-auth" / "src" / "tigrbl_auth" / "cli",
        ROOT / "pkgs" / "tigrbl-identity-operator" / "src" / "tigrbl_identity_operator" / "cli",
    ]

    for cli_root in legacy_cli_roots:
        assert sorted(path.name for path in cli_root.glob("*.py")) == ["__init__.py"]


def test_root_console_script_delegates_to_identity_cli() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert pyproject["project"]["scripts"]["tigrbl-auth"] == "tigrbl_identity_cli.cli.main:main"
    assert "pkgs/tigrbl-identity-cli/src" in pyproject["tool"]["pytest"]["ini_options"]["pythonpath"]


def test_identity_cli_declares_python_310_toml_reader_dependency() -> None:
    pyproject = tomllib.loads(
        (ROOT / "pkgs" / "tigrbl-identity-cli" / "pyproject.toml").read_text(encoding="utf-8")
    )

    assert "tomli>=2.0; python_version < '3.11'" in pyproject["project"]["dependencies"]
