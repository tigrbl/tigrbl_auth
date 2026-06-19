from __future__ import annotations

from tigrbl_identity_storage.tables import (
    AuthzVerificationReport,
    ControlCorrectnessReport,
    PluginDescriptorRecord,
    PluginLifecycleEventRecord,
    ProviderArtifact,
    ReleaseAttestationEvent,
    ReleaseAuthorizationState,
    ReleaseCapabilityRecord,
    ReleasePosture,
    ReleaseSecurityPosture,
    ResourceServerContract,
    RuntimeQualificationRecord,
    SDKPackageRecord,
    ScimGroupRecord,
    ScimPatchEvent,
    ScimSchemaRecord,
    ScimUserRecord,
)


def test_optional_contract_state_tables_are_storage_owned() -> None:
    expected = {
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
        assert model.__module__.startswith("tigrbl_identity_storage.tables.")
        assert model.__tablename__ == table_name
        assert getattr(model, "__table__", None) is not None
        assert getattr(model, "handlers", None) is not None


def test_optional_contract_state_tables_keep_payload_columns_for_contract_shapes() -> None:
    payload_columns = {
        SDKPackageRecord: "contract_payload",
        PluginDescriptorRecord: "descriptor_payload",
        PluginLifecycleEventRecord: "event_payload",
        ScimSchemaRecord: "schema_payload",
        ScimPatchEvent: "value_payload",
        ReleaseCapabilityRecord: "capability_payload",
        ReleaseAuthorizationState: "state_payload",
        RuntimeQualificationRecord: "qualification_payload",
        ReleaseSecurityPosture: "posture_payload",
        ReleasePosture: "posture_payload",
        ReleaseAttestationEvent: "event_payload",
        ControlCorrectnessReport: "report_payload",
        AuthzVerificationReport: "report_payload",
        ResourceServerContract: "contract_payload",
        ProviderArtifact: "artifact_payload",
    }

    for model, column_name in payload_columns.items():
        assert column_name in model.__table__.columns
