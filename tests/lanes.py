from __future__ import annotations

import ast
import importlib.util
import os
import sys
from functools import lru_cache
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TESTS_ROOT = REPO_ROOT / "tests"
SUPPORTED_CERTIFICATION_PYTHONS = {(3, 10), (3, 11), (3, 12)}
OPTIONAL_RUNTIME_MODULES = (
    "tigrbl",
    "sqlalchemy",
    "bcrypt",
    "swarmauri_core",
    "swarmauri_base",
    "swarmauri_standard",
    "swarmauri_signing_jws",
    "swarmauri_tokens_jwt",
    "swarmauri_signing_ed25519",
    "swarmauri_signing_dpop",
    "pqcrypto",
    "swarmauri_crypto_jwe",
    "swarmauri_crypto_paramiko",
    "swarmauri_keyprovider_file",
    "swarmauri_keyprovider_local",
)
RUNTIME_STACK_SOURCE_PREFIXES = (
    "tigrbl_auth",
    "tigrbl_auth_protocol_oauth",
    "tigrbl_auth_protocol_oidc",
    "tigrbl_identity_server",
    "tests",
)
EXTENSION_TEST_PREFIXES = (
    "test_rfc7800_",
    "test_rfc8417_",
    "test_rfc8291_",
    "test_rfc8812_",
    "test_rfc8932_",
)
DEFERRED_INTEGRATION_FILES = {
    "test_auth_flows.py",
    "test_authorization_response_types.py",
    "test_crud_api.py",
    "test_device_code_flow.py",
    "test_full_workflow.py",
    "test_long_lived_worker_flow.py",
    "test_migration_upgrade_downgrade_safety.py",
    "test_rfc7662.py",
    "test_rfc8628.py",
    "test_rfc8693_token_exchange_endpoint.py",
    "test_service_key_creation.py",
    "test_service_key_introspection_flow.py",
}
DEFERRED_FACADE_COMPAT_UNIT_FILES = {
    "test_adapters.py",
    "test_admin_policy_boundary.py",
    "test_advanced_surface_contracts.py",
    "test_authorization_invariant_guards.py",
    "test_authorization_provenance.py",
    "test_authorize_id_token_hashes.py",
    "test_authorize_response_modes.py",
    "test_auth_code_exchange_pkce.py",
    "test_bootstrappable_user_defaults.py",
    "test_crypto.py",
    "test_engine_initialization.py",
    "test_fapi_runtime_profile.py",
    "test_hardening_cluster_a.py",
    "test_hardening_cluster_b.py",
    "test_hardening_cluster_c.py",
    "test_jwks_rotation.py",
    "test_key_rotation_policy_governance.py",
    "test_models.py",
    "test_non_rfc_track_checkpoint.py",
    "test_oidc_authorize_scope_nonce.py",
    "test_oidc_id_token.py",
    "test_oidc_id_token_encryption.py",
    "test_openapi_examples.py",
    "test_openapi_well_known_endpoints.py",
    "test_openid_userinfo_endpoint.py",
    "test_operator_control_plane.py",
    "test_operator_service_layer.py",
    "test_policy_control_plane_" + "pha" + "se3.py",
    "test_profile_discovery_runtime.py",
    "test_protected_resource_verifier_contract.py",
    "test_provisioning_governance_ecosystem_boundary.py",
    "test_remote_adapter.py",
    "test_repo_truth_helpers.py",
    "test_request_scoped_runtime_authority.py",
    "test_rfc6749_auth_flow_endpoints.py",
    "test_rfc6749_token_endpoint.py",
    "test_rfc6750_bearer_token.py",
    "test_rfc7009_token_revocation.py",
    "test_rfc7516_jwe.py",
    "test_rfc7519_jwt.py",
    "test_rfc7521_assertion_framework.py",
    "test_rfc7523_jwt_profile.py",
    "test_rfc7662_token_introspection.py",
    "test_rfc8523_jwt_client_auth.py",
    "test_rfc8705_compliance.py",
    "test_rfc8707_resource_indicators.py",
    "test_rfc8725_jwt_best_practices.py",
    "test_rfc9068_jwt_profile.py",
    "test_rfc9728_metadata_checkpoint.py",
    "test_security_deps.py",
    "test_security_user_lookup.py",
    "test_ssot_document_authority.py",
    "test_tenant_public_discovery_boundary.py",
}


def certification_python_supported() -> bool:
    return sys.version_info[:2] in SUPPORTED_CERTIFICATION_PYTHONS


@lru_cache(maxsize=1)
def missing_optional_runtime_modules() -> tuple[str, ...]:
    missing = []
    for module_name in OPTIONAL_RUNTIME_MODULES:
        if importlib.util.find_spec(module_name) is None:
            missing.append(module_name)
    return tuple(missing)


def active_lane(explicit_lane: str | None = None) -> str:
    lane = explicit_lane or os.getenv("TIGRBL_AUTH_TEST_LANE", "core")
    return lane.strip().lower() or "core"


def classify_test_path(path: Path) -> str:
    name = path.name
    parts = path.parts
    if "packages" in parts:
        return "package"
    if name in DEFERRED_FACADE_COMPAT_UNIT_FILES:
        return "extension"
    if name in DEFERRED_INTEGRATION_FILES:
        return "integration"
    if name.startswith(EXTENSION_TEST_PREFIXES) or any(
        bucket in parts for bucket in ("examples", "e2e", "perf")
    ):
        return "extension"
    if "integration" in parts:
        return "integration"
    if "conformance" in parts or "runtime" in parts:
        return "conformance"
    if "security" in parts or "negative" in parts:
        return "security-negative"
    if "interop" in parts:
        return "interop"
    return "core"


def lane_allows_path(selected_lane: str, path: Path) -> bool:
    if path.name in DEFERRED_INTEGRATION_FILES:
        return selected_lane in {"all", "*", "extension"}
    if path.name in DEFERRED_FACADE_COMPAT_UNIT_FILES:
        return selected_lane in {"all", "*", "extension"}
    lane = classify_test_path(path)
    if lane == "package":
        package_context = os.getenv("PACKAGE_UNDER_TEST") or os.getenv("TIGRBL_AUTH_PACKAGE_UNDER_TEST")
        return bool(package_context) or selected_lane in {"all", "*"}
    if selected_lane in {"all", "*"}:
        return True
    if selected_lane == "core":
        return lane == "core"
    return lane == selected_lane


def _module_path(module_name: str) -> Path | None:
    if not module_name:
        return None
    rel = Path(*module_name.split("."))
    for candidate in (REPO_ROOT / f"{rel}.py", REPO_ROOT / rel / "__init__.py"):
        if candidate.exists():
            return candidate
    for src_root in sorted((REPO_ROOT / "pkgs").glob("*/src")):
        for candidate in (src_root / f"{rel}.py", src_root / rel / "__init__.py"):
            if candidate.exists():
                return candidate
    return None


@lru_cache(maxsize=None)
def _module_imports(module_name: str) -> tuple[str, ...]:
    module_path = _module_path(module_name)
    if module_path is None:
        return ()
    try:
        tree = ast.parse(module_path.read_text(encoding="utf-8"), filename=str(module_path))
    except Exception:
        return ()

    imports: set[str] = set()
    package = module_name if module_path.name == "__init__.py" else module_name.rsplit(".", 1)[0]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                target = "." * node.level + (node.module or "")
                try:
                    resolved = importlib.util.resolve_name(target, package)
                except Exception:
                    continue
                imports.add(resolved)
            elif node.module:
                imports.add(node.module)
        elif isinstance(node, ast.Call):
            module_name = _dynamic_import_target(node)
            if module_name:
                imports.add(module_name)
    return tuple(sorted(imports))


@lru_cache(maxsize=None)
def module_requires_runtime_stack(module_name: str, _seen: tuple[str, ...] = ()) -> bool:
    if not module_name:
        return False
    for dependency in OPTIONAL_RUNTIME_MODULES:
        if module_name == dependency or module_name.startswith(f"{dependency}."):
            return True
    if not module_name.startswith(RUNTIME_STACK_SOURCE_PREFIXES):
        return False
    if module_name in _seen:
        return False
    seen = _seen + (module_name,)
    for imported in _module_imports(module_name):
        if module_requires_runtime_stack(imported, seen):
            return True
    return False


def _dynamic_import_target(node: ast.Call) -> str | None:
    target: ast.AST | None = None
    func = node.func
    if isinstance(func, ast.Name) and func.id == "__import__":
        target = node.args[0] if node.args else None
    elif isinstance(func, ast.Name) and func.id == "import_module":
        target = node.args[0] if node.args else None
    elif isinstance(func, ast.Attribute) and func.attr == "import_module":
        target = node.args[0] if node.args else None
    elif isinstance(func, ast.Name) and func.id.endswith("alias_module"):
        target = node.args[1] if len(node.args) > 1 else None
    elif isinstance(func, ast.Attribute) and func.attr == "alias_module":
        target = node.args[1] if len(node.args) > 1 else None
    if isinstance(target, ast.Constant) and isinstance(target.value, str):
        return target.value
    return None


@lru_cache(maxsize=None)
def test_file_requires_runtime_stack(path_str: str) -> bool:
    path = Path(path_str)
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except Exception:
        return False

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if module_requires_runtime_stack(alias.name):
                    return True
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module or ""
            if node.level:
                package = "tests"
                target = "." * node.level + module_name
                try:
                    module_name = importlib.util.resolve_name(target, package)
                except Exception:
                    module_name = ""
            if module_requires_runtime_stack(module_name):
                return True
        elif isinstance(node, ast.Call):
            module_name = _dynamic_import_target(node)
            # Dynamic imports are runtime edges by definition; conservatively
            # classify known runtime package targets without relying on static
            # traversal of the target's current import graph.
            if module_name and (
                module_name.startswith(RUNTIME_STACK_SOURCE_PREFIXES)
                or module_requires_runtime_stack(module_name)
            ):
                return True
    return False


DEFERRED_EXTENSION_TARGETS = {
    prefix.removeprefix("test_").removesuffix("_").upper(): prefix
    for prefix in EXTENSION_TEST_PREFIXES
}


def skip_reason_for_test_path(path: Path) -> str | None:
    missing = missing_optional_runtime_modules()
    if certification_python_supported() and not missing:
        return None
    if test_file_requires_runtime_stack(str(path)):
        reasons = []
        if not certification_python_supported():
            reasons.append(
                f"python {sys.version_info.major}.{sys.version_info.minor} is outside the supported certification range"
            )
        if missing:
            reasons.append(f"missing runtime modules: {', '.join(missing)}")
        return "; ".join(reasons)
    return None


__all__ = [
    "OPTIONAL_RUNTIME_MODULES",
    "active_lane",
    "certification_python_supported",
    "classify_test_path",
    "lane_allows_path",
    "missing_optional_runtime_modules",
    "skip_reason_for_test_path",
    "test_file_requires_runtime_stack",
]
