from __future__ import annotations

import ast
import importlib
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]

MIGRATED_RELEASE_PATHS = [
    ROOT / "pkgs/40-capabilities/tigrbl-authn-credentials/src/tigrbl_authn_credentials/authenticators.py",
    ROOT / "pkgs/40-capabilities/tigrbl-authn-credentials/src/tigrbl_authn_credentials/backends.py",
    ROOT / "pkgs/50-protocols/tigrbl-auth-protocol-oidc/src/tigrbl_auth_protocol_oidc/standards/discovery.py",
    ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/auth_code/_op.py",
    ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/auth_session/_op.py",
    ROOT / "pkgs/30-storage-runtime/tigrbl-identity-storage-runtime/src/tigrbl_identity_storage_runtime/client_registration.py",
    ROOT / "pkgs/30-storage-runtime/tigrbl-identity-storage-runtime/src/tigrbl_identity_storage_runtime/device_authorization.py",
    ROOT / "pkgs/30-storage-runtime/tigrbl-identity-storage-runtime/src/tigrbl_identity_storage_runtime/logout.py",
    ROOT / "pkgs/30-storage-runtime/tigrbl-identity-storage-runtime/src/tigrbl_identity_storage_runtime/par.py",
    ROOT / "pkgs/30-storage-runtime/tigrbl-identity-storage-runtime/src/tigrbl_identity_storage_runtime/token_exchange.py",
    ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/revoked_token/_op.py",
    ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/token_record/_op.py",
    ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/user/_table.py",
    ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/realm/_table.py",
    ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/tenant/_table.py",
    ROOT / "pkgs/40-capabilities/tigrbl-identity-admin/src/tigrbl_identity_admin/bootstrap.py",
    ROOT / "pkgs/60-runtime/tigrbl-identity-runtime/src/tigrbl_identity_runtime/backends.py",
    ROOT / "pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/security/auth.py",
    ROOT / "pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/security/security_deps.py",
    ROOT / "pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/security/handler_records.py",
    ROOT / "pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/security/user_lookup.py",
]

FORBIDDEN_FRAMEWORK_EXPORTS = {
    "IntegrityError",
    "Select",
    "delete",
    "or_",
    "select",
}
FORBIDDEN_DB_METHODS = {
    "add",
    "commit",
    "delete",
    "execute",
    "flush",
    "refresh",
    "rollback",
    "scalar",
    "scalars",
}

SEMANTIC_FACADE_PATHS = [
    ROOT / "pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/token_exchange.py",
    ROOT / "pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/dpop.py",
    ROOT / "pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/oauth_security_bcp.py",
    ROOT / "pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/_rfc8693/__init__.py",
    ROOT / "pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/_dpop/__init__.py",
    ROOT / "pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/_rfc9700/__init__.py",
    ROOT / "pkgs/40-capabilities/tigrbl-authz-policy-admin-gate/src/tigrbl_authz_policy_admin_gate/gate.py",
    ROOT / "pkgs/40-capabilities/tigrbl-authz-policy/src/tigrbl_authz_policy/assurance.py",
    ROOT / "pkgs/40-capabilities/tigrbl-authz-policy/src/tigrbl_authz_policy/authority.py",
    ROOT / "pkgs/40-capabilities/tigrbl-authz-policy/src/tigrbl_authz_policy/control_plane.py",
    ROOT / "pkgs/40-capabilities/tigrbl-authz-policy/src/tigrbl_authz_policy/delegation.py",
    ROOT / "pkgs/40-capabilities/tigrbl-authz-policy/src/tigrbl_authz_policy/governance_extension.py",
    ROOT / "pkgs/40-capabilities/tigrbl-authz-policy/src/tigrbl_authz_policy/abac.py",
    ROOT / "pkgs/40-capabilities/tigrbl-authz-policy/src/tigrbl_authz_policy/delegated_admin.py",
    ROOT / "pkgs/40-capabilities/tigrbl-authz-policy/src/tigrbl_authz_policy/policy_engine.py",
    ROOT / "pkgs/40-capabilities/tigrbl-authz-policy/src/tigrbl_authz_policy/rbac.py",
    ROOT / "pkgs/40-capabilities/tigrbl-authz-policy/src/tigrbl_authz_policy/service_identity_registry.py",
    ROOT / "pkgs/60-runtime/tigrbl-identity-runtime/src/tigrbl_identity_runtime/deployment.py",
    ROOT / "pkgs/60-runtime/tigrbl-identity-runtime/src/tigrbl_identity_runtime/surfaces.py",
    ROOT / "pkgs/60-runtime/tigrbl-identity-runtime/src/tigrbl_identity_runtime/_deployment/__init__.py",
    ROOT / "pkgs/60-runtime/tigrbl-identity-runtime/src/tigrbl_identity_runtime/_surfaces/__init__.py",
    ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/persistence.py",
    ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/operator_store.py",
    ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/_sync.py",
    ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/_operator_store/__init__.py",
    ROOT / "pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/surfaces.py",
    ROOT / "pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/_surfaces/__init__.py",
    ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/resource_service.py",
    ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/_resource_service/__init__.py",
    ROOT / "pkgs/60-runtime/tigrbl-identity-operator/src/tigrbl_identity_operator/uix/admin_console.py",
    ROOT / "pkgs/60-runtime/tigrbl-identity-operator/src/tigrbl_identity_operator/uix/_admin_console/__init__.py",
]

PERSISTENCE_HELPER_PATHS = [
    ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/token_record/_lifecycle.py",
    ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/auth_session/_lifecycle.py",
    ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/logout_state/_lifecycle.py",
    ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/client_registration/_lifecycle.py",
    ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/consent/_lifecycle.py",
    ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/audit_event.py",
]

SYNC_COMPAT_PATHS = [
    ROOT / "pkgs/20-providers/tigrbl-identity-jose/src/tigrbl_identity_jose/jwt_runtime.py",
    ROOT / "pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/_dpop/primitives.py",
    ROOT / "pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/jwtoken.py",
    ROOT / "pkgs/20-providers/tigrbl-identity-jose/src/tigrbl_identity_jose/standards/rfc8037.py",
    ROOT / "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/_sync.py",
]

ASYNC_REQUEST_TOKEN_PATHS = [
    ROOT / "pkgs/40-capabilities/tigrbl-authn-credentials/src/tigrbl_authn_credentials/authenticators.py",
    ROOT / "pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/token_exchange.py",
    ROOT / "pkgs/50-protocols/tigrbl-auth-protocol-oidc/src/tigrbl_auth_protocol_oidc/standards/userinfo.py",
    ROOT / "pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/security/auth.py",
    ROOT / "pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/security/security_deps.py",
]

AUTHN_TOKEN_SIGNER_PATHS = [
    ROOT / "pkgs/20-providers/tigrbl-identity-jose/src/tigrbl_identity_jose/jwt_runtime.py",
    ROOT / "pkgs/20-providers/tigrbl-identity-jose/src/tigrbl_identity_jose/jwt_coder.py",
    ROOT / "pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/jwtoken.py",
]


def _root_name(node: ast.AST) -> str | None:
    current = node
    while isinstance(current, ast.Attribute):
        current = current.value
    if isinstance(current, ast.Name):
        return current.id
    return None


def _enclosing_function_name(node: ast.AST) -> str | None:
    parent = getattr(node, "_parent", None)
    while parent is not None:
        if isinstance(parent, (ast.AsyncFunctionDef, ast.FunctionDef)):
            return parent.name
        parent = getattr(parent, "_parent", None)
    return None


def _violations(path: Path, *, allow_session_transaction_boundary: bool = False) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            setattr(child, "_parent", parent)
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module == "sqlalchemy" or module.startswith("sqlalchemy."):
                names = ", ".join(alias.name for alias in node.names)
                found.append(f"{path}:{node.lineno}: direct SQLAlchemy import {names}")
            if module in {"tigrbl_auth.framework", "tigrbl_identity_server.framework"}:
                leaked = sorted(
                    alias.name for alias in node.names if alias.name in FORBIDDEN_FRAMEWORK_EXPORTS
                )
                if leaked:
                    found.append(
                        f"{path}:{node.lineno}: framework DB primitive import {', '.join(leaked)}"
                    )
        elif isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id == "select":
                found.append(f"{path}:{node.lineno}: direct select() call")
            elif (
                isinstance(func, ast.Attribute)
                and func.attr in FORBIDDEN_DB_METHODS
                and _root_name(func) in {"db", "session"}
            ):
                if (
                    allow_session_transaction_boundary
                    and path.name == "token_records.py"
                    and func.attr in {"commit", "rollback"}
                    and _root_name(func) == "session"
                    and _enclosing_function_name(node) == "_session"
                ):
                    continue
                found.append(f"{path}:{node.lineno}: direct {_root_name(func)}.{func.attr}() call")
    return found


@pytest.mark.unit
def test_migrated_release_paths_use_tigrbl_handlers_not_direct_db_or_sqla() -> None:
    violations: list[str] = []
    for path in MIGRATED_RELEASE_PATHS:
        if not path.exists():
            violations.append(f"{path}: migrated release path is missing")
            continue
        violations.extend(_violations(path))

    assert violations == []


@pytest.mark.unit
def test_package_surfaces_do_not_use_generated_part_modules() -> None:
    violations: list[str] = []
    for base in (ROOT / "pkgs",):
        for path in base.rglob("part_*.py"):
            violations.append(f"{path}: generated part module remains in a package surface")

    assert violations == []


@pytest.mark.unit
def test_semantic_facades_do_not_use_split_exec_loaders() -> None:
    violations: list[str] = []
    for path in SEMANTIC_FACADE_PATHS:
        if not path.exists():
            violations.append(f"{path}: semantic facade path is missing")
            continue
        source = path.read_text(encoding="utf-8")
        if "exec(compile(" in source:
            violations.append(f"{path}: release-path split loader uses exec(compile(...))")

    assert violations == []


@pytest.mark.unit
def test_package_code_does_not_use_exec_compile_split_loaders() -> None:
    violations: list[str] = []
    for base in (ROOT / "pkgs",):
        for path in base.rglob("*.py"):
            source = path.read_text(encoding="utf-8")
            if "exec(compile(" in source:
                violations.append(f"{path}: package code uses exec(compile(...)) split loading")

    assert violations == []


@pytest.mark.unit
def test_framework_public_surface_is_not_supported() -> None:
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("tigrbl_identity_server.framework")


@pytest.mark.unit
def test_storage_persistence_helpers_use_handlers_not_direct_queries() -> None:
    violations: list[str] = []
    for path in PERSISTENCE_HELPER_PATHS:
        if not path.exists():
            violations.append(f"{path}: persistence helper path is missing")
            continue
        violations.extend(_violations(path, allow_session_transaction_boundary=True))

    assert violations == []


@pytest.mark.unit
def test_sync_compat_surfaces_do_not_spawn_private_event_loop_threads() -> None:
    violations: list[str] = []
    forbidden_snippets = ("Thread(", "threading.Thread(", "asyncio.new_event_loop(")
    for path in SYNC_COMPAT_PATHS:
        if not path.exists():
            violations.append(f"{path}: sync compatibility path is missing")
            continue
        source = path.read_text(encoding="utf-8")
        for snippet in forbidden_snippets:
            if snippet in source:
                violations.append(f"{path}: sync compatibility surface uses {snippet}")

    assert violations == []


@pytest.mark.unit
def test_async_request_token_paths_do_not_call_sync_jwt_default() -> None:
    violations: list[str] = []
    for path in ASYNC_REQUEST_TOKEN_PATHS:
        if not path.exists():
            violations.append(f"{path}: async request token path is missing")
            continue
        source = path.read_text(encoding="utf-8")
        if "JWTCoder.default()" in source:
            violations.append(f"{path}: async request path calls JWTCoder.default()")

    assert violations == []


@pytest.mark.unit
def test_authn_token_signers_do_not_register_oauth_introspection_state() -> None:
    violations: list[str] = []
    forbidden_snippets = (
        "register_token",
        "register_token_async",
        ".standards.introspection",
        "standards.oauth2.introspection",
    )
    for path in AUTHN_TOKEN_SIGNER_PATHS:
        if not path.exists():
            violations.append(f"{path}: authn token signer path is missing")
            continue
        source = path.read_text(encoding="utf-8")
        for snippet in forbidden_snippets:
            if snippet in source:
                violations.append(f"{path}: authn token signer owns OAuth introspection state via {snippet}")

    assert violations == []
