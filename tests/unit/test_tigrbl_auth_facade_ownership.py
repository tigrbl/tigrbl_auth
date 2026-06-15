from __future__ import annotations

import hashlib
import importlib
import sys
from contextlib import contextmanager
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"
LEGACY_ROOT = ROOT / "tigrbl_auth"
LARGE_FILE_THRESHOLD = 400


SPLIT_MODULE_PREFIXES = (
    "tigrbl_auth_protocol_",
    "tigrbl_authn_",
    "tigrbl_authz_",
    "tigrbl_identity_",
)


FACADE_MODULES = {
    "tigrbl_auth.api.surfaces": "tigrbl_identity_server.surfaces",
    "tigrbl_auth.config.deployment": "tigrbl_identity_runtime.deployment",
    "tigrbl_auth.config.surfaces": "tigrbl_identity_runtime.surfaces",
    "tigrbl_auth.framework": "tigrbl_identity_server.framework",
    "tigrbl_auth.rfc.rfc8693": "tigrbl_auth_protocol_oauth.standards.rfc8693",
    "tigrbl_auth.security.admin_gate": "tigrbl_authz_policy.admin_gate",
    "tigrbl_auth.security.certification": "tigrbl_authz_policy.certification",
    "tigrbl_auth.services._operator_store": "tigrbl_identity_storage.operator_store",
    "tigrbl_auth.services.advanced_identity_plane": "tigrbl_identity_admin.advanced_identity_plane",
    "tigrbl_auth.services.governance_extension_plane": "tigrbl_authz_policy.governance_extension",
    "tigrbl_auth.services.policy_control_plane": "tigrbl_authz_policy.control_plane",
    "tigrbl_auth.services.operator_service": "tigrbl_identity_operator.operator_service",
    "tigrbl_auth.standards.oauth2.dpop": "tigrbl_auth_protocol_oauth.standards.dpop",
    "tigrbl_auth.standards.oauth2.rfc9700": "tigrbl_auth_protocol_oauth.standards.rfc9700",
    "tigrbl_auth.services.release_posture_plane": "tigrbl_authz_policy.release_posture",
    "tigrbl_auth.services.token_service": "tigrbl_authn_credentials.token_service",
    "tigrbl_auth.release_signing": "tigrbl_identity_jose.release_signing",
    "tigrbl_auth.ops.register": "tigrbl_auth_protocol_oauth.ops.register",
    "tigrbl_auth.services.authorization_provenance": "tigrbl_identity_operator.authorization_provenance",
    "tigrbl_auth.services.audit_service": "tigrbl_identity_operator.audit_service",
    "tigrbl_auth.uix.admin_console": "tigrbl_identity_operator.uix.admin_console",
}

EXECUTABLE_FACADE_MODULES = {
    "tigrbl_auth.ops.token": "tigrbl_auth_protocol_oauth.ops.token",
}

INSTALLED_FACADE_MODULES = {
    key: FACADE_MODULES[key]
    for key in (
        "tigrbl_auth.framework",
        "tigrbl_auth.services._operator_store",
        "tigrbl_auth.services.governance_extension_plane",
        "tigrbl_auth.services.policy_control_plane",
        "tigrbl_auth.services.operator_service",
        "tigrbl_auth.release_signing",
        "tigrbl_auth.services.authorization_provenance",
        "tigrbl_auth.services.audit_service",
    )
}


@contextmanager
def source_tree_paths_first():
    original_path = list(sys.path)
    removed_modules = {
        name: module
        for name, module in sys.modules.items()
        if name == "tigrbl_auth"
        or name.startswith("tigrbl_auth.")
        or name.startswith(SPLIT_MODULE_PREFIXES)
    }
    for name in list(removed_modules):
        sys.modules.pop(name, None)
    try:
        root_value = str(ROOT)
        sys.path = [value for value in sys.path if value not in {root_value, ""}]
        sys.path.insert(0, root_value)
        yield
    finally:
        for name in list(sys.modules):
            if (
                name == "tigrbl_auth"
                or name.startswith("tigrbl_auth.")
                or name.startswith(SPLIT_MODULE_PREFIXES)
            ):
                sys.modules.pop(name, None)
        sys.modules.update(removed_modules)
        sys.path = original_path


@contextmanager
def package_src_paths_only():
    original_path = list(sys.path)
    removed_modules = {
        name: module
        for name, module in sys.modules.items()
        if name == "tigrbl_auth"
        or name.startswith("tigrbl_auth.")
        or name.startswith(SPLIT_MODULE_PREFIXES)
    }
    for name in list(removed_modules):
        sys.modules.pop(name, None)
    try:
        root_values = {str(ROOT), ""}
        sys.path = [value for value in sys.path if value not in root_values]
        for src in PKGS.glob("*/src"):
            value = str(src)
            if value not in sys.path:
                sys.path.insert(0, value)
        yield
    finally:
        for name in list(sys.modules):
            if (
                name == "tigrbl_auth"
                or name.startswith("tigrbl_auth.")
                or name.startswith(SPLIT_MODULE_PREFIXES)
            ):
                sys.modules.pop(name, None)
        sys.modules.update(removed_modules)
        sys.path = original_path


def test_legacy_facade_modules_alias_canonical_module_objects() -> None:
    with source_tree_paths_first():
        for legacy_name, canonical_name in FACADE_MODULES.items():
            legacy = importlib.import_module(legacy_name)
            canonical = importlib.import_module(canonical_name)

            assert legacy is canonical


def test_legacy_executable_facades_preserve_private_patch_points() -> None:
    with source_tree_paths_first():
        for legacy_name, canonical_name in EXECUTABLE_FACADE_MODULES.items():
            legacy = importlib.import_module(legacy_name)
            canonical = importlib.import_module(canonical_name)

            assert legacy.DEVICE_CODE_GRANT_TYPE == canonical.DEVICE_CODE_GRANT_TYPE
            assert legacy.token_request.__code__.co_code == canonical.token_request.__code__.co_code
            assert hasattr(legacy, "_require_tls")


def test_installable_tigrbl_auth_facade_exposes_runtime_legacy_paths() -> None:
    with package_src_paths_only():
        for legacy_name, canonical_name in INSTALLED_FACADE_MODULES.items():
            legacy = importlib.import_module(legacy_name)
            canonical = importlib.import_module(canonical_name)

            assert legacy is canonical


def test_tigrbl_auth_facade_declares_canonical_runtime_dependencies() -> None:
    import tomllib

    metadata = tomllib.loads(
        (ROOT / "pkgs" / "tigrbl-auth" / "pyproject.toml").read_text(encoding="utf-8")
    )

    assert set(metadata["project"]["dependencies"]).issuperset(
        {
            "tigrbl-identity-cli==0.4.0.dev2",
            "tigrbl-identity-admin==0.4.0.dev2",
            "tigrbl-authn-credentials==0.4.0.dev2",
            "tigrbl-identity-jose==0.4.0.dev2",
            "tigrbl-auth-protocol-oauth==0.4.0.dev2",
            "tigrbl-identity-operator==0.4.0.dev2",
            "tigrbl-authz-policy==0.4.0.dev2",
            "tigrbl-identity-runtime==0.4.0.dev2",
            "tigrbl-identity-server==0.4.0.dev2",
            "tigrbl-identity-storage==0.4.0.dev2",
        }
    )


def test_tigrbl_auth_has_no_large_exact_copies_of_split_package_modules() -> None:
    canonical_hashes: dict[str, list[Path]] = {}
    for package_root in sorted(PKGS.glob("*/src")):
        if package_root.parent.name == "tigrbl-auth":
            continue
        for path in package_root.rglob("*.py"):
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            canonical_hashes.setdefault(digest, []).append(path)

    duplicate_large_files: list[str] = []
    for path in sorted(LEGACY_ROOT.rglob("*.py")):
        if len(path.read_text(encoding="utf-8").splitlines()) <= LARGE_FILE_THRESHOLD:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        matches = canonical_hashes.get(digest, [])
        if matches:
            duplicate_large_files.append(
                f"{path.relative_to(ROOT).as_posix()} duplicates "
                f"{matches[0].relative_to(ROOT).as_posix()}"
            )

    assert duplicate_large_files == []
