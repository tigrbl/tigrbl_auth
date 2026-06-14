from __future__ import annotations

import ast
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"

PYTHON_PACKAGE_LAYERS = {
    "foundation": {
        "tigrbl-auth-protocol-oauth",
        "tigrbl-auth-protocol-oidc",
        "tigrbl-auth-protocol-rp",
        "tigrbl-authn-credentials",
        "tigrbl-authz-policy",
        "tigrbl-authz-resource-server",
        "tigrbl-identity-admin",
        "tigrbl-identity-cli",
        "tigrbl-identity-contracts",
        "tigrbl-identity-core",
        "tigrbl-identity-credentials",
        "tigrbl-identity-jose",
        "tigrbl-identity-oauth",
        "tigrbl-identity-oidc",
        "tigrbl-identity-operator",
        "tigrbl-identity-policy",
        "tigrbl-identity-principals",
        "tigrbl-identity-resource-server",
        "tigrbl-identity-rp",
        "tigrbl-identity-runtime",
        "tigrbl-identity-server",
        "tigrbl-identity-storage",
        "tigrbl-identity-testkit",
    },
    "facade": {"tigrbl-auth"},
    "downstream_backend": {
        "tigrbl-auth-api-developer",
        "tigrbl-auth-api-my-account",
        "tigrbl-auth-api-platform-admin",
        "tigrbl-auth-api-public",
        "tigrbl-auth-api-resource-validation",
        "tigrbl-auth-api-service-admin",
        "tigrbl-auth-api-tenant-admin",
    },
}

FRONTEND_WORKSPACES = {
    ROOT / "apps" / "admin-uix",
    ROOT / "apps" / "demo-hub-uix",
    ROOT / "apps" / "developer-uix",
    ROOT / "apps" / "my-account-uix",
    ROOT / "apps" / "platform-admin-uix",
    ROOT / "apps" / "public-uix",
    ROOT / "apps" / "rp",
    ROOT / "apps" / "service-admin-uix",
    ROOT / "apps" / "tenant-admin-uix",
    ROOT / "packages" / "uix-core",
}

T2_FOUNDATION_FACADE_IMPORT_EXCEPTIONS: dict[str, str] = {}

JS_IMPORT_RE = re.compile(
    r"""(?:from\s+["'](?P<from>[^"']+)["']|import\s*\(\s*["'](?P<dynamic>[^"']+)["']\s*\)|require\s*\(\s*["'](?P<require>[^"']+)["']\s*\))"""
)


def _declared_python_packages() -> set[str]:
    return {path.parent.name for path in PKGS.glob("*/pyproject.toml")}


def _absolute_import_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    roots: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            roots.add(node.module.split(".")[0])

    return roots


def _package_facade_imports(package_name: str) -> list[Path]:
    package_dir = PKGS / package_name
    return [
        path.relative_to(ROOT)
        for path in sorted((package_dir / "src").rglob("*.py"))
        if "tigrbl_auth" in _absolute_import_roots(path)
    ]


def _js_import_specifiers(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    specifiers: set[str] = set()

    for match in JS_IMPORT_RE.finditer(text):
        specifier = match.group("from") or match.group("dynamic") or match.group("require")
        if specifier:
            specifiers.add(specifier)

    return specifiers


def test_all_python_packages_are_assigned_to_one_dependency_layer() -> None:
    discovered = _declared_python_packages()
    declared = set().union(*PYTHON_PACKAGE_LAYERS.values())

    assert declared == discovered

    layer_names = list(PYTHON_PACKAGE_LAYERS)
    for index, layer in enumerate(layer_names):
        for other in layer_names[index + 1 :]:
            assert PYTHON_PACKAGE_LAYERS[layer].isdisjoint(PYTHON_PACKAGE_LAYERS[other])


def test_t2_foundation_packages_do_not_import_tigrbl_auth_facade() -> None:
    facade_consumers = {
        package
        for package in _declared_python_packages()
        if _package_facade_imports(package)
    }
    expected_upper_layers = (
        PYTHON_PACKAGE_LAYERS["facade"] | PYTHON_PACKAGE_LAYERS["downstream_backend"]
    )
    foundation_consumers = facade_consumers - expected_upper_layers

    undeclared = foundation_consumers - set(T2_FOUNDATION_FACADE_IMPORT_EXCEPTIONS)
    stale = set(T2_FOUNDATION_FACADE_IMPORT_EXCEPTIONS) - foundation_consumers

    assert not undeclared, {
        package: [str(path) for path in _package_facade_imports(package)]
        for package in sorted(undeclared)
    }
    assert not stale


def test_new_authn_authz_protocol_packages_do_not_import_tigrbl_auth_facade() -> None:
    split_packages = {
        package
        for package in PYTHON_PACKAGE_LAYERS["foundation"]
        if package.startswith("tigrbl-auth")
    }

    offenders = {
        package: [str(path) for path in _package_facade_imports(package)]
        for package in sorted(split_packages)
        if _package_facade_imports(package)
    }

    assert offenders == {}


def test_frontend_workspaces_do_not_import_python_facade_modules() -> None:
    frontend_source_suffixes = {".cjs", ".js", ".jsx", ".mjs", ".ts", ".tsx"}
    offenders: dict[str, list[str]] = {}

    for workspace in FRONTEND_WORKSPACES:
        for path in sorted(workspace.rglob("*")):
            if path.suffix not in frontend_source_suffixes:
                continue

            python_facade_specifiers = [
                specifier
                for specifier in sorted(_js_import_specifiers(path))
                if specifier == "tigrbl_auth" or specifier.startswith("tigrbl_auth.")
            ]
            if python_facade_specifiers:
                offenders[str(path.relative_to(ROOT))] = python_facade_specifiers

    assert offenders == {}
