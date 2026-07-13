from __future__ import annotations

import asyncio

import pytest
from tigrbl_identity_storage.tables import (
    AttestationEvidence,
    CredentialIssuanceTransaction,
    CredentialOffer,
    CredentialStatusEntry,
    PresentationConsent,
    PresentationReplay,
    PresentationTransaction,
    SecurityEvent,
    SecurityEventDelivery,
    SecurityEventReplay,
    SpiffeTrustBundle,
    SvidRecord,
)
from tigrbl_identity_storage_runtime import (
    AttestationEvidenceRuntimeSpec,
    CredentialIssuanceTransactionRuntimeSpec,
    CredentialOfferRuntimeSpec,
    CredentialStatusEntryRuntimeSpec,
    PresentationConsentRuntimeSpec,
    PresentationReplayRuntimeSpec,
    PresentationTransactionRuntimeSpec,
    SecurityEventDeliveryRuntimeSpec,
    SecurityEventReplayRuntimeSpec,
    SecurityEventRuntimeSpec,
    SpiffeTrustBundleRuntimeSpec,
    SvidRecordRuntimeSpec,
)


def _operation(spec, alias: str):
    return next(operation for operation in spec.ops if operation.alias == alias)


def test_runtime_specs_target_authoritative_layer_01_tables() -> None:
    pairs = (
        (CredentialOfferRuntimeSpec, CredentialOffer),
        (CredentialIssuanceTransactionRuntimeSpec, CredentialIssuanceTransaction),
        (CredentialStatusEntryRuntimeSpec, CredentialStatusEntry),
        (PresentationTransactionRuntimeSpec, PresentationTransaction),
        (PresentationConsentRuntimeSpec, PresentationConsent),
        (PresentationReplayRuntimeSpec, PresentationReplay),
        (AttestationEvidenceRuntimeSpec, AttestationEvidence),
        (SecurityEventRuntimeSpec, SecurityEvent),
        (SecurityEventDeliveryRuntimeSpec, SecurityEventDelivery),
        (SecurityEventReplayRuntimeSpec, SecurityEventReplay),
        (SvidRecordRuntimeSpec, SvidRecord),
        (SpiffeTrustBundleRuntimeSpec, SpiffeTrustBundle),
    )

    for spec, table in pairs:
        assert spec.model is table
        assert table.__module__.startswith("tigrbl_identity_storage.tables")


def test_family_operations_are_carrier_neutral_table_operations() -> None:
    operations = (
        _operation(CredentialOfferRuntimeSpec, "create_offer"),
        _operation(PresentationTransactionRuntimeSpec, "begin_presentation"),
        _operation(AttestationEvidenceRuntimeSpec, "record_evidence"),
        _operation(SecurityEventRuntimeSpec, "record_event"),
        _operation(SvidRecordRuntimeSpec, "record_svid"),
    )
    for operation in operations:
        assert operation.target == "custom"
        assert operation.tx_scope == "read_write"
        assert operation.bindings == ()
        assert operation.handler is operation.core


def test_table_operation_refuses_sensitive_raw_values_before_persistence() -> None:
    operation = _operation(CredentialOfferRuntimeSpec, "create_offer")
    for field in (
        "raw_nonce",
        "pre_authorized_code",
        "presentation_disclosures",
        "raw_payload",
    ):
        with pytest.raises(ValueError, match="sensitive raw fields"):
            asyncio.run(operation.handler({"payload": {field: "secret"}, "db": object()}))
