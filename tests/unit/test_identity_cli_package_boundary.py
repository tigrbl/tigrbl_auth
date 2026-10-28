from __future__ import annotations

import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[2]
FACADE_SRC = ROOT / "pkgs" / "70-facade" / "tba-auth" / "src"
CLI_SRC = ROOT / "pkgs" / "60-runtime" / "tba-cli-identity" / "src"
OPERATOR_SRC = ROOT / "pkgs" / "60-runtime" / "tba-operator-identity" / "src"

for value in (str(ROOT), str(FACADE_SRC), str(CLI_SRC), str(OPERATOR_SRC)):
    if value in sys.path:
        sys.path.remove(value)
for value in (str(OPERATOR_SRC), str(CLI_SRC), str(FACADE_SRC)):
    if value not in sys.path:
        sys.path.insert(0, value)


def _clear_cli_modules() -> None:
    for value in (str(ROOT), str(FACADE_SRC), str(CLI_SRC), str(OPERATOR_SRC)):
        while value in sys.path:
            sys.path.remove(value)
    for value in (str(OPERATOR_SRC), str(CLI_SRC), str(FACADE_SRC)):
        sys.path.insert(0, value)
    for name in list(sys.modules):
        if (
            name == "tba_auth"
            or name.startswith("tba_auth.cli")
            or name.startswith("tba_cli_identity")
            or name.startswith("tba_operator_identity.cli")
        ):
            sys.modules.pop(name, None)


def test_identity_cli_package_owns_canonical_entrypoint() -> None:
    _clear_cli_modules()

    from tba_cli_identity.cli.main import main
    from tba_cli_identity.cli.metadata import build_parser

    assert callable(main)
    assert build_parser().prog == "tba-auth"


def test_legacy_cli_import_paths_are_shims_to_identity_cli() -> None:
    _clear_cli_modules()

    from tba_auth.cli.handlers import HANDLER_MAP as auth_handlers
    from tba_auth.cli.metadata import COMMAND_SPECS as auth_specs
    from tba_cli_identity.cli.handlers import HANDLER_MAP as cli_handlers
    from tba_cli_identity.cli.metadata import COMMAND_SPECS as cli_specs
    from tba_operator_identity.cli.handlers import HANDLER_MAP as operator_handlers
    from tba_operator_identity.cli.metadata import COMMAND_SPECS as operator_specs

    assert auth_handlers is cli_handlers
    assert operator_handlers is cli_handlers
    assert auth_specs is cli_specs
    assert operator_specs is cli_specs


def test_legacy_cli_packages_do_not_keep_per_module_shim_files() -> None:
    legacy_cli_roots = [
        ROOT / "pkgs" / "70-facade" / "tba-auth" / "src" / "tba_auth" / "cli",
        ROOT
        / "pkgs"
        / "60-runtime"
        / "tba-operator-identity"
        / "src"
        / "tba_operator_identity"
        / "cli",
    ]

    for cli_root in legacy_cli_roots:
        assert sorted(path.name for path in cli_root.glob("*.py")) == ["__init__.py"]


def test_workspace_console_script_delegates_to_identity_cli_without_packaging_root() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert pyproject["project"]["scripts"]["tba-auth"] == "tba_cli_identity.cli.main:main"
    assert pyproject["tool"]["uv"]["package"] is False
    assert "tba_auth_workspace" not in (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "." not in pyproject["tool"]["pytest"]["ini_options"]["pythonpath"]
    assert "pkgs/60-runtime/tba-cli-identity/src" in pyproject["tool"]["pytest"]["ini_options"]["pythonpath"]


def test_identity_cli_declares_python_310_toml_reader_dependency() -> None:
    pyproject = tomllib.loads(
        (ROOT / "pkgs" / "60-runtime" / "tba-cli-identity" / "pyproject.toml").read_text(
            encoding="utf-8"
        )
    )

    assert "tomli>=2.0; python_version < '3.11'" in pyproject["project"]["dependencies"]
