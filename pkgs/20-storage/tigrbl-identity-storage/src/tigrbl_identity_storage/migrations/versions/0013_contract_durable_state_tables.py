"""Executable DDL migration for contract-backed durable state tables."""

from __future__ import annotations

from tigrbl_identity_storage.migrations.helpers import create_tables, drop_tables
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

revision = "0013_contract_durable_state_tables"
down_revision = "0012_key_version_and_token_provenance_tables"
branch_labels = None
depends_on = None

TABLES = (
    Credential,
    CredentialAuditEvent,
    CredentialDpopKey,
    CredentialMtlsCertificate,
    TenantMembership,
    SubjectAlias,
    Role,
    AttributePolicy,
    PolicyCondition,
    DelegatedAdminScope,
    KeyRotationPolicy,
    Entitlement,
    EntitlementAssignment,
    AccessReviewCampaign,
    AccessReviewItem,
    AccessReviewDecision,
    ResidencyZone,
    TenantResidency,
)


def upgrade(conn) -> None:
    create_tables(conn, *TABLES)


def downgrade(conn) -> None:
    drop_tables(conn, *TABLES)
