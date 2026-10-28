"""Compatibility facade for storage migration runtime and durable assets."""

from tba_auth._split_imports import alias_module as _alias_module

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
_module = _alias_module(
    __name__,
    "tba_runtime_identity_storage.migrations",
    "tba-runtime-identity-storage",
)
globals().update(_module.__dict__)

for _submodule in ("env", "helpers"):
    _alias_module(
        f"{_LEGACY_NAME}.{_submodule}",
        f"tba_storage_core.migrations.{_submodule}",
        "tba-storage-core",
    )
_alias_module(
    f"{_LEGACY_NAME}.runtime",
    "tba_runtime_identity_storage.migrations.runtime",
    "tba-runtime-identity-storage",
)

_alias_module(
    f"{_LEGACY_NAME}.versions",
    "tba_storage_core.migrations.versions",
    "tba-storage-core",
)
for _version in _VERSIONS:
    _alias_module(
        f"{_LEGACY_NAME}.versions.{_version}",
        f"tba_storage_core.migrations.versions.{_version}",
        "tba-storage-core",
    )
