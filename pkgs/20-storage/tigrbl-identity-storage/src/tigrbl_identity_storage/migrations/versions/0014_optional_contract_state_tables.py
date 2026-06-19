"""Executable DDL migration for optional contract state tables."""

from __future__ import annotations

from tigrbl_identity_storage.migrations.helpers import create_tables, drop_tables
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

revision = "0014_optional_contract_state_tables"
down_revision = "0013_contract_durable_state_tables"
branch_labels = None
depends_on = None

TABLES = (
    SDKPackageRecord,
    PluginDescriptorRecord,
    PluginLifecycleEventRecord,
    ScimSchemaRecord,
    ScimUserRecord,
    ScimGroupRecord,
    ScimPatchEvent,
    ReleaseCapabilityRecord,
    ReleaseAuthorizationState,
    RuntimeQualificationRecord,
    ReleaseSecurityPosture,
    ReleasePosture,
    ReleaseAttestationEvent,
    ControlCorrectnessReport,
    AuthzVerificationReport,
    ResourceServerContract,
    ProviderArtifact,
)


def upgrade(conn) -> None:
    create_tables(conn, *TABLES)


def downgrade(conn) -> None:
    drop_tables(conn, *reversed(TABLES))
