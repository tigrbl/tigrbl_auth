"""Compatibility facade for `tigrbl_identity_storage.tables`."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_SUBMODULES = (
    "access_review_campaign",
    "access_review_decision",
    "access_review_item",
    "attribute_policy",
    "audit_event",
    "auth_code",
    "auth_session",
    "authorization_server",
    "client",
    "client_registration",
    "consent",
    "credential",
    "credential_audit_event",
    "credential_api_key",
    "credential_client_secret",
    "credential_dpop_key",
    "credential_mfa_factor",
    "credential_mtls_certificate",
    "credential_password",
    "credential_recovery_code",
    "credential_service_key",
    "credential_webauthn_passkey",
    "crypto_key",
    "crypto_key_version",
    "delegation_grant",
    "delegated_admin_scope",
    "device_code",
    "engine",
    "entitlement",
    "entitlement_assignment",
    "key_attestation_evidence",
    "key_envelope",
    "key_rotation_event",
    "key_rotation_policy",
    "logout_state",
    "machine_identity",
    "policy_condition",
    "principal",
    "principal_key_binding",
    "pushed_authorization_request",
    "realm",
    "revoked_token",
    "residency_zone",
    "role",
    "service_identity",
    "subject_alias",
    "tenant",
    "tenant_membership",
    "tenant_residency",
    "token_record",
    "user",
    "workload_identity",
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
