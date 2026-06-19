from __future__ import annotations

import ast
from pathlib import Path


TABLES_DIR = (
    Path(__file__).resolve().parents[2]
    / "pkgs"
    / "20-storage"
    / "tigrbl-identity-storage"
    / "src"
    / "tigrbl_identity_storage"
    / "tables"
)


REQUIRED_TABLE_OPS = {
    "auth_session.py": {"AuthSession": {"create_for_user", "list_for_user", "revoke_for_user", "revoke_all_for_user", "touch"}},
    "consent.py": {"Consent": {"grant", "list_for_user", "revoke_for_user", "revoke_for_client"}},
    "token_record.py": {"TokenRecord": {"persist_issued_token", "list_active_for_subject", "revoke_family", "mark_rotated"}},
    "revoked_token.py": {"RevokedToken": {"revoke_token", "is_revoked"}},
    "auth_code.py": {"AuthCode": {"create_for_authorization", "consume", "expire"}},
    "device_code.py": {"DeviceCode": {"create_device_authorization", "approve", "deny", "poll", "consume"}},
    "pushed_authorization_request.py": {
        "PushedAuthorizationRequest": {"create_request", "resolve_request_uri", "consume", "consume_request"}
    },
    "client.py": {"Client": {"new", "verify_secret", "authenticate", "rotate_secret", "enable", "disable"}},
    "client_registration.py": {
        "ClientRegistration": {"register_client", "read_registration", "update_registration", "delete_registration"}
    },
    "audit_event.py": {"AuditEvent": {"record", "list_for_subject", "list_for_tenant"}},
    "logout_state.py": {"LogoutState": {"create_logout", "consume_logout", "expire"}},
    "realm.py": {"Realm": {"create_realm", "update_realm", "list_realms", "lookup_by_slug"}},
    "tenant.py": {"Tenant": {"create_tenant", "update_tenant", "disable_tenant", "list_by_realm", "lookup_by_name"}},
    "user.py": {"User": {"create_user", "update_user", "disable_user", "list_by_tenant", "lookup_by_identifier"}},
    "delegation_grant.py": {
        "DelegationGrantRecord": {"create_grant", "revoke_grant", "list_grants"},
        "DelegationGrantProof": {"persist_provenance"},
        "DelegationGrantTokenLink": {"link_token"},
    },
    "key.py": {"Key": {"create_key", "lookup_by_kid", "list_active", "enable", "disable", "retire", "rotate", "publish_jwks", "sign", "verify"}},
    "key_version.py": {"KeyVersion": {"create_version", "lookup", "list_for_key", "activate", "retire", "export_public_jwk"}},
    "credential.py": {"Credential": {"create_credential", "lookup_active", "list_for_principal", "rotate", "revoke"}},
    "credential_audit_event.py": {"CredentialAuditEvent": {"record", "list_for_credential", "list_for_principal"}},
    "credential_mtls_certificate.py": {"CredentialMtlsCertificate": {"bind_certificate", "lookup_by_thumbprint", "list_for_principal", "revoke"}},
    "credential_dpop_key.py": {"CredentialDpopKey": {"bind_key", "lookup_by_thumbprint", "list_for_principal", "revoke"}},
    "tenant_membership.py": {"TenantMembership": {"grant_membership", "lookup", "list_for_principal", "revoke_membership"}},
    "subject_alias.py": {"SubjectAlias": {"bind_alias", "lookup", "list_for_principal", "verify_alias"}},
    "role.py": {"Role": {"create_role", "lookup", "list_for_tenant", "disable"}},
    "attribute_policy.py": {"AttributePolicy": {"create_policy", "lookup", "list_for_permission", "disable"}},
    "policy_condition.py": {"PolicyCondition": {"add_condition", "list_for_policy"}},
    "delegated_admin_scope.py": {"DelegatedAdminScope": {"grant_scope", "lookup", "list_active", "revoke_scope"}},
    "key_rotation_policy.py": {"KeyRotationPolicy": {"create_policy_version", "lookup_version", "list_for_tenant", "approve", "publish"}},
    "entitlement.py": {"Entitlement": {"define", "lookup", "list_for_tenant", "disable"}},
    "entitlement_assignment.py": {"EntitlementAssignment": {"assign", "lookup", "list_for_subject", "revoke"}},
    "access_review_campaign.py": {"AccessReviewCampaign": {"create_campaign", "lookup", "list_for_tenant", "close"}},
    "access_review_item.py": {"AccessReviewItem": {"create_item", "lookup", "list_for_campaign", "mark_decided"}},
    "access_review_decision.py": {"AccessReviewDecision": {"record_decision", "lookup", "list_for_item"}},
    "residency_zone.py": {"ResidencyZone": {"create_zone", "lookup", "list_active", "disable"}},
    "tenant_residency.py": {"TenantResidency": {"assign_residency", "lookup", "list_for_zone", "disable"}},
}


def _class_methods(path: Path, class_name: str) -> set[str]:
    module = ast.parse(path.read_text(encoding="utf-8"))
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return {item.name for item in node.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))}
    raise AssertionError(f"{class_name} not found in {path}")


def test_storage_tables_own_required_operation_methods() -> None:
    missing: list[str] = []

    for filename, class_requirements in REQUIRED_TABLE_OPS.items():
        path = TABLES_DIR / filename
        if not path.exists():
            path = TABLES_DIR / filename.removesuffix(".py") / "_table.py"
        for class_name, operation_names in class_requirements.items():
            defined = _class_methods(path, class_name)
            for name in sorted(operation_names - defined):
                missing.append(f"{class_name}.{name}")

    assert missing == []
