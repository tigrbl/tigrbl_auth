"""Compatibility facade for `tigrbl_identity_storage.tables`."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_SUBMODULES = (
    "api_key",
    "access_review_campaign",
    "access_review_decision",
    "access_review_item",
    "attribute_policy",
    "audit_event",
    "auth_code",
    "auth_session",
    "client",
    "client_registration",
    "consent",
    "credential",
    "credential_audit_event",
    "credential_dpop_key",
    "credential_mtls_certificate",
    "delegation_grant",
    "delegated_admin_scope",
    "device_code",
    "engine",
    "entitlement",
    "entitlement_assignment",
    "key",
    "key_rotation_event",
    "key_rotation_policy",
    "key_version",
    "logout_state",
    "policy_condition",
    "pushed_authorization_request",
    "realm",
    "revoked_token",
    "residency_zone",
    "role",
    "service",
    "service_key",
    "subject_alias",
    "tenant",
    "tenant_membership",
    "tenant_residency",
    "token_record",
    "user",
)

_LEGACY_NAME = __name__
_module = _alias_module(__name__, "tigrbl_identity_storage.tables", "tigrbl-identity-storage")
globals().update(_module.__dict__)

for _submodule in _SUBMODULES:
    _alias_module(
        f"{_LEGACY_NAME}.{_submodule}",
        f"tigrbl_identity_storage.tables.{_submodule}",
        "tigrbl-identity-storage",
    )
