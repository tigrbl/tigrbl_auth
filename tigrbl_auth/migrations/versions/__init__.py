"""Compatibility facade for identity-storage migration version modules."""

from importlib import import_module
import sys

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

_VERSIONS = (
    "0001_initial_identity_tables",
    "0002_client_and_service_tables",
    "0003_authorization_runtime_tables",
    "0004_device_par_revocation_tables",
    "0005_session_logout_tables",
    "0006_key_rotation_and_audit_tables",
    "0007_browser_session_cookie_and_auth_code_linkage",
    "0008_refresh_token_family_state",
    "0009_admin_identity_bootstrap_and_password_recovery",
    "0010_realm_namespace_tables",
    "0011_delegation_grant_lifecycle_tables",
)

_LEGACY_NAME = __name__
_module = import_module("tigrbl_identity_storage.migrations.versions")
sys.modules[__name__] = _module
globals().update(_module.__dict__)

for _version in _VERSIONS:
    sys.modules[f"{_LEGACY_NAME}.{_version}"] = import_module(
        f"tigrbl_identity_storage.migrations.versions.{_version}"
    )
