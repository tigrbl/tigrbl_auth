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
    "storage": {
        "tigrbl-identity-storage",
    },
    "contracts": {
        "tigrbl-identity-contracts",
        "tigrbl-release-contracts",
        "tigrbl-security-key-rotation-policy-contracts",
        "tigrbl-security-trust-contracts",
    },
    "bases": {
        "tigrbl-authz-policy-bases",
        "tigrbl-identity-authenticator-bases",
        "tigrbl-identity-model-bases",
        "tigrbl-jose-bases",
        "tigrbl-oauth-bases",
        "tigrbl-oidc-bases",
        "tigrbl-resource-server-bases",
        "tigrbl-security-provenance-bases",
        "tigrbl-security-trust-domain-bases",
    },
    "concrete": {
        "tigrbl-oauth-scope-matcher",
        "tigrbl-oidc-claims-concrete",
        "tigrbl-oidc-subject-strategy",
        "tigrbl-authz-policy-attributes-mapping",
        "tigrbl-authz-policy-combiner-default",
        "tigrbl-authz-policy-evaluators-default",
        "tigrbl-authz-policy-obligations-concrete",
        "tigrbl-authz-policy-rules-concrete",
        "tigrbl-identity-credentials-concrete",
        "tigrbl-identity-identities-concrete",
    },
    "providers": {
        "tigrbl-authenticator-api-key-local",
        "tigrbl-authenticator-client-secret-local",
        "tigrbl-authenticator-dpop-proof",
        "tigrbl-authenticator-federated-oidc",
        "tigrbl-authenticator-mtls-client-cert",
        "tigrbl-authenticator-otp-local",
        "tigrbl-authenticator-password-local",
        "tigrbl-authenticator-recovery-code-local",
        "tigrbl-authenticator-remote-introspection",
        "tigrbl-authenticator-service-key-local",
        "tigrbl-authenticator-session-local",
        "tigrbl-authenticator-webauthn-local",
        "tigrbl-identity-jose",
        "tigrbl-security-authorization-provenance-builder",
        "tigrbl-security-certificate-mtls",
        "tigrbl-security-auth-context-acr-basic",
        "tigrbl-security-auth-context-amr-basic",
        "tigrbl-security-claims-provider-local",
        "tigrbl-security-proof-dpop",
        "tigrbl-security-proof-pkce",
        "tigrbl-security-oidc-federation-provider",
        "tigrbl-security-signing-pqc",
        "tigrbl-security-subject-pairwise-provider",
        "tigrbl-security-webfinger-provider",
        "tigrbl-authz-resource-server-verifier",
        "tigrbl-security-dpop-cnf-binding-validator",
        "tigrbl-security-mtls-cnf-binding-validator",
        "tigrbl-security-sender-constraint-validator",
        "tigrbl-security-token-introspection-client",
        "tigrbl-security-token-jwks-cache",
    },
    "storage-runtime": {
        "tigrbl-identity-storage-runtime",
    },
    "capabilities": {
        "tigrbl-authn-credentials",
        "tigrbl-authz-policy-admin-gate",
        "tigrbl-authz-policy-authority-derivation-graph",
        "tigrbl-authz-policy-decision-engine",
        "tigrbl-authz-policy",
        "tigrbl-identity-admin",
        "tigrbl-identity-admin-auth-anomaly-detector",
        "tigrbl-identity-admin-control-plane",
        "tigrbl-identity-admin-relationship-graph",
        "tigrbl-identity-admin-trust-federation-graph",
        "tigrbl-identity-principals",
    },
    "protocols": {
        "tigrbl-auth-protocol-oauth",
        "tigrbl-auth-protocol-oidc",
        "tigrbl-auth-protocol-rp",
        "tigrbl-authz-resource-server",
    },
    "runtime": {
        "tigrbl-auth-plugin",
        "tigrbl-identity-author",
        "tigrbl-identity-cli",
        "tigrbl-identity-operator",
        "tigrbl-identity-runtime",
        "tigrbl-identity-server",
        "tigrbl-identity-testkit",
        "tigrbl-auth-release-certification",
    },
    "facade": {"tigrbl-auth"},
    "routers": {
        "tigrbl-auth-router-admin-gate",
    },
    "backend-apps": {
        "tigrbl-auth-backend-app-developer",
        "tigrbl-auth-backend-app-my-account",
        "tigrbl-auth-backend-app-platform-admin",
        "tigrbl-auth-backend-app-public",
        "tigrbl-auth-backend-app-resource-validation",
        "tigrbl-auth-backend-app-service-admin",
        "tigrbl-auth-backend-app-tenant-admin",
    },
    "tests": {
        "tigrbl-identity-testkit",
    },
    "examples": {
        "acme-notes-cli",
    },
    "deprecated": {
        "tigrbl-auth-protocol-oidc-backchannel-replay-store",
        "tigrbl-authz-policy-invariant-registry",
        "tigrbl-identity-admin-advanced-authenticator-registry",
        "tigrbl-identity-admin-federation-registry",
        "tigrbl-identity-admin-policy-registry",
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
    "storage": "01-storage",
    "contracts": "02-contracts",
    "bases": "05-bases",
    "concrete": "10-concrete",
    "providers": "20-providers",
    "storage-runtime": "30-storage-runtime",
    "capabilities": "40-capabilities",
    "protocols": "50-protocols",
    "runtime": "60-runtime",
    "facade": "70-facade",
    "routers": "80-routers",
    "backend-apps": "90-backend-apps",
    "tests": "120-tests",
    "examples": "110-examples",
    "deprecated": "deprecated",
}

# The layer directory is the package's authoritative ownership declaration.
# Build the inventory from live package metadata so adding a correctly placed
# standalone package cannot leave this boundary test's hand-maintained catalog
# stale. The assertions below still reject packages outside a declared layer,
# duplicate package names, and non-package children.
for _layer, _folder in PYTHON_LAYER_FOLDERS.items():
    _root = PKGS / _folder
    PYTHON_PACKAGE_LAYERS[_layer] = {
        child.name
        for child in _root.iterdir()
        if child.is_dir() and (child / "pyproject.toml").is_file()
    }

FRONTEND_LAYER_FOLDERS = {"100-uix-core", "105-ui"}

REQUIRED_PROTOCOL_MODULES = {
    "bindings.py",
    "claims.py",
    "compatibility.py",
    "errors.py",
    "features.py",
    "migrations.py",
    "schemas.py",
    "versions.py",
}

FRONTEND_WORKSPACES = {
    ROOT / "pkgs" / "100-uix-core" / "uix-core",
    ROOT / "pkgs" / "105-ui" / "admin-uix",
    ROOT / "pkgs" / "105-ui" / "demo-hub-uix",
    ROOT / "pkgs" / "105-ui" / "developer-uix",
    ROOT / "pkgs" / "105-ui" / "my-account-uix",
    ROOT / "pkgs" / "105-ui" / "platform-admin-uix",
    ROOT / "pkgs" / "105-ui" / "public-uix",
    ROOT / "pkgs" / "105-ui" / "rp",
    ROOT / "pkgs" / "105-ui" / "service-admin-uix",
    ROOT / "pkgs" / "105-ui" / "tenant-admin-uix",
}

LOWER_LAYER_FACADE_IMPORT_EXCEPTIONS: dict[str, str] = {}

JS_IMPORT_RE = re.compile(
    r"""(?:from\s+["'](?P<from>[^"']+)["']|import\s*\(\s*["'](?P<dynamic>[^"']+)["']\s*\)|require\s*\(\s*["'](?P<require>[^"']+)["']\s*\))"""
)


def _declared_python_packages() -> set[str]:
    return {path.parent.name for path in PKGS.rglob("pyproject.toml")}


def _package_dir(package_name: str) -> Path:
    matches = [
        path.parent
        for path in PKGS.rglob("pyproject.toml")
        if path.parent.name == package_name
    ]
    assert len(matches) == 1, (package_name, matches)
    return matches[0]


def _absolute_import_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
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
        specifier = (
            match.group("from") or match.group("dynamic") or match.group("require")
        )
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


def test_protocol_packages_use_explicit_import_surfaces() -> None:
    violations: list[str] = []
    protocol_root = PKGS / PYTHON_LAYER_FOLDERS["protocols"]

    for path in sorted(protocol_root.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and any(
                alias.name == "*" for alias in node.names
            ):
                violations.append(
                    f"{path.relative_to(ROOT)}:{node.lineno}: wildcard import"
                )

    assert violations == []


def test_protocol_packages_own_complete_versioned_specification_surfaces() -> None:
    violations: list[str] = []
    protocol_root = PKGS / PYTHON_LAYER_FOLDERS["protocols"]

    for package_dir in sorted(path for path in protocol_root.iterdir() if path.is_dir()):
        package_roots = sorted(
            path
            for path in (package_dir / "src").iterdir()
            if path.is_dir() and (path / "__init__.py").is_file()
        )
        if len(package_roots) != 1:
            violations.append(
                f"{package_dir.relative_to(ROOT)}: expected one import package, "
                f"found {len(package_roots)}"
            )
            continue
        missing = sorted(
            module
            for module in REQUIRED_PROTOCOL_MODULES
            if not (package_roots[0] / module).is_file()
        )
        if missing:
            violations.append(
                f"{package_dir.relative_to(ROOT)}: missing {', '.join(missing)}"
            )

    assert violations == []


def test_python_package_layers_match_filesystem_layout() -> None:
    assert set(PYTHON_LAYER_FOLDERS) == set(PYTHON_PACKAGE_LAYERS)

    for layer, packages in PYTHON_PACKAGE_LAYERS.items():
        expected_folder = PYTHON_LAYER_FOLDERS[layer]
        for package in packages:
            package_folder = _package_dir(package).relative_to(PKGS).parts[0]
            assert package_folder == expected_folder, (
                package,
                expected_folder,
                package_folder,
            )


def test_pkgs_tree_contains_only_declared_package_layers() -> None:
    allowed_layers = set(PYTHON_LAYER_FOLDERS.values()) | FRONTEND_LAYER_FOLDERS
    unexpected_layers = [
        path.name
        for path in sorted(PKGS.iterdir())
        if path.is_dir() and path.name not in allowed_layers
    ]

    assert unexpected_layers == []


def test_layer_children_are_packages_or_declared_frontend_workspaces() -> None:
    frontend_workspaces = {path.resolve() for path in FRONTEND_WORKSPACES}
    offenders: list[str] = []

    for layer_dir in sorted(path for path in PKGS.iterdir() if path.is_dir()):
        for child in sorted(path for path in layer_dir.iterdir() if path.is_dir()):
            if (child / "pyproject.toml").is_file():
                continue
            if child.resolve() in frontend_workspaces:
                continue
            offenders.append(str(child.relative_to(ROOT)).replace("\\", "/"))

    assert offenders == []


def test_lower_layer_packages_do_not_import_tigrbl_auth_facade() -> None:
    facade_consumers = {
        package
        for package in _declared_python_packages()
        if _package_facade_imports(package)
    }
    expected_upper_layers = (
        PYTHON_PACKAGE_LAYERS["facade"] | PYTHON_PACKAGE_LAYERS["backend-apps"]
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
    split_packages = (
        PYTHON_PACKAGE_LAYERS["capabilities"] | PYTHON_PACKAGE_LAYERS["protocols"]
    )

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
