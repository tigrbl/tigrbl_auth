from __future__ import annotations

from tigrbl_identity_storage.tables import (
    AccessReviewCampaign,
    AccessReviewDecision,
    AccessReviewItem,
    AttributePolicy,
    Credential,
    CredentialAuditEvent,
    CredentialDpopKey,
    CredentialMtlsCertificate,
    DelegatedAdminScope,
    Entitlement,
    EntitlementAssignment,
    KeyRotationPolicy,
    PolicyCondition,
    ResidencyZone,
    Role,
    SubjectAlias,
    TenantMembership,
    TenantResidency,
)


def test_remaining_definitely_durable_contracts_have_storage_tables() -> None:
    expected = {
        Credential: "credentials",
        CredentialAuditEvent: "credential_audit_events",
        CredentialDpopKey: "credential_dpop_keys",
        CredentialMtlsCertificate: "credential_mtls_certificates",
        TenantMembership: "tenant_memberships",
        SubjectAlias: "subject_aliases",
        Role: "roles",
        AttributePolicy: "attribute_policies",
        PolicyCondition: "policy_conditions",
        DelegatedAdminScope: "delegated_admin_scopes",
        KeyRotationPolicy: "key_rotation_policies",
        Entitlement: "entitlements",
        EntitlementAssignment: "entitlement_assignments",
        AccessReviewCampaign: "access_review_campaigns",
        AccessReviewItem: "access_review_items",
        AccessReviewDecision: "access_review_decisions",
        ResidencyZone: "residency_zones",
        TenantResidency: "tenant_residency",
    }

    for model, table_name in expected.items():
        assert model.__tablename__ == table_name
        assert getattr(model, "__table__", None) is not None
        assert getattr(model, "handlers", None) is not None


def test_optional_contracts_are_not_duplicated_as_storage_tables() -> None:
    table_names = {table.name for table in Credential.metadata.sorted_tables if table.schema == "authn"}

    assert "jose_keys" not in table_names
    assert "key_rotation_contracts" not in table_names
    assert "policy_decisions" not in table_names
    assert "residency_decisions" not in table_names
    assert "verification_results" not in table_names
