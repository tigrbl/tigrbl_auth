from __future__ import annotations

import ast
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"

PYTHON_PACKAGE_LAYERS = {
    "primitives": {
        "tigrbl-identity-core",
    },
    "contracts": {
        "tigrbl-identity-contracts",
        "tigrbl-release-contracts",
        "tigrbl-security-trust-contracts",
    },
    "bases": {
        "tigrbl-security-trust-domain-bases",
    },
    "concrete": {
        "tigrbl-authz-policy-concrete",
        "tigrbl-identity-concrete",
    },
    "storage": {
        "tigrbl-identity-storage",
    },
    "providers": {
        "tigrbl-identity-jose",
        "tigrbl-security-certificate-mtls",
        "tigrbl-security-proof-dpop",
        "tigrbl-security-proof-pkce",
        "tigrbl-security-signing-pqc",
    },
    "capabilities": {
        "tigrbl-authn-credentials",
        "tigrbl-authz-policy-abac-administrator",
        "tigrbl-authz-policy-delegated-administrator",
        "tigrbl-authz-policy-decision-engine",
        "tigrbl-authz-policy-engine",
        "tigrbl-authz-policy-invariant-registry",
        "tigrbl-authz-policy-rbac-administrator",
        "tigrbl-authz-policy-service-identity-registry",
        "tigrbl-authz-policy",
        "tigrbl-identity-admin",
        "tigrbl-identity-principals",
    },
    "protocols": {
        "tigrbl-auth-protocol-oauth",
        "tigrbl-auth-protocol-oidc",
        "tigrbl-auth-protocol-rp",
        "tigrbl-authz-resource-server",
    },
    "runtime": {
        "tigrbl-identity-author",
        "tigrbl-identity-cli",
        "tigrbl-identity-operator",
        "tigrbl-identity-runtime",
        "tigrbl-identity-server",
        "tigrbl-identity-testkit",
        "tigrbl-auth-release-certification",
    },
    "facade": {"tigrbl-auth"},
    "apis": {
        "tigrbl-auth-api-developer",
        "tigrbl-auth-api-my-account",
        "tigrbl-auth-api-platform-admin",
        "tigrbl-auth-api-public",
        "tigrbl-auth-api-resource-validation",
        "tigrbl-auth-api-service-admin",
        "tigrbl-auth-api-tenant-admin",
    },
    "deprecated": {
        "tigrbl-identity-credentials",
        "tigrbl-identity-oauth",
        "tigrbl-identity-oidc",
        "tigrbl-identity-policy",
        "tigrbl-identity-resource-server",
        "tigrbl-identity-rp",
    },
}

PYTHON_LAYER_FOLDERS = {
    "primitives": "00-primitives",
    "contracts": "01-contracts",
    "bases": "05-bases",
    "concrete": "10-concrete",
    "storage": "20-storage",
    "providers": "30-providers",
    "capabilities": "40-capabilities",
    "protocols": "50-protocols",
    "runtime": "60-runtime",
    "facade": "70-facade",
    "apis": "80-apis",
    "deprecated": "deprecated",
}

FRONTEND_WORKSPACES = {
    ROOT / "pkgs" / "90-uix-core" / "uix-core",
    ROOT / "pkgs" / "95-ui" / "admin-uix",
    ROOT / "pkgs" / "95-ui" / "demo-hub-uix",
    ROOT / "pkgs" / "95-ui" / "developer-uix",
    ROOT / "pkgs" / "95-ui" / "my-account-uix",
    ROOT / "pkgs" / "95-ui" / "platform-admin-uix",
    ROOT / "pkgs" / "95-ui" / "public-uix",
    ROOT / "pkgs" / "95-ui" / "rp",
    ROOT / "pkgs" / "95-ui" / "service-admin-uix",
    ROOT / "pkgs" / "95-ui" / "tenant-admin-uix",
}

LOWER_LAYER_FACADE_IMPORT_EXCEPTIONS: dict[str, str] = {}

JS_IMPORT_RE = re.compile(
    r"""(?:from\s+["'](?P<from>[^"']+)["']|import\s*\(\s*["'](?P<dynamic>[^"']+)["']\s*\)|require\s*\(\s*["'](?P<require>[^"']+)["']\s*\))"""
)


def _declared_python_packages() -> set[str]:
    return {path.parent.name for path in PKGS.rglob("pyproject.toml")}


def _package_dir(package_name: str) -> Path:
    matches = [path.parent for path in PKGS.rglob("pyproject.toml") if path.parent.name == package_name]
    assert len(matches) == 1, (package_name, matches)
    return matches[0]


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
    package_dir = _package_dir(package_name)
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

    assert "core" not in PYTHON_PACKAGE_LAYERS
    assert "foundation" not in PYTHON_PACKAGE_LAYERS
    assert not (PKGS / "00-core").exists()
    assert "domain" not in PYTHON_PACKAGE_LAYERS
    assert not (PKGS / "10-domain").exists()
    assert declared == discovered

    layer_names = list(PYTHON_PACKAGE_LAYERS)
    for index, layer in enumerate(layer_names):
        for other in layer_names[index + 1 :]:
            assert PYTHON_PACKAGE_LAYERS[layer].isdisjoint(PYTHON_PACKAGE_LAYERS[other])


def test_python_package_layers_match_filesystem_layout() -> None:
    assert set(PYTHON_LAYER_FOLDERS) == set(PYTHON_PACKAGE_LAYERS)

    for layer, packages in PYTHON_PACKAGE_LAYERS.items():
        expected_folder = PYTHON_LAYER_FOLDERS[layer]
        for package in packages:
            package_folder = _package_dir(package).relative_to(PKGS).parts[0]
            assert package_folder == expected_folder, (package, expected_folder, package_folder)


def test_lower_layer_packages_do_not_import_tigrbl_auth_facade() -> None:
    facade_consumers = {
        package
        for package in _declared_python_packages()
        if _package_facade_imports(package)
    }
    expected_upper_layers = (
        PYTHON_PACKAGE_LAYERS["facade"] | PYTHON_PACKAGE_LAYERS["apis"]
    )
    lower_layer_consumers = facade_consumers - expected_upper_layers

    undeclared = lower_layer_consumers - set(LOWER_LAYER_FACADE_IMPORT_EXCEPTIONS)
    stale = set(LOWER_LAYER_FACADE_IMPORT_EXCEPTIONS) - lower_layer_consumers

    assert not undeclared, {
        package: [str(path) for path in _package_facade_imports(package)]
        for package in sorted(undeclared)
    }
    assert not stale


def test_new_authn_authz_protocol_packages_do_not_import_tigrbl_auth_facade() -> None:
    split_packages = PYTHON_PACKAGE_LAYERS["capabilities"] | PYTHON_PACKAGE_LAYERS["protocols"]

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
