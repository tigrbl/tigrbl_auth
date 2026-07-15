from __future__ import annotations

import ast
import importlib
import re
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"


COMPAT_TO_PREFERRED = {
    "tigrbl_identity_credentials": "tigrbl_authn_credentials",
    "tigrbl_identity_policy": "tigrbl_authz_policy",
    "tigrbl_identity_resource_server": "tigrbl_authz_resource_server",
    "tigrbl_identity_oauth": "tigrbl_auth_protocol_oauth",
    "tigrbl_identity_oidc": "tigrbl_auth_protocol_oidc",
    "tigrbl_identity_rp": "tigrbl_auth_protocol_rp",
}

DIST_TO_IMPORT_ROOT = {
    "tigrbl-authn-credentials": "tigrbl_authn_credentials",
    "tigrbl-authz-policy-admin-gate": "tigrbl_authz_policy_admin_gate",
    "tigrbl-authz-policy": "tigrbl_authz_policy",
    "tigrbl-authz-resource-server": "tigrbl_authz_resource_server",
    "tigrbl-authz-resource-server-verifier": "tigrbl_authz_resource_server_verifier",
    "tigrbl-security-dpop-cnf-binding-validator": "tigrbl_security_dpop_cnf_binding_validator",
    "tigrbl-security-mtls-cnf-binding-validator": "tigrbl_security_mtls_cnf_binding_validator",
    "tigrbl-security-sender-constraint-validator": "tigrbl_security_sender_constraint_validator",
    "tigrbl-security-token-introspection-client": "tigrbl_security_token_introspection_client",
    "tigrbl-security-token-jwks-cache": "tigrbl_security_token_jwks_cache",
    "tigrbl-auth-protocol-oauth": "tigrbl_auth_protocol_oauth",
    "tigrbl-auth-protocol-oidc": "tigrbl_auth_protocol_oidc",
    "tigrbl-auth-protocol-rp": "tigrbl_auth_protocol_rp",
}

DEPRECATED_DIST_TO_IMPORT_ROOT = {
    "tigrbl-identity-credentials": "tigrbl_identity_credentials",
    "tigrbl-identity-policy": "tigrbl_identity_policy",
    "tigrbl-identity-resource-server": "tigrbl_identity_resource_server",
    "tigrbl-identity-oauth": "tigrbl_identity_oauth",
    "tigrbl-identity-oidc": "tigrbl_identity_oidc",
    "tigrbl-identity-rp": "tigrbl_identity_rp",
}

DEPRECATED_MODULE_CANONICAL_IMPORT_ROOT = {
    "tigrbl_identity_credentials/authenticators.py": "tigrbl_identity_server.security.auth",
    "tigrbl_identity_credentials/_operator_store.py": "tigrbl_identity_storage_runtime.operator_store",
    "tigrbl_identity_credentials/_token_service/__init__.py": "tigrbl_identity_runtime.token_service",
    "tigrbl_identity_credentials/_token_service/coder.py": "tigrbl_identity_jose.jwt_coder",
    "tigrbl_identity_credentials/_token_service/operator.py": "tigrbl_identity_storage_runtime.session_service",
    "tigrbl_identity_credentials/_token_service/persistence.py": "tigrbl_identity_storage_runtime.token_persistence",
    "tigrbl_identity_credentials/_token_service/runtime.py": "tigrbl_identity_jose.jwt_runtime",
    "tigrbl_identity_credentials/audit_service.py": "tigrbl_identity_storage_runtime.audit",
    "tigrbl_identity_credentials/operator_service.py": "tigrbl_identity_storage_runtime.resource_service",
    "tigrbl_identity_credentials/session_service.py": "tigrbl_identity_storage_runtime.session_service",
    "tigrbl_identity_credentials/token_service.py": "tigrbl_identity_runtime.token_service",
    "tigrbl_identity_oidc/discovery_service.py": "tigrbl_identity_cli.discovery_service",
    "tigrbl_identity_policy/_certification/__init__.py": "tigrbl_auth_release_certification.certification",
    "tigrbl_identity_policy/_certification/authorization.py": "tigrbl_auth_release_certification.certification.authorization",
    "tigrbl_identity_policy/_certification/base.py": "tigrbl_auth_release_certification.certification.base",
    "tigrbl_identity_policy/_certification/crypto.py": "tigrbl_auth_release_certification.certification.crypto",
    "tigrbl_identity_policy/_certification/isolation.py": "tigrbl_auth_release_certification.certification.isolation",
    "tigrbl_identity_policy/_certification/observability.py": "tigrbl_auth_release_certification.certification.observability",
    "tigrbl_identity_policy/_certification/runtime.py": "tigrbl_auth_release_certification.certification.runtime",
    "tigrbl_identity_policy/_release_posture/__init__.py": "tigrbl_auth_release_certification.release_posture",
    "tigrbl_identity_policy/_release_posture/disclosure.py": "tigrbl_auth_release_certification.release_posture.disclosure",
    "tigrbl_identity_policy/_release_posture/models.py": "tigrbl_auth_release_certification.release_posture.models",
    "tigrbl_identity_policy/_release_posture/provenance.py": "tigrbl_auth_release_certification.release_posture.provenance",
    "tigrbl_identity_policy/_release_posture/summary.py": "tigrbl_auth_release_certification.release_posture.summary",
    "tigrbl_identity_policy/_release_posture/transport.py": "tigrbl_auth_release_certification.release_posture.transport",
    "tigrbl_identity_policy/admin_gate.py": "tigrbl_authz_policy.admin_gate",
    "tigrbl_identity_policy/_admin_gate/__init__.py": "tigrbl_authz_policy.admin_gate",
    "tigrbl_identity_policy/_admin_gate/constants.py": "tigrbl_authz_policy.admin_gate",
    "tigrbl_identity_policy/_admin_gate/gate.py": "tigrbl_authz_policy.admin_gate",
    "tigrbl_identity_policy/_admin_gate/helpers.py": "tigrbl_authz_policy.admin_gate",
    "tigrbl_identity_policy/certification.py": "tigrbl_auth_release_certification.certification",
    "tigrbl_identity_policy/invariants.py": "tigrbl_authz_policy",
    "tigrbl_identity_policy/release_posture.py": "tigrbl_auth_release_certification.release_posture",
}

NON_TAXONOMY_CANONICAL_ROOTS = {
    "tigrbl_auth_release_certification",
    "tigrbl_authz_policy_admin_gate",
    "tigrbl_authz_policy_attributes_mapping",
    "tigrbl_authz_policy_combiner_default",
    "tigrbl_authz_policy_evaluators_default",
    "tigrbl_authz_policy_obligations_concrete",
    "tigrbl_authz_policy_rules_concrete",
    "tigrbl_identity_credentials_concrete",
    "tigrbl_identity_identities_concrete",
    "tigrbl_identity_jose",
    "tigrbl_identity_runtime",
    "tigrbl_identity_server",
    "tigrbl_identity_storage",
    "tigrbl_identity_storage_runtime",
    "tigrbl_security_authorization_provenance_builder",
    "tigrbl_security_key_rotation_policy_contracts",
}

CANONICAL_MODULE_RE = re.compile(r'_CANONICAL_MODULE\s*=\s*"([^"]+)"')


def _install_package_src_paths() -> None:
    for src in PKGS.rglob("src"):
        value = str(src)
        if value not in sys.path:
            sys.path.insert(0, value)


def _absolute_imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            imports.add(node.module.split(".")[0])
    return imports


def _package_path(dist_name: str) -> Path:
    matches = sorted(PKGS.glob(f"**/{dist_name}/pyproject.toml"))
    assert matches, dist_name
    return matches[0].parent


def test_deprecated_taxonomy_roots_reexport_preferred_surfaces() -> None:
    _install_package_src_paths()

    for compat_root, preferred_root in COMPAT_TO_PREFERRED.items():
        preferred = importlib.import_module(preferred_root)
        compat = importlib.import_module(compat_root)

        assert set(preferred.__all__) == set(compat.__all__)
        for name in preferred.__all__:
            assert getattr(preferred, name) is getattr(compat, name), (preferred_root, name)


def test_preferred_taxonomy_package_metadata_is_declared() -> None:
    for dist_name, import_root in DIST_TO_IMPORT_ROOT.items():
        pyproject = _package_path(dist_name) / "pyproject.toml"
        metadata = tomllib.loads(pyproject.read_text(encoding="utf-8"))

        assert metadata["project"]["name"] == dist_name
        assert metadata["tool"]["poetry"]["packages"] == [{"include": import_root, "from": "src"}]


def test_deprecated_taxonomy_package_metadata_lives_under_deprecated_folder() -> None:
    for dist_name, import_root in DEPRECATED_DIST_TO_IMPORT_ROOT.items():
        package_path = PKGS / "deprecated" / dist_name
        pyproject = package_path / "pyproject.toml"
        metadata = tomllib.loads(pyproject.read_text(encoding="utf-8"))

        assert not (PKGS / dist_name).exists()
        assert metadata["project"]["name"] == dist_name
        assert metadata["tool"]["poetry"]["packages"] == [{"include": import_root, "from": "src"}]
        assert (package_path / "src" / import_root).is_dir()


def test_deprecated_taxonomy_roots_delegate_to_preferred_roots() -> None:
    deprecated_imports = set(COMPAT_TO_PREFERRED)

    for dist_name, import_root in DEPRECATED_DIST_TO_IMPORT_ROOT.items():
        package_root = PKGS / "deprecated" / dist_name / "src" / import_root
        preferred_root = COMPAT_TO_PREFERRED[import_root]
        for path in package_root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            relative_module = path.relative_to(package_root).as_posix()
            relative_key = f"{import_root}/{relative_module}"
            expected_root = DEPRECATED_MODULE_CANONICAL_IMPORT_ROOT.get(relative_key)
            match = CANONICAL_MODULE_RE.search(text)
            assert match, path
            canonical_module = match.group(1)
            canonical_root = canonical_module.split(".")[0]

            assert "_CANONICAL_MODULE" in text, path
            if expected_root is None:
                assert (
                    canonical_module == preferred_root
                    or canonical_module.startswith(f"{preferred_root}.")
                    or canonical_root in NON_TAXONOMY_CANONICAL_ROOTS
                ), path
            else:
                assert canonical_module == expected_root, path
            assert canonical_root not in deprecated_imports, path
            assert canonical_root != "tigrbl_auth", path
            assert _absolute_imports(path) <= {"__future__", "importlib", "warnings"}, path


def test_authn_authz_protocol_roots_do_not_import_deprecated_roots() -> None:
    deprecated_imports = set(COMPAT_TO_PREFERRED)

    for import_root in DIST_TO_IMPORT_ROOT.values():
        package_root = next(PKGS.glob(f"**/src/{import_root}"))
        for path in package_root.rglob("*.py"):
            imports = _absolute_imports(path)
            assert "tigrbl_auth" not in imports, path
            assert imports.isdisjoint(deprecated_imports), path
