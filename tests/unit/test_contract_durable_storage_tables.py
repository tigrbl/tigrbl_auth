from __future__ import annotations

from tigrbl_identity_storage.tables import (
    AccessReviewCampaign,
    AccessReviewDecision,
    AccessReviewItem,
    AttributePolicy,
    AuthzVerificationReport,
    ControlCorrectnessReport,
    Credential,
    CredentialAuditEvent,
    CredentialDpopKey,
    CredentialMtlsCertificate,
    DelegatedAdminScope,
    Entitlement,
    EntitlementAssignment,
    KeyRotationPolicy,
    PolicyCondition,
    PluginDescriptorRecord,
    PluginLifecycleEventRecord,
    ProviderArtifact,
    ReleaseAttestationEvent,
    ReleaseAuthorizationState,
    ReleaseCapabilityRecord,
    ReleasePosture,
    ReleaseSecurityPosture,
    ResidencyZone,
    ResourceServerContract,
    Role,
    RuntimeQualificationRecord,
    SDKPackageRecord,
    ScimGroupRecord,
    ScimPatchEvent,
    ScimSchemaRecord,
    ScimUserRecord,
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
        SDKPackageRecord: "sdk_packages",
        PluginDescriptorRecord: "plugin_descriptors",
        PluginLifecycleEventRecord: "plugin_lifecycle_events",
        ScimSchemaRecord: "scim_schemas",
        ScimUserRecord: "scim_users",
        ScimGroupRecord: "scim_groups",
        ScimPatchEvent: "scim_patch_events",
        ReleaseCapabilityRecord: "release_capability_records",
        ReleaseAuthorizationState: "release_authorization_states",
        RuntimeQualificationRecord: "runtime_qualifications",
        ReleaseSecurityPosture: "release_security_postures",
        ReleasePosture: "release_postures",
        ReleaseAttestationEvent: "release_attestation_events",
        ControlCorrectnessReport: "control_correctness_reports",
        AuthzVerificationReport: "authz_verification_reports",
        ResourceServerContract: "resource_server_contracts",
        ProviderArtifact: "provider_artifacts",
    }

    for model, table_name in expected.items():
        assert model.__tablename__ == table_name
        assert getattr(model, "__table__", None) is not None
        assert getattr(model, "handlers", None) is not None


def test_remaining_ephemeral_contracts_are_not_duplicated_as_storage_tables() -> None:
    table_names = {table.name for table in Credential.metadata.sorted_tables if table.schema == "authn"}

    assert "jose_keys" not in table_names
    assert "key_rotation_contracts" not in table_names
    assert "policy_decisions" not in table_names
    assert "residency_decisions" not in table_names
    assert "verification_results" not in table_names
